import logging

from tachyonic.neutrino import constants as const
from tachyonic.neutrino.imports import get_class
from tachyonic.neutrino.wsgi import app
from tachyonic.neutrino.wsgi import router

from tachyonic.api.models import users
from tachyonic.neutrino import exceptions
from tachyonic.api.validate import enabled
from tachyonic.api.api import orm as api
from tachyonic.neutrino.mysql import Mysql

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
        enabled('create', app.config.get('users'))
        driver = req.config.get('users').get('driver')
        driver = get_class(driver)()
        return api.post(users.User, req,
                        callback=driver.create)

    def put(self, req, resp, id):
        enabled('update', app.config.get('users'))
        driver = req.config.get('users').get('driver')
        driver = get_class(driver)()
        # Verifying that User has Role assigned
        db = Mysql()
        user_role = db.execute("SELECT * FROM user_role WHERE user_id = %s",
                               (id,))
        if len(user_role) == 0:
            raise exceptions.HTTPBadRequest(title="Role Assigment",
                                            description="User has no role assigned")
        response = api.put(users.User, req, id,
                           callback=driver.password)
        return response

    def delete(self, req, resp, id):
        enabled('update', app.config.get('users'))
        driver = req.config.get('users').get('driver')
        driver = get_class(driver)()
        return api.delete(users.User, req, id,
                          callback=driver.delete)
