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

    # IRequestHandler methods

    def match_request(self, req):
        return req.path_info.find('/trade') == 0

    def process_request(self, req):
        if req.path_info.find('/trade/list') == 0:
            data = {}
            cursor = self.env.db_query("select max(t.date) as date, t.portfolio, t.exchange, t.symbol, c.name, tt.quantity "
                "from (invest.trades t inner join (select portfolio, exchange, symbol, sum(quantity * case when type = 'Verkoop' then -1 "
                "else 1 end) as quantity from invest.trades where type in ('Koop', 'Verkoop') group by portfolio, exchange, symbol having "
                "quantity > 0) tt on t.portfolio = tt.portfolio and t.exchange = tt.exchange and t.symbol = tt.symbol) "
                "left join invest.components c on t.exchange = c.exchange and t.symbol = c.symbol "
                "where type = 'Koop' group by t.portfolio, t.exchange, t.symbol, c.name"
            )
            data['trades'] = [
                (row[0], row[1], row[2], row[3], row[4], row[5]) 
                for row in cursor
            ]
            return 'trade_list.html', data, {}
        else:
            data = {}
            # Add warning when cash / quantity does not approximate the price of the last few days
            cursor = self.env.db_query(
                "select value from invest.parameters where type = 'tolerance' and metric = 'quantity' limit 1"
            )
            data['tolerance'] = [(row[0]) for row in cursor]

            cursor = self.env.db_query(
                "select distinct currency as metric from invest.exchanges where owner = 'broker' order by currency"
            )
            data['currency'] = "EUR"
            data['currencyList'] = [(row[0]) for row in cursor]
            cursor = self.env.db_query(
                "select exchange, currency from invest.exchanges where owner = 'broker' order by exchange"
            )
            data['exchangeList'] = [(row[0], row[1]) for row in cursor]

            cursor = self.env.db_query(
                "select name from invest.portfolios order by name"
            )
            data['portfolioList'] = [(row[0]) for row in cursor]

            cursor = self.env.db_query(
                 "select exchange, symbol, name from invest.components order by exchange, symbol"
            )
            data['symbolList'] = [(row[0], row[1], row[2]) for row in cursor]
            data['date'] = datetime.now().strftime('%Y-%m-%d')
            if req.method == 'POST':
                portfolio = req.args.get('portfolio').strip()
                type = req.args.get('type').strip()
                quantity = req.args.get('quantity').strip()
                exchange = req.args.get('exchange').strip()
                cash = req.args.get('cash').strip()
                currency = req.args.get('currency').strip()
                temp = req.args.get('symbol').strip()
                date = req.args.get('date').strip()
                symbol = ''
                entireholding = req.args.get('entireholding')
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
                    data['type'] = type
                    data['quantity'] = quantity
                    data['exchange'] = exchange
                    data['currency'] = currency
                    data['cash'] = cash
                    data['symbol'] = temp
                    data['date'] = date
                    add_warning(req, 'Please enter valid symbol or name.')
                else:
                    sql = ("select ifnull(avg(close), 0)*(1+( "
                           "select avg(value) from invest.parameters where type = 'tolerance' and metric = 'cash')) " 
                           "from invest.prices where exchange = %s and symbol = %s and datediff(now(), date) < 10"
                          )
                    args = (exchange, symbol)
                    cursor = self.env.db_query(sql, args)
                    data['price'] = [(row[0]) for row in cursor]
                    sql = ("select sum(quantity * case when type = 'Verkoop' then -1 else 1 end) as quantity "
                           "from invest.trades " 
                           "where exchange = %s and symbol = %s and portfolio = %s and type in ('Koop', 'Verkoop') " 
                           "group by exchange, symbol, portfolio"
                          )
                    args = (exchange, symbol, portfolio)
                    cursor = self.env.db_query(sql, args)
                    holding = [(row[0]) for row in cursor]
                    if type.lower() == 'verkoop' and entireholding == 'on':
                        sql = ("select exchange, symbol, sum(quantity * case when type = 'Verkoop' then -1 else 1 end) as quantity "
                               "from invest.trades ",
                               "where exchange = %s and symbol = %s and type in ('Koop', 'Verkoop') "
                               "group by exchange, symbol"
                              )
                        args = (exchange, symbol)
                        cursor = self.env.db_query(sql, args)
                        data['holding'] = [(row[2]) for row in cursor]
                        quantity = data['holding'][0]
                    if (type.lower() == 'verkoop') and (len(holding) <= 0 or int(holding[0]) <= 0):
                        add_warning(req, 'There is no holding of that symbol in this portfolio.')
                    elif int(quantity) <= 0:
                        if entireholding == 'on':
                            add_warning(req, 'No holding in this symbol.')
                        else:
                            add_warning(req, 'Enter the quantity bought or sold.')
                    elif type.lower() == 'verkoop' and int(quantity) > int(holding[0]):
                        add_warning(req, 'Cannot sell more than is being held.')
                    elif float(data['price'][0]) <= 0:
                        data['portfolio'] = portfolio
                        data['type'] = type
                        data['quantity'] = quantity
                        data['exchange'] = exchange
                        data['currency'] = currency
                        data['cash'] = cash
                        data['symbol'] = temp
                        data['date'] = date
                        add_warning(req, 'The security is no longer tradeable.')
                    elif float(cash)/int(quantity) > float(data['price'][0]):
                        data['portfolio'] = portfolio
                        data['type'] = type
                        data['quantity'] = quantity
                        data['exchange'] = exchange
                        data['currency'] = currency
                        data['cash'] = cash
                        data['symbol'] = temp
                        data['date'] = date
                        add_warning(
                            req, 'The cash/quantity exceeds the price tolerance of the last 10 days.'
                        )
                    else:
                        sql = ("INSERT INTO invest.trades "
                               "(portfolio, type, quantity, exchange, symbol, cash, currency, date, description) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, (select name from invest.components where exchange = %s and symbol = %s))"
                        )
                        args = (portfolio.lower(), type, quantity, exchange, symbol, cash, currency, date, exchange, symbol)
                        self.env.db_transaction(sql, args)
                        add_notice(req, 'Your trade has been saved.')
            chrome = Chrome(self.env)
            chrome.add_auto_preview(req)
            chrome.add_wiki_toolbars(req)
            return 'trade_view.html', data, {}
