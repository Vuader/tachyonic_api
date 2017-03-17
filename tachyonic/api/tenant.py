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
        fields.append('external_id')
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
        data['external_id'] = tenant_id
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

    def retrieve(self, domain_id=None, external_id=None,
                 search=None, orderby=None, start=None, limit=None):

        db = Mysql()
        sql_values = []
        sql_where = []
        if external_id is not None:
            sql_where.append("external_id = %s")
            sql_values.append(external_id)

        sql_where.append("domain_id = %s")
        sql_values.append(domain_id)

        fields = db.fields('tenant')
        sql_search_where = []
        if search is not None:
            for field in fields:
                if 'char' in fields[field]:
                    sql_search_where.append("%s like %s" % (field, '%s'))
                    sql_values.append(search + "%")
                if 'int' in fields[field]:
                    try:
                        sql_values.append(int(search))
                        sql_search_where.append("%s = %s" % (field, '%s'))
                    except:
                        pass
            if len(sql_search_where) > 0:
                sql_search_string = " or ".join(sql_search_where)
                sql_where.append("( %s )" % (sql_search_string,))

        sql_where_string = " and ".join(sql_where)

        sql_pager = ""
        if start is not None and limit is not None:
            sql_pager = "limit %s, %s" % (int(start), int(limit))

        sql_order = ""
        if orderby is not None:
            orders = orderby.split(',')
            formatted_orders = []
            for order in orders:
                regex = re.compile('[^a-zA-Z_]')
                order_options = order.split(' ')
                order_field = order_options[0]
                order_field = regex.sub('', order_field)
                fields_no_tables = [re.sub(".*\.","",f) for f in fields]
                if order_field not in fields_no_tables:
                    raise exceptions.HTTPInvalidParam(order_field)
                order_type = "asc"
                if len(order_options) == 2:
                    order_type = order_options[1].lower()
                if order_type != "asc" and order_type != "desc":
                    order_type = "asc"
                formatted_order = "%s %s" % (order_field, order_type)
                formatted_orders.append(formatted_order)
            formatted_orders = ",".join(formatted_orders)
            sql_order = "ORDER BY %s " % (formatted_orders,)
        sql_count = "SELECT count(id) AS count FROM tenant"
        sql_query = "SELECT * FROM tenant"

        if len(sql_where) > 0:
            sql_query = "%s WHERE %s" % (sql_query, sql_where_string)
            sql_count = "%s WHERE %s" % (sql_count, sql_where_string)
        sql_query = "%s %s %s" % (sql_query, sql_order, sql_pager)

        count_result = db.execute(sql_count, sql_values)
        total = count_result[0]['count']

        result = db.execute(sql_query, sql_values)
        db.commit()

        return (total, result)

    def delete(self, domain_id, tenant_id):
        db = Mysql()
        sql = "DELETE FROM tenant WHERE domain_id = %s and id = %s"
        db.execute(sql, (domain_id, tenant_id))
        if db.last_row_count() > 0:
            db.commit()
            return True
        else:
            db.commit()
            return False


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
