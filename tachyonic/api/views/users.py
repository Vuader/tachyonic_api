from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from tachyonic import app
from tachyonic import router
from tachyonic.neutrino import constants as const
from tachyonic.common.models import users
from tachyonic.common.driver import get_driver

from tachyonic.api.api import orm as api

log = logging.getLogger(__name__)


@app.resources()
class Users(object):
    def __init__(self):
        router.add(const.HTTP_GET,
                   '/v1/users',
                   self.get,
                   'users:view')
        router.add(const.HTTP_GET,
                   '/v1/user/{id}',
                   self.get,
                   'users:view')
        router.add(const.HTTP_POST,
                   '/v1/user',
                   self.post,
                   'users:admin')
        router.add(const.HTTP_PUT,
                   '/v1/user/{id}',
                   self.put,
                   'users:admin')
        router.add(const.HTTP_DELETE,
                   '/v1/user/{id}',
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
