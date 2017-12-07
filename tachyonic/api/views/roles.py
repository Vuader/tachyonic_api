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

from tachyonic.neutrino import constants as const
from tachyonic.neutrino.wsgi import app
from tachyonic.neutrino.wsgi import router

from tachyonic.api.models import roles
from tachyonic.api.api import orm as api

log = logging.getLogger(__name__)


@app.resources()
class Roles(object):
    def __init__(self):
        router.add(const.HTTP_GET,
                   '/v1/roles',
                   self.get,
                   'tachyonic:login')
        router.add(const.HTTP_GET,
                  '/v1/role/{id}',
                   self.get,
                   'roles:admin')
        router.add(const.HTTP_POST,
                   '/v1/role',
                   self.post,
                   'roles:admin')
        router.add(const.HTTP_PUT,
                   '/v1/role/{id}',
                   self.put,
                   'roles:admin')
        router.add(const.HTTP_DELETE,
                   '/v1/role/{id}',
                   self.delete,
                   'roles:admin')

    def get(self, req, resp, id=None):
        return api.get(roles.Roles, req, resp, id)

    def post(self, req, resp):
        return api.post(roles.Role, req)

    def put(self, req, resp, id):
        return api.put(roles.Role, req, id)

    def delete(self, req, resp, id):
        return api.delete(roles.Role, req, id)
