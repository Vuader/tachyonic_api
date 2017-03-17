from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import json

import tachyonic
from tachyonic.neutrino import constants as const

log = logging.getLogger(__name__)


@tachyonic.app.resources()
class Index(object):
    def __init__(self, app):
        app.router.add(const.HTTP_GET, '/', self.index, 'tachyonic:public')

    def index(self, req, resp):
        resources = {}
        routes = req.router.routes
        site = req.get_app_url()
        for r in routes:
            r_method, r_uri, r_obj, r_name = r
            if req.policy.validate(r_name):
                url = "%s/%s" % (site, r_uri)
                method = {}
                method[r_method] = r_name
                if url in resources:
                    resources[url]['methods'].append(method)
                else:
                    resources[url] = {}
                    resources[url]['methods'] = []
                    resources[url]['methods'].append(method)
        return json.dumps(resources, indent=4)
