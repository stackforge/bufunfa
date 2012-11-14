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
from datetime import datetime, timedelta
from bufunfa.openstack.common import log as logging
from bufunfa.openstack.common import timeutils
from bufunfa.tests.test_central import CentralTestCase
from bufunfa import exceptions

LOG = logging.getLogger(__name__)


class ServiceTest(CentralTestCase):
    __test__ = True

    record = {
        'resource_id': '0cc13414-905d-4563-b61a-e80702566fd5',
        'type': 'instance',
        'volume': 3.5,
        'start_timestamp': datetime.now() - timedelta(1),
        'end_timestamp': datetime.now(),
        'account_id': 'c97027dd880d4c129ae7a4ba7edade05'
    }

    rates = [
        {'name': 'cpu', 'value': 1},
        {'name': 'memory', 'value': 2}
    ]

    accounts = [
        {'name': 'customer_a'}
    ]

    system_accounts = [
        {'name': 'system_a', 'id': 'd44f1779-5034-455e-b334-cac2ac3eee33'},
        {'name': 'system_b', 'id': 'a45e43af-090b-4045-ae78-6a9d507d1418'}
    ]

    def setUp(self):
        super(ServiceTest, self).setUp()
        self.config(rpc_backend='bufunfa.openstack.common.rpc.impl_fake')
        self.service = self.get_central_service()
        self.admin_context = self.get_admin_context()

    def add_rate(self, fixture=0, context=None, values={}):
        context = context or self.get_admin_context()
        values = self.rates[fixture]
        values.update(values)
        return self.service.add_rate(context, values)

    def add_account(self, fixture=0, context=None, values={}):
        context = context or self.get_admin_context()
        values = self.accounts[fixture]
        values.update(values)
        return self.service.add_account(context, values)

    def add_system_account(self, fixture=0, context=None, values={}):
        context = context or self.get_admin_context()
        values = self.system_accounts[fixture]
        values.update(values)
        return self.service.add_system_account(context, values)

    def test_process_record_unexisting_system(self):
        """
        If the system we we're receiving a record from doesn't have a system
        account entry we'll create one
        """
        self.service.process_record(
            self.admin_context, self.record)

        system = self.service.storage_conn.get_system_account(
            self.admin_context, self.record['account_id'])
        self.assertEquals(system.id, self.record['account_id'])

    def test_set_polled_at(self):
        """
        Set the last time the SystemAccount was polled
        """
        account_id = str(self.add_system_account()['id'])
        now = datetime.now()
        self.service.set_polled_at(self.admin_context, account_id,
                                   timeutils.strtime(now))

        account = self.service.get_system_account(self.admin_context,
                                                  account_id)
        self.assertEquals(account["polled_at"], now)

    def test_set_polled_at_too_old(self):
        """
        Shouldn't be allowed to set polled_at older then the current one in
        SystemAccount
        """
        account_id = str(self.add_system_account()['id'])
        now = datetime.now()
        self.service.set_polled_at(
            self.admin_context, account_id, timeutils.strtime(now))

        with self.assertRaises(exceptions.TooOld):
            self.service.set_polled_at(
                self.admin_context, account_id,
                timeutils.strtime(now - timedelta(1)))
