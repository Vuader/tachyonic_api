import logging
import json
import datetime

from tachyonic import app
from tachyonic.neutrino.mysql import Mysql
from tachyonic import router
from tachyonic.common import constants as const
from tachyonic.common import exceptions
from tachyonic.common.imports import get_class
from tachyonic.api.models import tenants
from tachyonic.api.validate import enabled

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
        driver = req.config.get('tenants').get('driver')
        driver = get_class(driver)()
        return orm_api.get(tenants.Tenants, req, resp, tenant_id)

    def post(self, req, resp):
        enabled('create', app.config.get('tenants'))
        # TODO DRIVER CALLBACK LINK
        driver = req.config.get('tenants').get('driver')
        driver = get_class(driver)()
        return orm_api.post(tenants.Tenant, req, resp)

    def put(self, req, resp, tenant_id):
        enabled('update', app.config.get('tenants'))
        # TODO DRIVER CALLBACK LINK
        driver = req.config.get('tenants').get('driver')
        driver = get_class(driver)()
        return orm_api.put(tenants.Tenant, req, tenant_id)

    def delete(self, req, resp, tenant_id):
        enabled('update', app.config.get('tenants'))
        # TODO DRIVER CALLBACK LINK
        driver = req.config.get('tenants').get('driver')
        driver = get_class(driver)()
        return orm_api.delete(tenants.Tenant, req, tenant_id)
