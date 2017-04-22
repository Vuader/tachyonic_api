from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import json
from collections import OrderedDict

from tachyonic import router
from tachyonic import app
from tachyonic.common import constants as const
from tachyonic.common import exceptions
from tachyonic.neutrino.mysql import Mysql

from tachyonic.api.api import sql as api
from tachyonic.api import auth

log = logging.getLogger(__name__)


@app.resources()
class UsersRoles(object):
    def __init__(self):
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
        user = api.get_query('user', req, resp, user_id)
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
        user = api.get_query('user', req, resp, user_id)
        domain_id = auth.get_domain_id(domain)
        domain_name = auth.get_domain_name(domain)
        role_id = auth.get_role_id(role)
        if tenant is not None:
            tenant_id = auth.get_tenant_id(tenant)
        else:
            tenant_id = None
        db = Mysql()
        values = []

        # SECURITY CHECKS
        if req.context['is_root'] is True:
            pass
        else:
            if req.context['domain_admin'] is True:
                if domain_id != req.context['domain_id']:
                    raise exceptions.HTTPForbidden("Role Assignment",
                                                   "Not within domain \"%s\"" % domain_name)
            else:
                if domain_id != req.context['domain_id']:
                    raise exceptions.HTTPForbidden("Role Assignment",
                                                   "Not within domain \"%s\"" % domain_name)
                if tenant_id is None:
                    raise exceptions.HTTPForbidden("Role Assignment",
                                                   "Not domain \"%s\" admin" % domain_name)
                sql = "SELECT * FROM user_role"
                sql += " WHERE user_id = %s"
                sql += " AND tenant_id = %s"
                sql += " AND domain_id = %s"
                result_role_check = db.execute(sql, (req.context['user_id'],
                                                     tenant_id,
                                                     domain_id))
                sql = "SELECT * FROM tenant"
                sql += " WHERE tenant_id = %s"
                sql += " AND domain_id = %s"
                result_sub_tenant_check = db.execute(sql,
                                                     (req.context['tenant_id'],
                                                      req.context['domain_id']))
                db.commit()
                if (len(result_role_check) == 0 and
                        len(result_sub_tenant_check) == 0):
                    raise exceptions.HTTPForbidden("Role Assignment",
                                                   "Access Denied to Tenant")

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
        else:
            sql += " and tenant_id is null"

        c_role = db.execute(sql, values)
        if len(c_role) == 0 and len(user) > 0:
            sql = "INSERT INTO user_role"
            sql += " (id, role_id, domain_id, tenant_id, user_id)"
            sql += " values"
            sql += " (uuid(), %s, %s, %s, %s)"
            db.execute(sql, (role_id, domain_id, tenant_id, user_id))
            db.commit()

    def delete(self, req, resp, user_id, role, domain, tenant=None):
        user = api.get_query('user', req, resp, user_id)
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
            else:
                sql += " and tenant_id is null"

            db.execute(sql, values)
            db.commit()
