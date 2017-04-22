from __future__ import absolute_import
from __future__ import unicode_literals

from tachyonic.neutrino.model import Model
from tachyonic.neutrino.web.bootstrap3.forms import Form as Bootstrap

class DomainFields(object):
    class Meta(object):
        db_table = 'domain'

    id = Model.Uuid(hidden=True)
    name = Model.Text(length=15,
                          max_length=15,
                          label="Domain",
                          required=True)
    enabled = Model.Bool(label="Enabled")
    creation_time = Model.Datetime(label="Created",
                                       placeholder="0000-00-00 00:00:00",
                                       readonly=True,
                                       length=20)


class Domains(DomainFields, Model):
    pass


class Domain(DomainFields, Bootstrap):
    pass
