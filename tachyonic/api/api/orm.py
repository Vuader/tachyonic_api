from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import re

from tachyonic.neutrino import exceptions
from tachyonic.neutrino import model as nfw_model

from tachyonic.api.mysql import Mysql
from tachyonic.api.api.sql import table_has_col
from tachyonic.api.api.sql import parse_body

log = logging.getLogger(__name__)

def model_table(model):
    table = model._model
    if hasattr(model, 'Meta'):
        if hasattr(model.Meta, 'db_table'):
            table = model.Meta.db_table
    return table


def get(model, req, resp, id, where=None, where_values=None,
        ignore_tenant=False):
    db = Mysql()
    data = model(db=db)
    table = model_table(data)

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
        sql_where.append("id = %s")
        sql_values.append(id)

    if domain_id is not None:
        if domain_field is True:
            sql_where.append("domain_id = %s")
            sql_values.append(domain_id)
    else:
        if domain_field is True:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")

    sql_search_where = []
    if search is not None:
        search = "%s%s" % (search,'%')
        for field in data._declared_fields:
            f = getattr(data, field)
            if isinstance(f, nfw_model.Fields.Text):
                sql_search_where.append("%s like %s" % (field, '%s'))
                sql_values.append(search)
            if isinstance(f, nfw_model.Fields.Integer):
                sql_search_where.append("%s like %s" % (field, '%s'))
                sql_values.append(int(search))
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
        sql_where.append(where)
    if where_values is not None:
        sql_values.extend(where_values)

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
            if order_field not in data._declared_fields:
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

    sql_query = "SELECT * FROM %s" % (table,)
    sql_count = "SELECT count(id) as count FROM %s" % (table,)
    if len(sql_where) > 0:
        sql_query = "%s where %s" % (sql_query, sql_where_string)
        sql_count = "%s where %s" % (sql_count, sql_where_string)
    sql_query = "%s %s %s" % (sql_query, sql_order, sql_pager)

    count_result = db.execute(sql_count, sql_values)
    resp.headers['X-Total-Rows'] = count_result[0]['count']
    resp.headers['X-Filtered-Rows'] = count_result[0]['count']

    data.query(sql_query, sql_values)
    data.commit()
    if id is not None:
        if len(data) == 1:
            return data[0].dump_json()
        else:
            raise exceptions.HTTPNotFound("Not Found", "Object not found")
    else:
        return data.dump_json()


def post(model, req, ignore_tenant=False, callback=None):
    db = Mysql()
    data = model(db=db)
    table = model_table(data)

    tenant_id = req.context.get('tenant_id')
    domain_id = req.context.get('domain_id')
    domain_admin = req.context.get('domain_admin')
    tenant_field = table_has_col(table, 'tenant_id')
    domain_field = table_has_col(table, 'domain_id')

    if domain_id is None:
        if domain_field is True:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")

    if ignore_tenant is False:
        if tenant_id is None:
            if tenant_field is True:
                if domain_admin is False:
                    raise exceptions.HTTPForbidden("Access Forbidden", "Not within tenant!")

    request_body = parse_body(req.read(),
                              domain_field,
                              domain_id,
                              tenant_field,
                              tenant_id)

    data.load_json(request_body)
    if callback is not None:
        callback(data)
    data.commit()
    return data.dump_json()


def put(model, req, id, ignore_tenant=False, callback=None):
    db = Mysql()
    data = model(db=db)
    table = model_table(data)

    tenant_id = req.context.get('tenant_id')
    domain_id = req.context.get('domain_id')
    domain_admin = req.context.get('domain_admin')
    tenant_field = table_has_col(table, 'tenant_id')
    domain_field = table_has_col(table, 'domain_id')

    if domain_id is None:
        if domain_field is True:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")

    if ignore_tenant is False:
        if tenant_id is None:
            if tenant_field is True:
                if domain_admin is False:
                    raise exceptions.HTTPForbidden("Access Forbidden", "Not within tenant!")

    request_body = parse_body(req.read(),
                              domain_field,
                              domain_id,
                              tenant_field,
                              tenant_id)

    sql_where = []
    sql_values = []
    sql_where.append("id = %s")
    sql_values.append(id)

    if domain_id is not None:
        if domain_field is True:
            sql_where.append("domain_id = %s")
            sql_values.append(domain_id)

    if ignore_tenant is False:
        if tenant_id is not None:
            if tenant_field is True:
                sql_where.append("tenant_id = %s")
                sql_values.append(tenant_id)

    sql_where_string = " and ".join(sql_where)

    sql = "SELECT * FROM %s WHERE %s" % (table, sql_where_string)
    data.query(sql=sql, values=sql_values)

    if len(data) > 0:
        data.load_json(request_body)
        if callback is not None:
            callback(id, data)
        data.commit()
        return data.dump_json()
    else:
        db.commit()
        raise exceptions.HTTPNotFound("Not Found", "Object not found")


def delete(model, req, id, ignore_tenant=False, callback=None):
    db = Mysql()
    data = model(db=db)
    table = model_table(data)

    tenant_id = req.context.get('tenant_id')
    domain_id = req.context.get('domain_id')
    domain_admin = req.context.get('domain_admin')
    tenant_field = table_has_col(table, 'tenant_id')
    domain_field = table_has_col(table, 'domain_id')

    if domain_id is None:
        if domain_field is True:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")

    if ignore_tenant is False:
        if tenant_id is None:
            if tenant_field is True:
                if domain_admin is False:
                    raise exceptions.HTTPForbidden("Access Forbidden", "Not within tenant!")
    else:
        tenant_field = False

    if tenant_field is True and tenant_id is not None:
        sql = "delete from %s" % (table) +\
              " where id = %s and tenant_id = %s and domain_id = %s"
        db.execute(sql, (id, tenant_id, domain_id))
    elif domain_field is True and domain_id is not None:
        sql = "delete from %s" % (table) +\
              " where id = %s and domain_id = %s"
        db.execute(sql, (id, domain_id))
    else:
        sql = "delete from %s" % (table) +\
              " where id = %s"
        db.execute(sql, (id,))

    if callback is not None:
        callback(id)

    if db.last_row_count() > 0:
        db.commit()
        return "{\"action\": \"success\"}"
    else:
        db.commit()
        raise exceptions.HTTPNotFound("Not Found", "Object not found")
