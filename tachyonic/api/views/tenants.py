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
class Tenants(object):
    def __init__(self):
        router.add(const.HTTP_GET,
                   '/v1/tenants',
                   self.get,
                   'tenants:view')
        router.add(const.HTTP_GET,
                   '/v1/tenant/{tenant_id}',
                   self.get,
                   'tenants:view')
        router.add(const.HTTP_POST,
                   '/v1/tenant',
                   self.post,
                   'tenants:admin')
        router.add(const.HTTP_PUT,
                   '/v1/tenant/{tenant_id}',
                   self.put,
                   'tenants:admin')
        router.add(const.HTTP_DELETE,
                   '/v1/tenant/{tenant_id}',
                   self.delete,
                   'tenants:admin')

    def get(self, req, resp, tenant_id=None):
        driver = req.config.get('tenant').get('driver')
        driver = get_driver(driver)()

        domain_id = req.context.get('domain_id')
        if domain_id is None:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")
        start = req.headers.get('X-Pager-Start')
        limit = req.headers.get('X-Pager-Limit')
        order = req.headers.get('X-Order-By')
        search = req.headers.get('X-Search')

        records, data = driver.retrieve(domain_id, tenant_id,
                                        search, order, start, limit)
        for d in data:
            if 'external_id' in d:
                d['id'] = tenant.get_local_id(domain_id, d['external_id'])

        resp.headers['X-Total-Rows'] = records
        resp.headers['X-Filtered-Rows'] = records

        for row in data:
            for key in row:
                if isinstance(row[key],datetime.datetime):
                    row[key] = row[key].strftime("%Y/%m/%d %H:%M:%S")


        if tenant_id is not None:
            if len(data) == 1:
                data = data[0]
                return json.dumps(data, indent=4)
            else:
                raise exceptions.HTTPNotFound("Not Found", "Tenant not found")
        else:
            return json.dumps(data, indent=4)

    def post(self, req, resp):
        driver = req.config.get('tenant').get('driver')
        driver = get_driver(driver)()
        obj = json.loads(req.read())
        domain_id = req.context.get('domain_id')
        if domain_id is None:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")
        if 'id' in obj:
            del obj['id']
        obj['domain_id'] = domain_id
        result = driver.create(obj)
        if 'id' in result:
            tenant_id = result['id']
        elif 'external_id' in result:
            external_id = result['external_id']
            tenant_id = tenant.get_local_id(domain_id, external_id)
        else:
            pass
        result['domain_id'] = domain_id
        result['id'] = tenant_id
        return json.dumps(result, indent=4)

    def put(self, req, resp, tenant_id):
        driver = req.config.get('tenant').get('driver')
        driver = get_driver(driver)()
        obj = json.loads(req.read())
        domain_id = req.context.get('domain_id')
        if domain_id is None:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")
        obj['domain_id'] = domain_id
        external_id = tenant.get_external_id(tenant_id)
        result = driver.update(external_id, obj)
        result['domain_id'] = domain_id
        result['id'] = tenant_id
        return json.dumps(result, indent=4)

    def delete(self, req, resp, tenant_id):
        driver = req.config.get('tenant').get('driver')
        driver = get_driver(driver)()
        domain_id = req.context.get('domain_id')
        if domain_id is None:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")
        result = driver.delete(domain_id, tenant_id)
        if result is True:
            return "{\"action\": \"success\"}"
        else:
            raise exceptions.HTTPNotFound("Not Found", "Object not found")
