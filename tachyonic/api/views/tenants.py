from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import json
import datetime

from tachyonic import app
from tachyonic.neutrino.mysql import Mysql
from tachyonic import router
from tachyonic.neutrino import constants as const
from tachyonic.neutrino import exceptions
from tachyonic.common.driver import get_driver
from tachyonic.common.models import tenants

from tachyonic.api.api import orm as orm_api

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
        # TODO DRIVER CALLBACK LINK
        driver = req.config.get('tenant').get('driver')
        driver = get_driver(driver)()
        return orm_api.get(tenants.Tenants, req, resp, tenant_id)

    def post(self, req, resp):
        # TODO DRIVER CALLBACK LINK
        driver = req.config.get('tenant').get('driver')
        driver = get_driver(driver)()
        return orm_api.post(tenants.Tenant, req, resp)

    def put(self, req, resp, tenant_id):
        # TODO DRIVER CALLBACK LINK
        driver = req.config.get('tenant').get('driver')
        driver = get_driver(driver)()
        return orm_api.put(tenants.Tenant, req, tenant_id)

    def delete(self, req, resp, tenant_id):
        # TODO DRIVER CALLBACK LINK
        driver = req.config.get('tenant').get('driver')
        driver = get_driver(driver)()
        return orm_api.delete(tenants.Tenant, req, tenant_id)
