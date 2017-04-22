from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import json

from tachyonic import router
from tachyonic import app
from tachyonic.common import constants as const

log = logging.getLogger(__name__)


@app.resources()
class Index(object):
    def __init__(self):
        router.add(const.HTTP_GET, '/', self.index, 'tachyonic:public')

    def index(self, req, resp):
        resources = {}
        routes = req.router.routes
        site = req.get_app_url()
        resources['local'] = {}
        resources['external'] = {}
        local = resources['local']
        external = resources['external']
        for r in routes:
            r_method, r_uri, r_obj, r_name = r
            if req.policy.validate(r_name):
                href = "%s/%s" % (site, r_uri)
                method = {}
                method[r_method] = r_name
                if href in resources:
                    local[href]['methods'].append(method)
                else:
                    local[href] = {}
                    local[href]['methods'] = []
                    local[href]['methods'].append(method)

        for endpoint in app.config.getitems('endpoints'):
            name, href = endpoint
            external[name] = href

        return json.dumps(resources, indent=4)
