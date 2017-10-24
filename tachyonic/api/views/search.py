import logging
import json
import datetime
import copy

from tachyonic import app
from tachyonic import router
from tachyonic.common import constants as const
from tachyonic.common import exceptions
from tachyonic.common.imports import get_class
from tachyonic.api.api import sql

from tachyonic.api import tenant

log = logging.getLogger(__name__)


@app.resources()
class Search(object):
    def __init__(self):
        router.add(const.HTTP_GET,
                   '/v1/search',
                   self.get,
                   'tachyonic:login')

    def get(self, req, resp):
        driver = req.config.get('tenants').get('driver')
        driver = get_class(driver)()

        domain_id = req.context.get('domain_id')

        if domain_id is None:
            raise exceptions.HTTPForbidden("Access Forbidden", "Require domain!")

        result = sql.get_query('tenant', req, resp,
                                       req.context['tenant_id'],
                                       ignore_tenant=True)
        if len(result) == 0:
            result = sql.get_query('tenant', req, resp, None)
        for t in result:
            if t['external_id'] is not None:
                q = driver.retrieve(domain_id, t['external_id'])
                t.update(q)

        for row in result:
            for key in row:
                if isinstance(row[key],datetime.datetime):
                    row[key] = row[key].strftime("%Y/%m/%d %H:%M:%S")
                if key == "enabled":
                    if row[key] == 0:
                        row[key] = False
                    elif row[key] == 1:
                        row[key] = True


        return json.dumps(result, indent=4)
