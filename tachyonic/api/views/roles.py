from __future__ import absolute_import
from __future__ import unicode_literals

import logging

import tachyonic
from tachyonic.neutrino import constants as const

from tachyonic.common.models import roles
from tachyonic.api.api import orm as api

log = logging.getLogger(__name__)


@tachyonic.app.resources()
class Roles(object):
    def __init__(self, app):
        app.router.add(const.HTTP_GET,
                       '/roles',
                       self.get,
                       'tachyonic:login')
        app.router.add(const.HTTP_GET,
                       '/roles/{id}',
                       self.get,
                       'roles:admin')
        app.router.add(const.HTTP_POST,
                       '/roles',
                       self.post,
                       'roles:admin')
        app.router.add(const.HTTP_PUT,
                       '/roles/{id}',
                       self.put,
                       'roles:admin')
        app.router.add(const.HTTP_DELETE,
                       '/roles/{id}',
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
