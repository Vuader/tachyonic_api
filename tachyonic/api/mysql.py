from __future__ import absolute_import
from __future__ import unicode_literals

import pymysql as MySQLdb
from tachyonic.neutrino.mysql import Mysql as NfwMysql
from tachyonic.common import exceptions


class Mysql(object):
    def __init__(self):
        self._mysql = NfwMysql()

    def execute(self, *args, **kwargs):
        try:
            return self._mysql.execute(*args, **kwargs)
        except MySQLdb.IntegrityError as e:
            code, value = e
            if code == 1451:
                raise exceptions.HTTPBadRequest('Object records','Object is required by others')
            elif code == 1062:
                raise exceptions.HTTPBadRequest('Object records','Duplicate object')
            elif code == 1048:
                raise exceptions.HTTPBadRequest('Object records', "SQL %s" % (value,))
            else:
                raise MySQLdb.IntegrityError(code, value)

    def __getattr__(self, key):
        if hasattr(self._mysql, key):
            return getattr(self._mysql, key)

