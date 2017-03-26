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
from tachyonic.common.models import tenants

from tachyonic.api.api import orm as orm_api

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
            # TODO DRIVER CALLBACK LINK
            driver = req.config.get('tenant').get('driver')
            driver = get_driver(driver)()
            return orm_api.get(tenants.Tenants, req, resp, tenant_id,
                               ignore_tenant=True)
        else:
            raise exceptions.HTTPNotFound("Not Found", "Tenant not specified")
