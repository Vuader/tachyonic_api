from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from tachyonic.neutrino import constants as const
from tachyonic.neutrino.mysql import Mysql
from tachyonic.neutrino import exceptions

from tachyonic.api import auth

log = logging.getLogger(__name__)


class Token(object):
    def pre(self, req, resp):
        tenant = req.headers.get('X-Tenant')
        domain = req.headers.get('X-Domain', 'default')
        otp = req.headers.get('X-Otp', None)
        domain_id = auth.get_domain_id(domain)
        if tenant is not None:
            tenant_id = auth.get_tenant_id(tenant)
        else:
            tenant_id = None

        req.context['tenant_id'] = None
        req.context['domain_admin'] = False
        req.context['domain_id'] = None
        req.context['login'] = False
        req.context['token'] = None
        req.context['expire'] = None
        req.context['roles'] = []

        resp.headers['Content-Type'] = const.APPLICATION_JSON
        token = req.headers.get('X-Auth_Token')
        if token is not None:
            db = Mysql()
            sql = "SELECT * FROM token where token = %s"
            if otp is not None:
                sql += " AND otp = %s"
                sql += " AND token_expire > NOW()"
                result = db.execute(sql, (token, otp))
            else:
                sql += " AND otp is NULL"
                sql += " AND token_expire > NOW()"
                result = db.execute(sql, (token,))
            db.commit()
            if len(result) > 0:
                user_id = result[0]['user_id']
                req.context['user_id'] = user_id
                req.context['token'] = token

                roles = auth.get_user_roles(user_id)
                req.context['login'] = True
                db.execute("UPDATE token" +
                           " set token_expire =" +
                           " (DATE_ADD(NOW()" +
                           ", INTERVAL 1 HOUR))" +
                           " WHERE token = %s", (token,))
                db.commit()
            else:
                raise exceptions.HTTPError(const.HTTP_404, 'Authentication failed',
                                    'Token not found or expired')

            if auth.authenticate_user_domain(user_id, domain_id):
                req.context['domain_id'] = domain_id
                req.context['domain_admin'] = auth.get_user_domain_admin(user_id,
                                                                    domain_id)
                if req.context['domain_admin'] is True:
                    req.context['tenant_id'] = tenant_id
                else:
                    if tenant_id is not None:
                        if auth.authenticate_user_tenant(user_id, domain_id,
                                                    tenant_id):
                            req.context['tenant_id'] = tenant_id
                        else:
                            raise exceptions.HTTPForbidden("Access Denied", "Invalid"
                                                           + " Tenant")
            else:
                raise exceptions.HTTPForbidden("Access Denied", "Invalid Domain")

            for role in roles:
                if (role['domain_id'] == domain_id):
                    if (role['tenant_id'] is None or
                            role['tenant_id'] == tenant_id):
                        role_name = auth.get_role_name(role['role_id'])
                        req.context['roles'].append(role_name)
