# Copyright 2012 Bouvet ASA
#
# Author: Endre Karlson <endre.karlson@bouvet.no>
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
# NOTE(zykes): Copied verbatim from Moniker
from bufunfa.openstack.common import cfg
from bufunfa.openstack.common import log
from bufunfa.openstack.common import timeutils
from bufunfa.openstack.common.rpc import service as rpc_service
from bufunfa import exceptions
from bufunfa import storage
from bufunfa import utils


LOG = log.getLogger(__name__)


class Service(rpc_service.Service):
    def __init__(self, *args, **kw):
        kw.update(
            host=cfg.CONF.host,
            topic=cfg.CONF.central_topic)

        super(Service, self).__init__(*args, **kw)

        self.storage_conn = storage.get_connection(cfg.CONF)

    def add_rate(self, context, values):
        return self.storage_conn.add_rate(context, values)

    def get_rate(self, context, rate_id):
        return self.storage_conn.get_rate(context, rate_id)

    def get_rates(self, context):
        return self.storage_conn.get_rates(context)

    def update_rate(self, context, rate_id, values):
        return self.storage_conn.update_rate(context, rate_id, values)

    def delete_rate(self, context, rate_id):
        return self.storage_conn.delete_rate(context, rate_id)

    def add_account(self, context, values):
        return self.storage_conn.add_account(context, values)

    def get_account(self, context, account_id):
        return self.storage_conn.get_account(context, account_id)

    def get_accounts(self, context):
        return self.storage_conn.get_accounts(context)

    def update_account(self, context, account_id, values):
        return self.storage_conn.update_account(context, account_id, values)

    def delete_account(self, context, account_id):
        return self.storage_conn.delete_rate(context, account_id)

    def add_system_account(self, context, values):
        return self.storage_conn.add_system_account(context, values)

    def get_system_account(self, context, account_id):
        return self.storage_conn.get_system_account(context, account_id)

    def get_system_accounts(self, context):
        return self.storage_conn.get_system_accounts(context)

    def update_system_account(self, context, account_id, values):
        return self.storage_conn.update_account(context, account_id, values)

    def delete_system_account(self, context, account_id):
        return self.storage_conn.delete_rate(context, account_id)

    def set_polled_at(self, context, account_id, time):
        """
        Set when the account was last polled in the system

        :param context: RPC context
        :param account_id: The Account ID in the System
        :param time_stamp: Timestamp of when it was polled
        """
        time = timeutils.parse_strtime(time)

        account = self.storage_conn.get_system_account(context, account_id)
        polled_at = account['polled_at']

        if polled_at and time < polled_at:
            raise exceptions.TooOld("Timestamp is older then the last poll")

        return self.storage_conn.update_system_account(context, account_id,
            {'polled_at': time})

    def process_records(self, context, records):
        """
        Process records in a batch

        :param context: RPC context
        :param records: A list of records
        """
        for record in records:
            self.process_record(context, record)

    def process_record(self, context, values):
        """
        Process a Record

        :param context: RPC context
        :param values: Values for the record
        """
        # NOTE: Add the system if it doesn't exist..
        try:
            self.storage_conn.get_system_account(
                context, values['account_id'])
        except exceptions.NotFound:
            self.storage_conn.add_system_account(
                context,
                {'id': values['account_id']})

        self.storage_conn.add_record(context, values)
