from __future__ import absolute_import
from __future__ import unicode_literals

from tachyonic.neutrino.model import Model
from tachyonic.neutrino.web.bootstrap3.forms import Form as Bootstrap


class TenantBase(object):
    class Meta(object):
        db_table = 'tenant'

    id = Model.Uuid(label="Internal ID", readonly=True,
                       lenght=60)
    external_id = Model.Text(label='External ID',
                                 length=60, readonly=True)
    tenant_id = Model.Text(label='Parent ID',
                           length=60, readonly=True)
    domain_id = Model.Uuid(hidden=True)


class TenantFields(TenantBase):

    tenant_type = Model.Text(label="Account Type",
                                 choices=['individual', 'organization'],
                                 required=False,
                                 length=13)
    name = Model.Text(label="Name",
                          required=True,
                          length=30,
                          max_length=50)
    title = Model.Text(label="Title",
                           choices=['', 'Mr', 'Mrs', 'Ms', 'Dr', 'Prof'],
                           required=False,
                           length=5,
                           cls='individual')
    email = Model.Email(label="Email",
                            length=30,
                            max_length=50)
    phone_mobile = Model.Phone(label="Mobile Phone",
                                   placeholder="e.g. +16502530000",
                                   required=False,
                                   cls='individual')
    phone_office = Model.Phone(label="Office Phone",
                                   placeholder="e.g. +16502530000",
                                   required=False)
    phone_fax = Model.Phone(label="Fax Phone",
                                placeholder="e.g. +16502530000",
                                required=False)
    phone_home = Model.Phone(label="Home Phone",
                                 placeholder="e.g. +16502530000",
                                 required=False,
                                 cls='individual')
    reg = Model.Text(label="Registration No.",
                         required=False,
                         length=30,
                         max_length=50,
                         cls='organization')
    taxno = Model.Text(label="TAX/VAT No.",
                           required=False,
                           length=30,
                           max_length=50,
                           cls='organization')
    idno = Model.Text(label="Identification No.",
                          required=False,
                          length=30,
                          max_length=50,
                          cls='individual')
    idtype = Model.Text(label="Identification Type",
                            choices=['ID Document', 'Passport'],
                            required=False,
                            length=13,
                            cls='individual')
    employer = Model.Text(label="Employer",
                              placeholder="e.g. Enterprise Inc.",
                              required=False,
                              length=30,
                              cls='individual')
    designation = Model.Text(label="Designation",
                                 placeholder="e.g. Engineer.",
                                 required=False,
                                 length=25,
                                 cls='individual')
    bill_address = Model.Text(label="Billing Address",
                                  placeholder="e.g. Engineer.",
                                  choices=['Physical', 'Post'],
                                  required=False,
                                  length=10)
    address_line1 = Model.Text(label="Address Line 1",
                                   placeholder="e.g. 1600 Amphitheatre Parkway",
                                   required=False,
                                   length=25)
    address_line2 = Model.Text(label="Address Line 2",
                                   placeholder="",
                                   required=False,
                                   length=25)
    address_line3 = Model.Text(label="Address Line 3",
                                   placeholder="",
                                   required=False,
                                   length=25)
    address_city = Model.Text(label="Address City",
                                  placeholder="eg. Mountain View",
                                  required=False,
                                  length=25)
    address_state = Model.Text(label="Address State/Province",
                                   placeholder="e.g. California",
                                   required=False,
                                   length=25)
    address_code = Model.Text(label="Address ZIP Code",
                                  placeholder="eg. 94043",
                                  required=False,
                                  length=10)
    address_country = Model.Text(label="Address Country",
                                     placeholder="e.g. United States",
                                     required=False,
                                     length=25)
    post_line1 = Model.Text(label="Post Line 1",
                                placeholder="e.g. 1600 Amphitheatre Parkway",
                                required=False,
                                length=25)
    post_line2 = Model.Text(label="Post Line 2",
                                placeholder="",
                                required=False,
                                length=25)
    post_line3 = Model.Text(label="Post Line 3",
                                placeholder="",
                                required=False,
                                length=25)
    post_city = Model.Text(label="Post City",
                               placeholder="eg. Mountain View",
                               required=False,
                               length=25)
    post_state = Model.Text(label="Post State/Province",
                                placeholder="e.g. California",
                                required=False,
                                length=25)
    post_code = Model.Text(label="Post ZIP Code",
                               placeholder="eg. 94043",
                               required=False,
                               length=10)
    post_country = Model.Text(label="Post Country",
                                  placeholder="e.g. United States",
                                  required=False,
                                  length=25)
    enabled = Model.Bool(label="Enabled")
    creation_time = Model.Datetime(label="Created",
                                       placeholder="0000-00-00 00:00:00",
                                       readonly=True,
                                       length=20)


class Tenants(TenantFields, Model):
    pass


class Tenant(TenantFields, Bootstrap):
    pass
