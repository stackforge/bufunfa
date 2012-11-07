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
import random
from bufunfa.openstack.common import log as logging
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

    def setUp(self):
        super(ServiceTest, self).setUp()
        self.config(rpc_backend='bufunfa.openstack.common.rpc.impl_fake')
        self.service = self.get_central_service()
        self.admin_context = self.get_admin_context()

    def test_process_record_unexisting_system(self):
        self.service.process_record(
            self.admin_context, self.record)

        system = self.service.storage_conn.get_system_account(
            self.admin_context, self.record['account_id'])
        self.assertEquals(system.id, self.record['account_id'])
