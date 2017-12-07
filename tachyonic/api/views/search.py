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
import copy

from tachyonic.neutrino import constants as const
from tachyonic.neutrino import exceptions
from tachyonic.neutrino.wsgi import app
from tachyonic.neutrino.wsgi import router
from tachyonic.neutrino.imports import get_class

from tachyonic.api.api import sql
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
        driver = req.config.get('tenants').get('driver')
        driver = get_class(driver)()

        domain_id = req.context.get('domain_id')

        if domain_id is None:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")

        result = sql.get_query('tenant', req, resp,
                                       req.context['tenant_id'],
                                       ignore_tenant=True)
        if len(result) == 0:
            result = sql.get_query('tenant', req, resp, None)
        for t in result:
            if t['external_id'] is not None:
                q = driver.retrieve(domain_id, t['external_id'])
                t.update(q)

        for row in result:
            for key in row:
                if isinstance(row[key],datetime.datetime):
                    row[key] = row[key].strftime("%Y/%m/%d %H:%M:%S")
                if key == "enabled":
                    if row[key] == 0:
                        row[key] = False
                    elif row[key] == 1:
                        row[key] = True


        return json.dumps(result, indent=4)
