import logging
import json
import base64
from collections import OrderedDict

from tachyonic import app
from tachyonic import router
from tachyonic.common import exceptions
from tachyonic.common import constants as const
from tachyonic.neutrino.mysql import Mysql
from tachyonic.api.models import themes

from tachyonic.api.api import orm as api
from tachyonic.api.api import sql as sql_api

log = logging.getLogger(__name__)


@app.resources()
class Themes(object):
    def __init__(self):
        router.add(const.HTTP_GET,
                   '/v1/themes',
                   self.get,
                   'tachyonic:public')
        router.add(const.HTTP_GET,
                   '/v1/theme/{domain}',
                   self.get,
                   'tachyonic:public')
        router.add(const.HTTP_GET,
                   '/v1/theme/{domain}/images',
                   self.images,
                   'tachyonic:public')
        router.add(const.HTTP_GET,
                   '/v1/theme/{domain}/single',
                   self.single,
                   'tachyonic:public')
        router.add(const.HTTP_GET,
                   '/v1/theme/{domain}/css',
                   self.css,
                   'tachyonic:public')
        router.add(const.HTTP_PUT,
                   '/v1/css/{domain_id}',
                   self.update,
                   'themes:admin')
        router.add(const.HTTP_PUT,
                   '/v1/images/{domain_id}',
                   self.upload,
                   'themes:admin')
        router.add(const.HTTP_DELETE,
                   '/v1/images/{domain_id}/{image}',
                   self.delete_image,
                   'themes:admin')
        router.add(const.HTTP_POST,
                   '/v1/theme',
                   self.post,
                   'themes:admin')
        router.add(const.HTTP_PUT,
                   '/v1/theme/{domain}',
                   self.put,
                   'themes:admin')
        router.add(const.HTTP_DELETE,
                   '/v1/theme/{domain}',
                   self.delete,
                   'themes:admin')

    def _images(self, result):
        data = {}
        data['logo'] = None
        data['logo_type'] = None
        data['logo_name'] = None
        data['logo_timestamp'] = None
        data['background'] = None
        data['background_type'] = None
        data['background_name'] = None
        data['background_timestamp'] = None
        if len(result) > 0:
            logo = result[0]['logo']
            logo_name = result[0]['logo_name']
            logo_type = result[0]['logo_type']
            logo_timestamp = result[0]['logo_timestamp']
            background = result[0]['background']
            background_name = result[0]['background_name']
            background_type = result[0]['background_type']
            background_timestamp = result[0]['background_timestamp']
            if logo_name is not None and logo_name != '':
                data['logo'] = base64.b64encode(logo)
                data['logo_type'] = logo_type
                data['logo_name'] = logo_name
                data['logo_timestamp'] = str(logo_timestamp.strftime("%Y/%m/%d %H:%M:%S"))
            if background_name is not None and background_name != '':
                data['background'] = base64.b64encode(background)
                data['background_type'] = background_type
                data['background_name'] = background_name
                data['background_timestamp'] = str(background_timestamp.strftime("%Y/%m/%d %H:%M:%S"))
        return data

    def images(self, req, resp, domain=None):
        db = Mysql()
        sql = "SELECT * FROM theme"
        sql += " WHERE id = %s"
        sql += " or domain = %s"
        result = db.execute(sql, (domain, domain))
        return json.dumps(self._images(result), indent=4)

    def single(self, req, resp, domain=None):
        db = Mysql()
        sql = "SELECT * FROM theme"
        sql += " WHERE id = %s"
        sql += " or domain = %s"
        result = db.execute(sql, (domain, domain))
        single = {}
        if len(result) == 1:
            single['domain'] = result[0]['domain']
            single['name'] = result[0]['name']
            if (result[0]['logo_name'] is not None and 
                    result[0]['logo_name'] != ''):
                single['logo'] = True
            else:
                single['logo'] = False
            if (result[0]['background_name'] is not None and 
                    result[0]['background_name'] != ''):
                single['background'] = True
            else:
                single['background'] = False
        return json.dumps(single, indent=4)


    def css(self, req, resp, domain=None):
        db = Mysql()
        sql = "SELECT id FROM theme"
        sql += " WHERE id = %s"
        sql += " or domain = %s"
        result = db.execute(sql, (domain, domain))
        sheet = OrderedDict()
        if len(result) > 0:
            theme_id = result[0]['id']
            sql = "SELECT * FROM css"
            sql += " WHERE theme_id = %s"
            sql += " order by element asc, property asc, value asc"
            result = db.execute(sql, (theme_id,))
            for o in result:
                element = o['element']
                prop = o['property']
                value = o['value']
                if element not in sheet:
                    sheet[element] = OrderedDict()
                sheet[element][prop] = value
        return json.dumps(sheet, indent=4)


    def delete_image(self, req, resp, domain_id=None, image=None):
        result = sql_api.get_query('theme', req, resp,
                               domain_id)
        if len(result) > 0:
            db = Mysql()
            if image.lower() == 'logo' or image.lower() == 'background':
                sql = "UPDATE theme"
                if image.lower() == 'logo':
                    sql += " set logo = null"
                    sql += " ,logo_name = null"
                    sql += " ,logo_type = null"
                if image.lower() == 'background':
                    sql += " set background = null"
                    sql += " ,background_name = null"
                    sql += " ,background_type = null"
                sql += " WHERE id = %s"
                db.execute(sql, (domain_id,))
                db.commit()

    def upload(self, req, resp, domain_id=None):
        result = sql_api.get_query('theme', req, resp,
                               domain_id)
        if len(result) > 0:
            db = Mysql()
            data = json.loads(req.read())
            for img in data:
                if 'logo' in data:
                    name = data['logo']['name']
                    mtype = data['logo']['type']
                    img = data['logo']['data']
                    img = base64.b64decode(img)
                    sql = "UPDATE theme"
                    sql += " set logo_name = %s"
                    sql += ", logo_type = %s"
                    sql += ", logo = %s"
                    sql += " WHERE id = %s"
                    db.execute(sql, (name, mtype, img, domain_id))
                    db.commit()
                if 'background' in data:
                    name = data['background']['name']
                    mtype = data['background']['type']
                    img = data['background']['data']
                    img = base64.b64decode(img)
                    sql = "UPDATE theme"
                    sql += " set background_name = %s"
                    sql += ", background_type = %s"
                    sql += ", background = %s"
                    sql += " WHERE id = %s"
                    db.execute(sql, (name, mtype, img, domain_id))
                    db.commit()


    def update(self, req, resp, domain_id=None):
        result = sql_api.get_query('theme', req, resp,
                               domain_id)
        if len(result) > 0:
            db = Mysql()
            data = json.loads(req.read())
            if 'del_element' in data:
                element = data['del_element']
                property = data['del_property']
                sql = "DELETE FROM css"
                sql += " WHERE theme_id = %s"
                sql += " AND element = %s"
                sql += " AND property = %s"
                db.execute(sql, (domain_id, element, property))
            else:
                for i in data:
                    element, property, value = i
                    if element != '':
                        if property != '':
                            if value == '':
                                value = "NULL"
                            sql = "INSERT INTO css"
                            sql += " (id, theme_id, element, property, value)"
                            sql += " VALUES"
                            sql += " (uuid(), %s,%s,%s,%s)"
                            sql += " ON DUPLICATE KEY UPDATE"
                            sql += " value=%s"
                            db.execute(sql, (domain_id,
                                             element,
                                             property,
                                             value,
                                             value))
            db.commit()

    def get(self, req, resp, domain=None):
        return api.get(themes.Themes, req, resp, domain)

    def post(self, req, resp):
        return api.post(themes.Theme, req)

    def put(self, req, resp, domain):
        return api.put(themes.Theme, req, domain)

    def delete(self, req, resp, domain):
        return api.delete(themes.Theme, req, domain)
