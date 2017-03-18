# -*- coding: utf-8 -*-
from pytest import raises

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest
parametrize = pytest.mark.parametrize

from tachyonic.api import metadata


class TestMain(object):
    def test_package(self):
        assert metadata.package == 'tachyonic.api'
