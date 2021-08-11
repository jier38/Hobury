import re
from datetime import datetime
from trac.core import *
from trac.util.html import html
from trac.web.api import IRequestHandler, HTTPNotFound
from trac.web.chrome import Chrome, INavigationContributor, 
	add_warning, add_notice
from trac.perm import IPermissionRequestor


class Charts(Component):

    implements(IRequestHandler, INavigationContributor, 
		IPermissionRequestor)

    # INavigationContributor methods

    def get_active_navigation_item(self, req):
        return 'charts'

    def get_navigation_items(self, req):
        if 'CHARTS_VIEW' in req.perm:
            yield ('mainnav', 'charts', html.a('Charts', 
				href=req.href.charts()))

    # IRequstHandler methods

    def match_request(self, req):
        return req.path_info.find('/charts') == 0

    def process_request(self, req):
        data = {}
        return 'charts.html', data, {}

    def get_permission_actions(self):
        view = 'CHARTS_VIEW'
        return [view]
