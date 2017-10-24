import logging

from tachyonic import app
from tachyonic import router
from tachyonic.common import constants as const
from tachyonic.api.models import domains

from tachyonic.api.api import orm as api

log = logging.getLogger(__name__)


@app.resources()
class Domains(object):
    def __init__(self):
        router.add(const.HTTP_GET,
                   '/v1/domains',
                   self.get,
                   'tachyonic:login')
        router.add(const.HTTP_GET,
                  '/v1/domain/{id}',
                   self.get,
                   'domains:admin')
        router.add(const.HTTP_POST,
                   '/v1/domain',
                   self.post,
                   'domains:admin')
        router.add(const.HTTP_PUT,
                   '/v1/domain/{id}',
                   self.put,
                   'domains:admin')
        router.add(const.HTTP_DELETE,
                   '/v1/domain/{id}',
                   self.delete,
                   'domains:admin')

    def get(self, req, resp, id=None):
        return api.get(domains.Domains, req, resp, id)

    def post(self, req, resp):
        return api.post(domains.Domain, req)

    def put(self, req, resp, id):
        return api.put(domains.Domain, req, id)

    def delete(self, req, resp, id):
        return api.delete(domains.Domain, req, id)
