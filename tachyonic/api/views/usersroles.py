# -*- coding: utf-8 -*-
# Copyright (c) 2017, Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
import json
from collections import OrderedDict

from tachyonic.neutrino.wsgi import router
from tachyonic.neutrino.wsgi import app
from tachyonic.neutrino import constants as const
from tachyonic.neutrino import exceptions
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
