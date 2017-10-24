import logging

from tachyonic import app
from tachyonic import router
from tachyonic.common import constants as const
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
