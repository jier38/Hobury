from trac.core import *
from trac.admin import IAdminPanelProvider
from trac.resource import Resource
from trac.web.chrome import Chrome, add_warning, add_notice


class PortfolioPanel(Component):
    """Admin panel for settings related to Portfolio plugin."""

    implements(IAdminPanelProvider)

    # IAdminPageProvider

    def get_admin_panels(self, req):
        if 'TRAC_ADMIN' in req.perm('portfolio'):
            yield 'portfolio', 'Portfolio', 'settings', 'Settings'

    def render_admin_panel(self, req, cat, page, path_info, user = 'anonymous'):
        req.perm(Resource('portfolio')).require('TRAC_ADMIN')
        data = {}
        if req.method == 'POST':
            submit = req.args.get('submit').strip()
            if submit == 'Add':
                name = req.args.get('name').strip()
                description = req.args.get('description').strip()
                sql = ("INSERT INTO invest.portfolios "
                       "(name, description, createtime, user) "
                       "VALUES('{}', '{}', now(), '{}')"
                      ).format(name, description, user)
                self.env.db_transaction(sql)
                add_notice(req, 'Portfolio has been added.')
            elif submit == 'Remove':
                open = 0
                sels = req.args.getlist('sels')
                if sels is not None and len(sels) > 0:
                    for sel in sels:
                        sql = ("SELECT IFNULL(sum(abs(quantity) * case when type = 'Verkoop' then 1 else -1 end),0) as quantity "
                               "from invest.trades where type in ('Koop', 'Verkoop') and LOWER(portfolio) = (select LOWER(name) "
                               "from invest.portfolios where id = {})"
                              )
                        sql = sql.format(int(sel))
                        cursor = self.env.db_query(sql)
                        open += cursor[0][0] 
                        sql = 'DELETE FROM invest.portfolios WHERE id = {}'
                        sql = sql.format(int(sel))
                        self.env.db_transaction(sql)
                    add_notice(req, 'Portfolio has been deleted.')
                    if open != 0:
                        add_warning(req, 'There are open positions on this portfolio. Removing this portfolio will neither remove nor close these positions.')
            elif submit == 'Save':
                sel = req.args.get('sel').strip()
                name = req.args.get('name').strip()
                description = req.args.get('description').strip()
                sql = ("UPDATE invest.portfolios "
                       "SET name = '{}', description = '{}', "
                       "createtime = now(), user = '{}' "
                       "WHERE id = {}"
                      ).format(name, description, user, int(sel))
                self.env.db_transaction(sql)
                add_notice(req, 'Portfolio has been saved.')
        else:
            sel = req.args.get('sel')
            if sel is not None:
                sql = ("SELECT id, name, description, createtime, user "
                       "FROM invest.portfolios where id = {}"
                      ).format(int(sel))
                cursor = self.env.db_query(sql)
                if len(cursor) > 0:
                    data['view'] = 'detail'
                    data['sel'] = sel
                    data['name'] = cursor[0][1]
                    data['description'] = cursor[0][2]

        cursor = self.env.db_query(
                     "SELECT id, name, description, createtime, user "
                     "FROM invest.portfolios ORDER BY name"
                 )
        data['portfolios'] = [
            (row[0], row[1], row[2], row[3], row[4]) for row in cursor]
        chrome = Chrome(self.env)
        chrome.add_auto_preview(req)
        chrome.add_wiki_toolbars(req)
        return 'portfolio_admin.html', data, {}
