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
class Tenant(object):
    def __init__(self):
        router.add(const.HTTP_GET,
                   '/v1/tenant',
                   self.get,
                   'tachyonic:login')

    def get(self, req, resp):
        tenant_id = req.context['tenant_id']
        if tenant_id is not None:
            driver = req.config.get('tenant').get('driver')
            driver = get_driver(driver)()

            domain_id = req.context.get('domain_id')
            if domain_id is None:
                raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")

            records, data = driver.retrieve(domain_id, tenant_id,
                                            None, None, None, None)
            for d in data:
                if 'external_id' in d:
                    d['id'] = tenant.get_local_id(domain_id, d['external_id'])

            resp.headers['X-Total-Rows'] = records
            resp.headers['X-Filtered-Rows'] = records

            for row in data:
                for key in row:
                    if isinstance(row[key],datetime.datetime):
                        row[key] = row[key].strftime("%Y/%m/%d %H:%M:%S")
                    if key == "enabled":
                        if row[key] == 0:
                            row[key] = False
                        elif row[key] == 1:
                            row[key] = True


            if len(data) == 1:
                data = data[0]
                return json.dumps(data, indent=4)
            else:
                raise exceptions.HTTPNotFound("Not Found", "Tenant not found")
        else:
            raise exceptions.HTTPNotFound("Not Found", "Tenant not specified")
