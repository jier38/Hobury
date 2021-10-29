import re
from datetime import datetime
from trac.core import *
from trac.util.html import html
from trac.web.api import IRequestHandler, HTTPNotFound
from trac.perm import IPermissionRequestor
from trac.web.chrome import (
                                Chrome,
                                INavigationContributor,
                                add_warning,
                                add_notice
                            )


class TradEntry(Component):

    implements(
        IRequestHandler,
        INavigationContributor,
        IPermissionRequestor
    )

    def get_permission_actions(self):
        view = 'TRADES'
        return [view]

    # INavigationContributor methods

    def get_active_navigation_item(self, req):
        return 'trade'

    def get_navigation_items(self, req):
        if 'TRADES' in req.perm:
            yield ('mainnav', 'trade', html.a('Trade', href=req.href.trade()))

    # IRequstHandler methods

    def match_request(self, req):
        return req.path_info.find('/trade') == 0

    def process_request(self, req):
        if req.path_info.find('/trade/list') == 0:
            data = {}
            cursor = self.env.db_query(
                         'SELECT id, portfolio, buysell, quantity, exchange, '
                         'symbol, cash, currency, tradedate, tradeid '
                         'FROM invest.trades ORDER BY id'
                     )
            data['trades'] = [
                                 (
                                     row[0], row[1], row[2], row[3],
                                     row[4], row[5], row[6], row[7],
                                     row[8], row[9]
						         ) for row in cursor
							 ]
            return 'trade_list.html', data, {}
        else:
            data = {}
            cursor = self.env.db_query(
                         "SELECT value FROM invest.parameters "
                         "WHERE type='tolerance' and metric='quantity' "
                         "LIMIT 1"
                     )
            data['tolerance'] = [(row[0]) for row in cursor]
            cursor = self.env.db_query(
                         "SELECT distinct currency as metric from invest.exchanges order by currency"
                     )
            data['currencyList'] = [(row[0]) for row in cursor]
            cursor = self.env.db_query(
                         "SELECT distinct exchange as metric, currency  from invest.exchanges order by exchange"
                     )
            data['exchangeList'] = [(row[0], row[1]) for row in cursor]
            cursor = self.env.db_query(
                "SELECT name FROM invest.portfolios ORDER BY name")
            data['portfolioList'] = [(row[0]) for row in cursor]
            cursor = self.env.db_query(
                         "SELECT exchange, symbol, name "
                         "FROM invest.components ORDER BY exchange, symbol"
                     )
            data['symbolList'] = [(row[0], row[1], row[2]) for row in cursor]
            data['tradedate'] = datetime.now().strftime('%Y-%m-%d')
            if req.method == 'POST':
                portfolio = req.args.get('portfolio').strip()
                buysell = req.args.get('buysell').strip()
                quantity = req.args.get('quantity').strip()
                exchange = req.args.get('exchange').strip()
                cash = req.args.get('cash').strip()
                currency = req.args.get('currency').strip()
                temp = req.args.get('symbol').strip()
                tradedate = req.args.get('tradedate').strip()
                symbol = ''
                for row in cursor:
                    if row[0] == exchange:
                        if row[1] == temp:
                            symbol = temp
                            break
                        elif row[2] == temp:
                            symbol = row[1]
                            break
                if symbol == '':
                    data['portfolio'] = portfolio
                    data['buysell'] = buysell
                    data['quantity'] = quantity
                    data['exchange'] = exchange
                    data['currency'] = currency
                    data['cash'] = cash
                    data['symbol'] = temp
                    data['tradedate'] = tradedate
                    add_warning(req, 'Please enter valid symbol or name.')
                else:
                    sql = (
                              "SELECT IFNULL(avg(close),0)*(1+( "
                              "SELECT avg(value) FROM invest.parameters "
                              "WHERE type='tolerance' and metric='cash')) " 
                              "FROM invest.prices WHERE exchange=%s and symbol=%s "
                              "and datediff(now(), date) < 10"
                          )
                    args = (exchange, symbol)
                    cursor = self.env.db_query(sql, args)
                    data['price'] = [(row[0]) for row in cursor]
                    if float(data['price'][0]) <= 0:
                        data['portfolio'] = portfolio
                        data['buysell'] = buysell
                        data['quantity'] = quantity
                        data['exchange'] = exchange
                        data['currency'] = currency
                        data['cash'] = cash
                        data['symbol'] = temp
                        data['tradedate'] = tradedate
                        add_warning(
                            req, 'The security is no longer tradeable.')
                    elif float(cash)/int(quantity) > float(data['price'][0]):
                        data['portfolio'] = portfolio
                        data['buysell'] = buysell
                        data['quantity'] = quantity
                        data['exchange'] = exchange
                        data['currency'] = currency
                        data['cash'] = cash
                        data['symbol'] = temp
                        data['tradedate'] = tradedate
                        add_warning(
                            req,
                            'The cash/quantity exceeds the price tolerance '
                            'of the last 10 days.'
                        )
                    else:
                        sql = (
                                  "INSERT INTO invest.trades "
                                  "(portfolio,buysell,quantity,exchange,"
                                  "symbol,cash,currency,tradedate,tradeid) "
                                  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        )
                        args = (portfolio, buysell, quantity, exchange,
                                symbol, cash, currency, tradedate, req.authname)
                        self.env.db_transaction(sql, args)
                        add_notice(req, 'Your trade has been saved.')
            chrome = Chrome(self.env)
            chrome.add_auto_preview(req)
            chrome.add_wiki_toolbars(req)
            return 'trade_view.html', data, {}