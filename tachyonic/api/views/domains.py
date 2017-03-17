from __future__ import absolute_import
from __future__ import unicode_literals

import logging

import tachyonic
from tachyonic.neutrino import constants as const
from tachyonic.common.models import domains

from tachyonic.api.api import orm as api

log = logging.getLogger(__name__)


@tachyonic.app.resources()
class Domains(object):
    def __init__(self, app):
        app.router.add(const.HTTP_GET,
                       '/domains',
                       self.get,
                       'tachyonic:login')
        app.router.add(const.HTTP_GET,
                       '/domains/{id}',
                       self.get,
                       'domains:admin')
        app.router.add(const.HTTP_POST,
                       '/domains',
                       self.post,
                       'domains:admin')
        app.router.add(const.HTTP_PUT,
                       '/domains/{id}',
                       self.put,
                       'domains:admin')
        app.router.add(const.HTTP_DELETE,
                       '/domains/{id}',
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
