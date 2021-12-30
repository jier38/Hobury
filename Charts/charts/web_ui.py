import re
from datetime import datetime
from trac.core import *
from trac.util.html import html
from trac.web.api import IRequestHandler, HTTPNotFound
from trac.web.chrome import Chrome, INavigationContributor
from trac.perm import IPermissionRequestor


class Charts(Component):

    implements(
        IRequestHandler,
        INavigationContributor,
        IPermissionRequestor
    )

    # INavigationContributor methods
    def get_active_navigation_item(self, req):
        return 'charts'

    def get_navigation_items(self, req):
        if 'CHARTS_VIEW' in req.perm:
            yield (
                'mainnav',
                'charts',
                html.a('Charts', href=req.href.charts())
            )

    # IRequstHandler methods
    def match_request(self, req):
        return req.path_info.find('/charts') == 0

    def process_request(self, req):
        data = {}
        cursor = self.env.db_query(
                     "SELECT t.symbol as symbol, max(t.date) as date, tt.quantity as quantity "
                     "FROM invest.trades t inner join (select exchange, symbol, sum(quantity * case when type = 'Verkoop' then -1 else 1 end) as quantity " "FROM invest.trades WHERE type in ('Koop', 'Verkoop') group by exchange, symbol having quantity > 0) tt "
					 "on t.exchange = tt.exchange and t.symbol = tt.symbol " 
                     "WHERE type = 'Koop' group by t.exchange, t.symbol;"
                 )
        data['holdings'] = [(row[0],row[1],row[2]) for row in cursor]
        return 'charts.html', data, {}

    def get_permission_actions(self):
        view = 'CHARTS_VIEW'
        return [view]
