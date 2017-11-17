import logging
import json
import re
import uuid

from tachyonic.neutrino import exceptions

from tachyonic.api.mysql import Mysql

from datetime import datetime

log = logging.getLogger(__name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise exceptions.HTTPInvalidParam("Type not serializable")


def table_has_col(table, column):
    db = Mysql()
    result = db.execute("DESCRIBE %s" % (table,))
    for field in result:
        if field['Field'] == column:
            return True
    return False


def parse_body(body, domain, domain_id, tenant, tenant_id):
    obj = json.loads(body)
    if 'id' in obj:
        del obj['id']
    if domain is True:
        obj['domain_id'] = domain_id
    if tenant is True:
        obj['tenant_id'] = tenant_id

    return json.dumps(obj, indent=4)


class LeftJoin():
    def __init__(self, additional_select, ljo):
        self.additional_select = additional_select
        self.ljo = ljo


def get_query(table, req, resp, id, where=None,
                  where_values=None, left_join=None,
                  ignore_tenant=False,
                  where_null=[]):
    db = Mysql()

    tables = set([ table ])

    if left_join is not None:
        for s in left_join.additional_select:
            tables.add(s.split(".")[0])

    fields = {}

    for i, t in enumerate(tables):
        field_query = """SELECT `COLUMN_NAME`,`DATA_TYPE`
                     FROM `INFORMATION_SCHEMA`.`COLUMNS`
                     WHERE `TABLE_NAME`=%s"""
        field_results = db.execute(field_query, (t,))

        if len(field_results) > 0:
            for field in field_results:
                fields[t + "." + field['COLUMN_NAME']] = field['DATA_TYPE']
        else:
            raise exceptions.HTTPNotFound("Not Found", "Table not found")

    tenant_id = req.context.get('tenant_id')
    domain_id = req.context.get('domain_id')
    domain_admin = req.context.get('domain_admin')

    header_start = req.headers.get('X-Pager-Start')
    header_limit = req.headers.get('X-Pager-Limit')
    header_order = req.headers.get('X-Order-By')
    search = req.headers.get('X-Search')

    tenant_field = table_has_col(table, 'tenant_id')
    domain_field = table_has_col(table, 'domain_id')

    sql_values = []
    sql_where = []
    if id is not None:
        if left_join is None:
            sql_where.append("id = %s")
        else:
            sql_where.append(table + ".id = %s")
        sql_values.append(id)

    if domain_id is not None:
        if domain_field is True:
            if left_join is None:
                sql_where.append("domain_id = %s")
            else:
                sql_where.append(table + ".domain_id = %s")
            sql_values.append(domain_id)
    else:
        if domain_field is True:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")

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

    if ignore_tenant is False:
        if tenant_id is not None:
            if tenant_field is True:
                sql_where.append("tenant_id = %s")
                sql_values.append(tenant_id)
        else:
            if tenant_field is True:
                if domain_admin is False:
                    raise exceptions.HTTPForbidden("Access Forbidden", "Not within tenant!")

    if where is not None:
        if type(where) is str:
            if re.search('%',where):
                sql_where.append(where)
            else:
                sql_where.append(where + " = %s")
        elif type(where) is list:
            sql_where.extend([w + " = %s" for w in where])
    if where_values is not None:
        sql_values.extend(where_values)

    sql_where.extend([wn + ' is NULL' for wn in where_null])

    sql_where_string = " and ".join(sql_where)

    sql_pager = ""
    if header_start is not None and header_limit is not None:
        start = int(header_start)
        limit = int(header_limit)
        sql_pager = "limit %s, %s" % (start, limit)

    sql_order = ""
    if header_order is not None:
        orders = header_order.split(',')
        formatted_orders = []
        for order in orders:
            regex = re.compile('[^a-zA-Z_]')
            order_options = order.split(' ')
            order_field = order_options[0]
            order_field = regex.sub('', order_field)
            fields_no_tables = [re.sub(".*\.","",f) for f in fields]
            if order_field not in fields_no_tables:
                if left_join is None:
                    raise exceptions.HTTPInvalidParam(order_field)
                elif order_field not in left_join.additional_select.values():
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

    if left_join is None:
        sql_count = "SELECT count(id) as count FROM %s" % (table,)
        sql_query = "SELECT * FROM %s" % (table,)
    else:
        sql_query = ["SELECT"]
        original_sql_query = [ "%s.*" % (table,)]
        new_sql_query = []
        for k in left_join.additional_select:
            if left_join.additional_select[k]:
                new_sql_query.append(k + " as " + left_join.additional_select[k])
            else:
                new_sql_query.append(k)
        sql_query.append(",".join(original_sql_query + new_sql_query))
        sql_query.append("FROM")
        sql_query.append(table)
        sql_count = ["SELECT"]
        sql_count.append("count(%s.id) as count" % (table,))
        sql_count.append("FROM")
        sql_count.append(table)
        for k in left_join.ljo:
            sql_query.append('LEFT JOIN')
            sql_query.append(k)
            sql_query.append('ON')
            sql_count.append('LEFT JOIN')
            sql_count.append(k)
            sql_count.append('ON')
            for i, o in enumerate(left_join.ljo[k]):
                if i > 0:
                    sql_query.append('AND')
                    sql_count.append('AND')
                sql_query.append(o+"="+left_join.ljo[k][o])
                sql_count.append(o+"="+left_join.ljo[k][o])
        sql_query = " ".join(sql_query)
        sql_count = " ".join(sql_count)

    if len(sql_where) > 0:
        sql_query = "%s where %s" % (sql_query, sql_where_string)
        sql_count = "%s where %s" % (sql_count, sql_where_string)
    sql_query = "%s %s %s" % (sql_query, sql_order, sql_pager)

    count_result = db.execute(sql_count, sql_values)
    resp.headers['X-Total-Rows'] = count_result[0]['count']
    resp.headers['X-Filtered-Rows'] = count_result[0]['count']

    result = db.execute(sql_query, sql_values)
    db.commit()

    return result


def get(table, req, resp, id, where=None, where_values=None,
        where_null=[], left_join=None, ignore_tenant=False):
    result = get_query(table,
                       req,
                       resp,
                       id,
                       where=where,
                       where_values=where_values,
                       where_null=where_null,
                       left_join=left_join)

    if id is not None:
        if len(result) == 1:
            return json.dumps(result[0], indent=4, default=json_serial)
        else:
            raise exceptions.HTTPNotFound("Not Found", "Object not found")
    else:
        return json.dumps(result, indent=4, default=json_serial)
