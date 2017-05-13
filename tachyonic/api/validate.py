from __future__ import absolute_import
from __future__ import unicode_literals

import uuid
import re
import logging

from tachyonic.common import exceptions

log = logging.getLogger(__name__)

def enabled(function, config):
    if not config.getboolean(function, True):
        raise exceptions.HTTPBadRequest('Function disabled',
                                        'Function not availible due to' +
                                        ' administrator configuration')


