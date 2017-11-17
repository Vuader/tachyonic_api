import logging
import uuid
from collections import OrderedDict

from tachyonic import app
from tachyonic.neutrino.mysql import Mysql
from tachyonic.neutrino.password import valid as is_valid_password
from tachyonic.neutrino.password import hash as hash_password
from tachyonic.neutrino import exceptions

log = logging.getLogger(__name__)

class MysqlDriver(object):
    # Mandotory return true or false
    def authenticate(self, user_id, username, password, context):
        db = Mysql()
        sql = "SELECT * FROM user"
        sql += " WHERE id = %s"
        result = db.execute(sql, (user_id,))
        db.commit()
        if len(result) == 1:
            if is_valid_password(password, result[0]['password']):
                return True
        return False

    def create(self, context):
        if 'id' in context:
            user_id = context['id'].value()
            self.password(user_id, context)

    def password(self, user_id, context):
        db = Mysql()
        if ('password' in context
                and str(context['password']) != ''):
            password = hash_password(str(context['password']))
            sql = "UPDATE user"
            sql += " SET password = %s"
            sql += " WHERE id = %s"
            db.execute(sql, (password, user_id,))
            db.commit()

    def delete(self, id):
        pass


def get_user_roles(user_id):
    db = Mysql()
    result = db.execute("SELECT role_id,domain_id" +
                        ",tenant_id FROM user_role" +
                        " WHERE user_id = %s", (user_id,))
    db.commit()
    roles = []
    for r in result:
        role = OrderedDict()
        if is_domain_enabled(r['domain_id']):
            role['tenant_id'] = r['tenant_id']
            role['tenant_name'] = get_tenant_name(r['tenant_id'])
            role['domain_id'] = r['domain_id']
            role['domain_name'] = get_domain_name(r['domain_id'])
            role['role_id'] = r['role_id']
            role['role_name'] = get_role_name(r['role_id'])
            role['is_root'] = is_root(r['role_id'])
            roles.append(role)
    return roles

def is_domain_enabled(domain):
    db = Mysql()
    result = db.execute("SELECT id FROM domain" +
                        " WHERE (id = %s OR name = %s)" +
                        " AND enabled = 1",
                        (domain, domain))
    db.commit()
    if len(result) > 0:
        return True
    else:
        return False

def is_user_enabled(user_id):
    db = Mysql()
    result = db.execute("SELECT id FROM user" +
                        " WHERE (id = %s OR username = %s)" +
                        " AND enabled = 1",
                        (user_id, user_id))
    db.commit()
    if len(result) > 0:
        return True
    else:
        return False

def is_user_tenant_enabled(user_id):
    db = Mysql()
    result = db.execute("SELECT tenant_id FROM user" +
                        " WHERE (id = %s OR username = %s)" +
                        " AND enabled = 1 and tenant_id is not null",
                        (user_id, user_id))
    db.commit()
    if len(result) > 0:
        tenant_id = result[0]['tenant_id']
        return is_tenant_enabled(tenant_id)
    else:
        return True

def is_tenant_enabled(tenant):
    db = Mysql()
    result = db.execute("SELECT id FROM tenant" +
                        " WHERE (id = %s OR name = %s)" +
                        " AND enabled = 1",
                        (tenant, tenant))
    db.commit()
    if len(result) > 0:
        return True
    else:
        return False

def get_domain_id(domain):
    db = Mysql()
    result = db.execute("SELECT id FROM domain" +
                        " WHERE id = %s OR name = %s",
                        (domain, domain))
    db.commit()
    if len(result) > 0:
        return result[0]['id']
    else:
        raise exceptions.HTTPNotFound("Domain not found: %s" % (domain,))


def get_domain_name(domain):
    db = Mysql()
    result = db.execute("SELECT name FROM domain" +
                        " WHERE id = %s OR name = %s",
                        (domain, domain))
    if len(result) > 0:
        return result[0]['name']
    else:
        return None


def get_tenant_name(tenant):
    db = Mysql()
    result = db.execute("SELECT name FROM tenant" +
                        " WHERE id = %s OR name = %s",
                        (tenant, tenant))
    if len(result) > 0:
        return result[0]['name']
    else:
        return None


def get_external_id(tenant):
    db = Mysql()
    result = db.execute("SELECT external_id FROM tenant" +
                        " WHERE id = %s OR name = %s",
                        (tenant, tenant))
    db.commit()
    if len(result) > 0:
        return result[0]['external_id']
    else:
        raise exceptions.HTTPNotFound("Tenant not found: %s" % (tenant,))

def get_tenant_id(tenant):
    db = Mysql()
    result = db.execute("SELECT id FROM tenant" +
                        " WHERE id = %s OR name = %s",
                        (tenant, tenant))
    db.commit()
    if len(result) > 0:
        return result[0]['id']
    else:
        raise exceptions.HTTPNotFound("Tenant not found: %s" % (tenant,))


def get_role_name(role):
    db = Mysql()
    result = db.execute("SELECT name FROM role" +
                        " WHERE id = %s OR name = %s",
                        (role, role))
    db.commit()
    if len(result) > 0:
        return result[0]['name']
    else:
        return None


def is_root(role):
    db = Mysql()
    result = db.execute("SELECT root FROM role" +
                        " WHERE (id = %s OR name = %s) and root = 'True'",
                        (role, role))
    db.commit()
    if len(result) > 0:
        return True
    else:
        return False

def get_role_id(role):
    db = Mysql()
    result = db.execute("SELECT id FROM role" +
                        " WHERE id = %s OR name = %s",
                        (role, role))
    db.commit()
    if len(result) > 0:
        return result[0]['id']
    else:
        raise exceptions.HTTPNotFound("Role not found: %s" % (role,))

def get_user_domain_admin(user_id, domain_id):
    db = Mysql()
    result = db.execute("SELECT domain_id,tenant_id" +
                        " FROM user_role WHERE user_id = %s" +
                        " AND domain_id = %s" +
                        " AND tenant_id is NULL",
                        (user_id, domain_id))
    db.commit()
    if len(result) > 0:
        return True
    else:
        return False


def get_user_domains(user_id):
    db = Mysql()
    sql_domains_result = db.execute("SELECT domain_id" +
                                    " FROM user_role WHERE user_id = %s" +
                                    " GROUP BY domain_id", (user_id,))
    result = []
    for sql_domain in sql_domains_result:
        domain = {}
        domain_id = sql_domain['domain_id']
        sql_domain_name_result = db.execute("SELECT name FROM domain" +
                                            " WHERE id = %s", (domain_id,))
        name = sql_domain_name_result[0]['name']
        if is_domain_enabled(domain_id):
            domain['domain_id'] = domain_id
            domain['domain_name'] = name
            domain['domain_admin'] = get_user_domain_admin(user_id, domain_id)
            result.append(domain)
    return result


def authenticate_user_domain(user_id, domain_id):
    if domain_id is None:
        return False

    user_domains = get_user_domains(user_id)
    for user_domain in user_domains:
        if user_domain['domain_id'] == domain_id:
            if is_domain_enabled(domain_id):
                return True
            else:
                return False
    return False


def authenticate_user_tenant(user_id, domain_id, tenant_id):
    if tenant_id is None:
        return False

    def sub_check(sub_id):
        db = Mysql()
        sql = "SELECT * FROM tenant"
        sql += " WHERE id = %s"
        sql += " AND domain_id = %s"
        result = db.execute(sql,
                            (sub_id,
                             domain_id))
        if len(result) == 1:
            role = db.execute("SELECT * FROM user_role" +
                              " WHERE user_id = %s AND domain_id = %s" +
                              " AND tenant_id = %s",
                              (user_id, domain_id, result[0]['tenant_id']))
            if len(role) > 0:
                return True
            else:
                return sub_check(result['tenant_id'])
        else:
            return False


    db = Mysql()
    result = db.execute("SELECT * FROM user_role" +
                        " WHERE user_id = %s AND domain_id = %s" +
                        " AND tenant_id = %s",
                        (user_id, domain_id, tenant_id))
    db.commit()
    if len(result) > 0:
        return True
    else:
        return sub_check(tenant_id)

    return False


def get_username(username):
    db = Mysql()
    result = db.execute("SELECT username FROM user" +
                        " WHERE id = %s OR username = %s",
                        (username, username))
    db.commit()
    if len(result) > 0:
        return result[0]['username']
    else:
        return None


def get_lastlogin(username):
    db = Mysql()
    result = db.execute("SELECT last_login FROM user" +
                        " WHERE id = %s OR username = %s",
                        (username, username))
    db.commit()
    if len(result) > 0:
        return result[0]['last_login']
    else:
        return None

