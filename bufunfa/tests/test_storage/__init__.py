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
from bufunfa.openstack.common import cfg
from bufunfa.openstack.common import log as logging
from bufunfa.tests import TestCase
from bufunfa import storage
from bufunfa import exceptions

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

    account_fixtures = [
        {'name': 'customer_a'},
        {'name': 'customer_b'}
    ]

    system_account_fixtures = [
        {
            'id': 'd44f1779-5034-455e-b334-cac2ac3eee33',
            'name': 'system_a'
        },
        {
            'id': 'a45e43af-090b-4045-ae78-6a9d507d1418',
            'name': 'system_b'
        }
    ]

    def setUp(self):
        super(StorageDriverTestCase, self).setUp()
        self.storage_conn = self.get_storage_driver()
        self.admin_context = self.get_admin_context()

    def test_init(self):
        self.get_storage_driver()

    def add_rate_fixture(self, context=None, fixture=0, values={}):
        context = context or self.admin_context
        _values = copy.copy(self.rate_fixtures[fixture])
        _values.update(values)
        return self.storage_conn.add_rate(context, _values)

    def add_account_fixture(self, context=None, fixture=0, values={}):
        context = context or self.admin_context
        _values = copy.copy(self.account_fixtures[fixture])
        _values.update(values)
        return self.storage_conn.add_account(context, _values)

    def add_system_account_fixture(self, context=None, fixture=0, values={}):
        context = context or self.admin_context
        _values = copy.copy(self.system_account_fixtures[fixture])
        _values.update(values)
        return self.storage_conn.add_system_account(context, _values)

    def test_add_rate(self):
        rate = self.add_rate_fixture()
        self.assertEquals(rate.name, self.rate_fixtures[0]['name'])
        self.assertEquals(rate.value, self.rate_fixtures[0]['value'])

    def test_delete_rate(self):
        rate = self.add_rate_fixture()
        self.storage_conn.delete_rate(self.admin_context, rate.id)
        with self.assertRaises(exceptions.NotFound):
            self.storage_conn.get_rate(self.admin_context, rate.id)

    def test_update_rate(self):
        rate = self.add_rate_fixture()
        self.storage_conn.update_rate(
            self.admin_context,
            rate.id,
            values={'name': 'memory', 'value': 15})
        self.assertEquals(rate.name, 'memory')
        self.assertEquals(rate.value, 15)

    def test_add_account(self):
        account = self.add_account_fixture()
        self.assertEquals(account.name, self.account_fixtures[0]['name'])

    def test_delete_account(self):
        account = self.add_account_fixture()
        self.storage_conn.delete_account(self.admin_context, account.id)
        with self.assertRaises(exceptions.NotFound):
            self.storage_conn.get_account(self.admin_context, account.id)

    def test_update_account(self):
        account = self.add_account_fixture()
        self.storage_conn.update_account(
            self.admin_context,
            account.id,
            values={'name': 'customer_a'})
        self.assertEquals(account.name, 'customer_a')

    def test_add_system_account(self):
        account = self.add_system_account_fixture()
        self.assertEquals(account.name,
                          self.system_account_fixtures[0]['name'])

    def test_delete_system_account(self):
        account = self.add_system_account_fixture()
        self.storage_conn.delete_system_account(self.admin_context, account.id)
        with self.assertRaises(exceptions.NotFound):
            self.storage_conn.get_system_account(self.admin_context,
                                                 account.id)

    def test_update_system_account(self):
        account = self.add_system_account_fixture()
        self.storage_conn.update_system_account(
            self.admin_context,
            account.id,
            values={'name': 'system_b'})
        self.assertEquals(account.name, 'system_b')
