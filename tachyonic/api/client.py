from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from tachyonic.client.client import Client

log = logging.getLogger(__name__)

sessions = {}

class Users(Client):
    def list_users(self):
        url = self.url
        url = "%s/v1/users" % (url,)
        headers, result = self.execute("GET", url)
        return result

