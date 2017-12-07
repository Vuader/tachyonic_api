# -*- coding: utf-8 -*-
# Copyright (c) 2017, Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
import json
import datetime

from tachyonic.neutrino import constants as const
from tachyonic.neutrino import exceptions
from tachyonic.neutrino.wsgi import app
from tachyonic.neutrino.wsgi import router
from tachyonic.neutrino.mysql import Mysql
from tachyonic.neutrino.imports import get_class

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
