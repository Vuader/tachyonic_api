from __future__ import absolute_import
from __future__ import unicode_literals

import uuid
import re
import logging

from tachyonic.api.mysql import Mysql
from tachyonic.neutrino import exceptions

log = logging.getLogger(__name__)


class MysqlDriver(object):
    def create(self, data):
        db = Mysql()
        if 'id' in data:
            del data['id']
        fields = []
        values = []
        values_str = []
        tenant_id = str(uuid.uuid4())
        fields.append('id')
        values.append(tenant_id)
        values_str.append('%s')
        for d in data:
            fields.append(d)
            values.append(data[d])
            values_str.append('%s')
        fields = ",".join(fields)
        values_str = ",".join(values_str)
        sql = "INSERT INTO tenant"
        sql += " (%s)" % (fields,)
        sql += " VALUES"
        sql += " (%s)" % (values_str,)
        db.execute(sql, values)
        data['id'] = tenant_id
        db.commit()
        return data

    def update(self, external_id, data):
        db = Mysql()
        if 'id' in data:
            del data['id']
        domain_id = data['domain_id']
        if 'domain_id' in data:
            del data['domain_id']
        sets = []
        values = []
        for f in data:
            sets.append("%s = %s" % (f, '%s'))
            values.append(data[f])
        values.append(domain_id)
        values.append(external_id)
        sets = ",".join(sets)
        data['external_id'] = external_id
        data['id'] = data
        sql = "UPDATE tenant"
        sql += " set %s" % (sets)
        sql += " WHERE domain_id = %s and external_id = %s"
        db.execute(sql, values)
        db.commit()
        return data

    def retrieve(self, domain_id, external_id):
        db = Mysql()
        sql_values = []
        sql_where = []
        sql_where.append("external_id = %s")
        sql_values.append(external_id)

        sql_where.append("domain_id = %s")
        sql_values.append(domain_id)
        sql_where_string = " and ".join(sql_where)

        sql_query = "SELECT * FROM tenant"
        sql_query = "%s WHERE %s" % (sql_query, sql_where_string)

        result = db.execute(sql_query, sql_values)
        db.commit()

        if len(result) == 1:
            return result[0]
        else:
            raise exceptions.HTTPNotFound("Not Found", "Tenant not found")


def get_local_id(domain_id, external_id):
    db = Mysql()
    sql = "SELECT * FROM tenant WHERE external_id = %s limit 1"
    result = db.execute(sql, (external_id,))
    if len(result) == 0:
        sql = "INSERT INTO tenant"
        sql += " (id, external_id, domain_id)"
        sql += " VALUES"
        sql += " (%s, %s, %s)"
        db.execute(sql, (str(uuid.uuid4()), external_id, domain_id))
        tenant_id = db.last_row_id()
        db.commit()
        return tenant_id
    else:
        return result[0]['id']


def get_external_id(tenant_id):
    db = Mysql()
    sql = "SELECT * FROM tenant WHERE id = %s limit 1"
    result = db.execute(sql, (tenant_id,))
    if len(result) == 0:
        raise exceptions.HTTPNotFound("Not Found", "Tenant not found")
    else:
        if result[0]['external_id'] is None:
            return result[0]['id']
        else:
            return result[0]['external_id']
