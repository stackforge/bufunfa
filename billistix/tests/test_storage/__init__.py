# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
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

    def setUp(self):
        super(StorageDriverTestCase, self).setUp()
        self.storage_conn = self.get_storage_driver()
        self.admin_context = self.get_admin_context()

    def test_init(self):
        self.get_storage_driver()

    def test_add_rate(self):
        values = {"name": "cpu_hour", "value": 1}
        rate = self.storage_conn.create_rate(self.admin_context, values=values)
        self.assertEquals(rate.name, "cpu_hour")
        self.assertEquals(rate.value, 1)
        self.storage_conn.get_rates(self.admin_context)

    def test_add_rate2(self):
        values = {"name": "cpu_hour", "value": 1}
        rate = self.storage_conn.create_rate(self.admin_context, values=values)
        self.assertEquals(rate.name, "cpu_hour")
        self.assertEquals(rate.value, 1)
        self.storage_conn.get_rates(self.admin_context)

        from billistix.storage.sqla import models
        test = models.Test(name="test")
        rate.test = [test]
        rate.save()
        #rate.tset = test
