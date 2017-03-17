from __future__ import absolute_import
from __future__ import unicode_literals

import logging

import tachyonic
from tachyonic.neutrino import constants as const
from tachyonic.common.models import users
from tachyonic.common.driver import get_driver

from tachyonic.api.api import orm as api

log = logging.getLogger(__name__)


@tachyonic.app.resources()
class Users(object):
    def __init__(self, app):
        app.router.add(const.HTTP_GET,
                       '/users',
                       self.get,
                       'users:view')
        app.router.add(const.HTTP_GET,
                       '/users/{id}',
                       self.get,
                       'users:view')
        app.router.add(const.HTTP_POST,
                       '/users',
                       self.post,
                       'users:admin')
        app.router.add(const.HTTP_PUT,
                       '/users/{id}',
                       self.put,
                       'users:admin')
        app.router.add(const.HTTP_DELETE,
                       '/users/{id}',
                       self.delete,
                       'users:admin')

    def get(self, req, resp, id=None):
        return api.get(users.Users, req, resp, id)

    def post(self, req, resp):
        driver = req.config.get('authentication').get('driver')
        driver = get_driver(driver)()
        return api.post(users.User, req,
                        callback=driver.create)

    def put(self, req, resp, id):
        driver = req.config.get('authentication').get('driver')
        driver = get_driver(driver)()
        response = api.put(users.User, req, id,
                           callback=driver.password)
        return response

    def delete(self, req, resp, id):
        driver = req.config.get('authentication').get('driver')
        driver = get_driver(driver)()
        return api.delete(users.User, req, id,
                          callback=driver.delete)
