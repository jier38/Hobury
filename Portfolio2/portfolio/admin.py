# -*- coding: utf-8 -*-
"""
TracFullBlog admin panel for some settings related to the plugin.

License: BSD

(c) 2007 ::: www.CodeResort.com - BV Network AS (simon-code@bvnetwork.no)
"""

from trac.core import *
from trac.admin import IAdminPanelProvider
from trac.resource import Resource
from trac.web.chrome import Chrome, add_warning, add_notice


class PortfolioPanel(Component):
    """Admin panel for settings related to FullBlog plugin."""

    implements(IAdminPanelProvider)

    # IAdminPageProvider

    def get_admin_panels(self, req):
        if 'TRAC_ADMIN' in req.perm('portfolio'):
            yield 'portfolio', 'Portfolio', 'settings', 'Settings'

    def render_admin_panel(self, req, cat, page, path_info, user='anonymous'):
        req.perm(Resource('portfolio')).require('TRAC_ADMIN')

        data = {}

        if req.method == "POST":
            submit = req.args.get('submit').strip()
            if submit == 'Add':
                name = req.args.get('name').strip()
                description = req.args.get('description').strip()
                sql = "INSERT INTO portfolios (name, description, createtime, user) " \
                      " VALUES('{}','{}',now(),'{}')".format(
                          name, description, user)
                self.env.db_transaction(sql)
                add_notice(req, 'Portfolio has been added.')
            elif submit == 'Remove':
                sels = req.args.getlist('sels')
                if sels is not None and len(sels) > 0:
                    for sel in sels:
                        sql = "DELETE FROM portfolios WHERE id ={}".format(
                            int(sel))
                        self.env.db_transaction(sql)
                    add_notice(req, 'Portfolio has been deleted.')
            elif submit == 'Save':
                sel = req.args.get('sel').strip()
                name = req.args.get('name').strip()
                description = req.args.get('description').strip()
                sql = "UPDATE portfolios SET name='{}', description='{}', createtime=now(), user='{}' " \
                      " WHERE id={}".format(name, description, user, int(sel))
                self.env.db_transaction(sql)
                add_notice(req, 'Portfolio has been saved.')
        else:
            sel = req.args.get('sel')
            if sel is not None:
                sql = "SELECT id, name, description, createtime, user FROM portfolios where id={}".format(
                    int(sel))
                cursor = self.env.db_query(sql)
                if len(cursor) > 0:
                    data['view'] = 'detail'
                    data['sel'] = sel
                    data['name'] = cursor[0][1]
                    data['description'] = cursor[0][2]

        cursor = self.env.db_query(
            "SELECT id, name, description, createtime, user FROM portfolios ORDER BY name")
        data['portfolios'] = [
            (row[0], row[1], row[2], row[3], row[4]) for row in cursor]

        chrome = Chrome(self.env)
        chrome.add_auto_preview(req)
        chrome.add_wiki_toolbars(req)

        return 'portfolio_admin.html', data, {}
