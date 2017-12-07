# -*- coding: utf-8 -*-
# Copyright (c) 2017, Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from tachyonic.neutrino.model import Model
from tachyonic.neutrino.html.bootstrap3.forms import Form as Bootstrap


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
