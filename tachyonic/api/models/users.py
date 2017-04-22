from __future__ import absolute_import
from __future__ import unicode_literals

from tachyonic.neutrino.model import Model
from tachyonic.neutrino.web.bootstrap3.forms import Form as Bootstrap

class UserFields(object):
    class Meta(object):
        db_table = 'user'

    id = Model.Uuid(hidden=True)
    domain_id = Model.Uuid(hidden=True)
    tenant_id = Model.Uuid(hidden=True)
    username = Model.Text(length=15,
                              max_length=15,
                              label="Username",
                              required=True)
    password = Model.Password(label="Password",
                                  algo=None,
                                  length=15, 
                                  nodb=True,
                                  max_length=15)
    email = Model.Email(label="Email",
                            length=30,
                            max_length=50)
    name = Model.Text(label="Fullname",
                          placeholder=".e.g Joe Gates",
                          required=False,
                          length=30,
                          max_length=50)
    title = Model.Text(label="Title",
                           choices=['', 'Mr', 'Mrs', 'Ms', 'Dr', 'Prof'],
                           required=False,
                           length=5)
    employer = Model.Text(label="Employer",
                              placeholder="e.g. Enterprise Inc.",
                              required=False,
                              length=30)
    designation = Model.Text(label="Designation",
                                 placeholder="e.g. Engineer.",
                                 required=False,
                                 length=25)
    phone_mobile = Model.Phone(label="Mobile Phone",
                                   placeholder="e.g. +16502530000",
                                   required=False)
    phone_office = Model.Phone(label="Office Phone",
                                   placeholder="e.g. +16502530000",
                                   required=False)
    enabled = Model.Bool(label="Enabled")
    last_login = Model.Datetime(label="Last Login",
                                    placeholder="0000-00-00 00:00:00",
                                    readonly=True,
                                    length=20)
    creation_time = Model.Datetime(label="Created",
                                       placeholder="0000-00-00 00:00:00",
                                       readonly=True,
                                       length=20)


class Users(UserFields, Model):
    pass


class User(UserFields, Bootstrap):
    pass
