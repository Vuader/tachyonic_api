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

import logging
import json

from tachyonic.neutrino import constants as const
from tachyonic.neutrino.wsgi import router
from tachyonic.neutrino.wsgi import app

log = logging.getLogger(__name__)

# WTF ARE YOU DOING???? DUDE
@app.resources()
class Index(object):
    def __init__(self):
        router.add(const.HTTP_GET, '/', self.index, 'tachyonic:public')

    def index(self, req, resp):
        resources = {}
        routes = req.router.routes
        site = req.get_app_url()
        resources['local'] = {}
        resources['external'] = {}
        local = resources['local']
        external = resources['external']
        for r in routes:
            r_method, r_uri, r_obj, r_name = r
            if req.policy.validate(r_name):
                href = "%s/%s" % (site, r_uri)
                if href not in local:
                    local[href] = {}
                if 'methods' not in local[href]:
                    local[href]['methods'] = {}
                local[href]['methods'][r_method] = r_name

        for endpoint in app.config.get_items('endpoints'):
            name, href = endpoint
            external[name] = href

        return json.dumps(resources, indent=4)
