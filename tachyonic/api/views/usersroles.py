from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import json
from collections import OrderedDict

from tachyonic import router
from tachyonic import app
from tachyonic.neutrino import constants as const
from tachyonic.neutrino.mysql import Mysql

from tachyonic.api import api
from tachyonic.api import auth

log = logging.getLogger(__name__)


@app.resources()
class UsersRoles(object):
    def __init__(self):
        router.add(const.HTTP_GET,
                   '/v1/user/roles',
                   self.get,
                   'users:view')
        router.add(const.HTTP_GET,
                   '/v1/user/roles/{user_id}',
                   self.get,
                   'users:view')
        router.add(const.HTTP_POST,
                   '/v1/user/role/{user_id}/{role}/{domain}',
                   self.post,
                   'users:admin')
        router.add(const.HTTP_POST,
                   '/v1/user/role/{user_id}/{role}/{domain}/{tenant}',
                   self.post,
                   'users:admin')
        router.add(const.HTTP_DELETE,
                   '/v1/user/role/{user_id}/{role}/{domain}',
                   self.delete,
                   'users:admin')
        router.add(const.HTTP_DELETE,
                   '/v1/user/role/{user_id}/{role}/{domain}/{tenant}',
                   self.delete,
                   'users:admin')

    def get(self, req, resp, user_id):
        db = Mysql()
        user = api.sql_get_query('user', req, resp, user_id)
        response = db.execute("SELECT * FROM user_role WHERE user_id = %s",
                              (user_id,))
        roles = []
        for role in response:
            r = OrderedDict()
            r['user_id'] = user[0]['id']
            r['username'] = user[0]['username']
            r['role_id'] = role['role_id']
            r['role_name'] = auth.get_role_name(role['role_id'])
            r['domain_id'] = role['domain_id']
            r['domain_name'] = auth.get_domain_name(role['domain_id'])
            r['tenant_id'] = role['tenant_id']
            r['tenant_name'] = auth.get_tenant_name(role['tenant_id'])
            roles.append(r)

        return json.dumps(roles, indent=4)

    def post(self, req, resp, user_id, role, domain, tenant=None):
        user = api.sql_get_query('user', req, resp, user_id)
        domain_id = auth.get_domain_id(domain)
        role_id = auth.get_role_id(role)
        if tenant is not None:
            tenant_id = auth.get_tenant_id(tenant)
        else:
            tenant_id = None
        db = Mysql()
        values = []
        sql = "SELECT * FROM user_role"
        sql += " WHERE user_id = %s"
        sql += " AND role_id = %s"
        sql += " AND domain_id = %s"
        values.append(user_id)
        values.append(role_id)
        values.append(domain_id)

        if tenant is not None:
            sql += " and tenant_id = %s"
            values.append(tenant_id)

        c_role = db.execute(sql, values)
        if len(c_role) == 0 and len(user) > 0:
            sql = "INSERT INTO user_role"
            sql += " (id, role_id, domain_id, tenant_id, user_id)"
            sql += " values"
            sql += " (uuid(), %s, %s, %s, %s)"
            db.execute(sql, (role_id, domain_id, tenant_id, user_id))
            db.commit()

    def delete(self, req, resp, user_id, role, domain, tenant=None):
        user = api.sql_get_query('user', req, resp, user_id)
        domain_id = auth.get_domain_id(domain)
        role_id = auth.get_role_id(role)
        if tenant is not None:
            tenant_id = auth.get_tenant_id(tenant)
        else:
            tenant_id = None
        db = Mysql()

        if len(user) > 0:
            sql = "DELETE FROM user_role"
            sql += " WHERE user_id = %s"
            sql += " AND role_id = %s"
            sql += " AND domain_id = %s"
            values = []
            values.append(user_id)
            values.append(role_id)
            values.append(domain_id)

            if tenant is not None:
                sql += " and tenant_id = %s"
                values.append(tenant_id)

            db.execute(sql, values)
            db.commit()
