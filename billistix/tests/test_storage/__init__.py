# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import copy
from nose import SkipTest
from billistix.openstack.common import cfg
from billistix.openstack.common import log as logging
from billistix.tests import TestCase
from billistix import storage
from billistix import exceptions

LOG = logging.getLogger(__name__)


class StorageTestCase(TestCase):
    __test__ = False

    def get_storage_driver(self, conf=cfg.CONF):
        connection = storage.get_connection(conf)
        return connection


class StorageDriverTestCase(StorageTestCase):
    __test__ = False

    rate_fixtures = [
        {'name': 'cpu', 'value': 1},
        {'name': 'memory', 'value': 2}
    ]

    def setUp(self):
        super(StorageDriverTestCase, self).setUp()
        self.storage_conn = self.get_storage_driver()
        self.admin_context = self.get_admin_context()

    def test_init(self):
        self.get_storage_driver()

    def add_rate_fixtures(self, fixture=0, values={}):
        _values = copy.copy(self.rate_fixtures[fixture])
        _values.update(values)
        return self.storage_conn.add_rate(self.admin_context, _values)

    def test_add_rate(self):
        rate = self.storage_conn.add_rate(
            self.admin_context,
            {'name': 'cpu', 'value': 1})
        self.assertEquals(rate.name, 'cpu')
        self.assertEquals(rate.value, 1)

    def test_delete_rate(self):
        # NOTE: Needs fixing - get_rate is missing
        rate = self.storage_conn.add_rate(
            self.admin_context,
            {'name': 'cpu', 'value': 1})
        self.storage_conn.delete_rate(self.admin_context, rate.id)

    def test_update_rate(self):
        rate = self.storage_conn.add_rate(
            self.admin_context,
            {'name': 'cpu', 'value': 1})
        self.storage_conn.update_rate(
            self.admin_context,
            rate.id,
            values={'name': 'memory', 'value': 15})
        self.assertEquals(rate.name, 'memory')
        self.assertEquals(rate.value, 15)
