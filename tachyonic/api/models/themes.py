from __future__ import absolute_import
from __future__ import unicode_literals

from tachyonic.neutrino.model import Model
from tachyonic.neutrino.web.bootstrap3.forms import Form as Bootstrap


class ThemeFields(object):
    class Meta(object):
        db_table = 'theme'

    id = Model.Uuid(hidden=True)
    domain_id = Model.Uuid(hidden=True)
    tenant_id = Model.Uuid(hidden=True)
    domain = Model.Text(length=40,
                        max_length=40,
                        label="Domain",
                        required=True)
    name = Model.Text(length=40,
                      max_length=40,
                      label="Site Name",
                      required=True)
    creation_time = Model.Datetime(label="Created",
                                   placeholder="0000-00-00 00:00:00",
                                   readonly=True,
                                   length=20)
    logo_name = Model.Text(hidden=True)
    background_name = Model.Text(hidden=True)



class Themes(ThemeFields, Model):
    pass


class Theme(ThemeFields, Bootstrap):
    pass
