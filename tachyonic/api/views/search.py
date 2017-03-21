from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import json
import datetime

from tachyonic import app
from tachyonic import router
from tachyonic.neutrino import constants as const
from tachyonic.neutrino import exceptions
from tachyonic.common.driver import get_driver

from tachyonic.api import tenant

log = logging.getLogger(__name__)


@app.resources()
class Search(object):
    def __init__(self):
        router.add(const.HTTP_GET,
                   '/v1/search',
                   self.get,
                   'tachyonic:login')

    def get(self, req, resp):
        driver = req.config.get('tenant').get('driver')
        driver = get_driver(driver)()

        domain_id = req.context.get('domain_id')
        if domain_id is None:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")
        search = req.headers.get('X-Search')
        if search is not None:
            records, data = driver.retrieve(domain_id,
                                            None,
                                            search,
                                            "name asc",
                                            None,
                                            None)
            for d in data:
                if 'external_id' in d:
                    d['id'] = tenant.get_local_id(domain_id, d['external_id'])

            resp.headers['X-Total-Rows'] = records
            resp.headers['X-Filtered-Rows'] = records

            for row in data:
                for key in row:
                    if isinstance(row[key],datetime.datetime):
                        row[key] = row[key].strftime("%Y/%m/%d %H:%M:%S")
        else:
            data = []

        return json.dumps(data, indent=4)
