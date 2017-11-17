import logging
import json
import uuid
from collections import OrderedDict

from tachyonic import app
from tachyonic import router

from tachyonic.neutrino import constants as const
from tachyonic.neutrino.mysql import Mysql
from tachyonic.neutrino import exceptions
from tachyonic.neutrino.ids import random_id
from tachyonic.neutrino.imports import get_class

from tachyonic.api import auth

log = logging.getLogger(__name__)


@app.resources()
class Authenticate(object):
    def __init__(self):
        router.add(const.HTTP_POST, '/v1/token', self.post, 'tachyonic:public')
        router.add(const.HTTP_GET, '/v1/token', self.get, 'tachyonic:public')

    def _new_token(self, user_id, expire=1, extra=None):
        db = Mysql()
        token_id = random_id(64)
        extra = json.dumps(extra)
        db.execute("UPDATE user set last_login = now()" +
                   "  WHERE id = %s", (user_id,))

        db.execute("INSERT INTO token" +
                   " (id,user_id,token,token_expire,extra)" +
                   " VALUES (uuid(),%s, %s, DATE_ADD(NOW()" +
                   ", INTERVAL %s HOUR), %s)",
                   (user_id, token_id, expire, extra))

        result = db.execute("SELECT token_expire" +
                            " FROM token WHERE token = %s",
                            (token_id,))

        session_expire = result[0]['token_expire']

        db.commit()

        return [token_id, session_expire]

    def get(self, req, resp):
        if 'user_id' in req.context:
            db = Mysql()
            sql = "SELECT * FROM user"
            sql += " WHERE id = %s and enabled = 1"
            result = db.execute(sql, (req.context['user_id'],))
            db.commit()
            if len(result) == 1:
                creds = OrderedDict()
                user_id = result[0]['id']
                creds['username'] = result[0]['username']
                creds['email'] = result[0]['email']
                creds['token'] = req.context['token']
                sql = "SELECT * FROM token where token = %s"
                token_result = db.execute(sql, (req.context['token'],))
                creds['expire'] = token_result[0]['token_expire'].strftime("%Y/%m/%d %H:%M:%S")
                creds['roles'] = auth.get_user_roles(user_id)
                creds['roles'] = auth.get_user_roles(user_id)
                creds['extra'] = req.context['extra']
                creds['tenant_id'] = req.context['tenant_id']
                creds['external_id'] = req.context['external_id']
                return json.dumps(creds, indent=4)
            else:
                return "{}"
        else:
            return "{}"

    def post(self, req, resp):
        db = Mysql()
        creds = req.json()
        usern = creds.get('username', '')
        passw = creds.get('password', '')
        domain = req.headers.get('X-Domain', 'default')
        sql = "DELETE FROM token WHERE token_expire < NOW()"
        db.execute(sql)
        domain_id = auth.get_domain_id(domain)
        sql = "SELECT * FROM user"
        sql += " WHERE username = %s and domain_id = %s"
        result = db.execute(sql, (usern, domain_id))
        db.commit()
        driver = req.config.get('users').get('driver')
        driver = get_class(driver)()
        extra = OrderedDict()
        if len(result) == 1:
            user_id = result[0]['id']
        else:
            user_id = None
        if driver.authenticate(user_id, usern, passw, extra):
            if user_id is None:
                user_id = str(uuid.uuid4())
                sql = "INSERT INTO user"
                sql += " (id, username, domain_id)"
                sql += " VALUES"
                sql += " (%s, %s, %s)"
                db.execute(sql, (user_id, usern, domain_id))
                db.commit()
                username = usern
                email = None
            else:
                username = result[0]['username']
                email = result[0]['email']
            if hasattr(driver, 'assignments'):
                driver.assignments(user_id, domain_id)
            creds = OrderedDict()
            creds['username'] = username
            creds['email'] = email
            token, expire = self._new_token(user_id, extra=extra)
            creds['token'] = token
            creds['expire'] = expire.strftime("%Y/%m/%d %H:%M:%S")
            creds['roles'] = auth.get_user_roles(user_id)
            creds['extra'] = extra
            return json.dumps(creds, indent=4)
        else:
            raise exceptions.HTTPError(const.HTTP_404, 'Authentication failed',
                                'Could not validate username' +
                                ' and password credentials')
