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
from bufunfa.openstack.common import log as logging
from bufunfa.openstack.common.rpc.proxy import RpcProxy

DEFAULT_VERSION = "1.0"

LOG = logging.getLogger(__name__)
RPC = RpcProxy(cfg.CONF.central_topic, DEFAULT_VERSION)


def add_rate(context, values):
    msg = {
        "method": "add_rate",
        "args": {
            "values": values
        }
    }
    return RPC.call(context, msg)


def get_rate(context, rate_id):
    msg = {
        "method": "get_rate",
        "args": {
            "rate_id": rate_id
        }
    }
    return RPC.call(context, msg)


def get_rates(context):
    msg = {
        "method": "get_rates",
    }
    return RPC.call(context, msg)


def update_rate(context, rate_id, values):
    msg = {
        "method": "update_rate",
        "args": {
            "rate_id": rate_id,
            "values": values
        }
    }
    return RPC.call(context, msg)


def delete_rate(context, rate_id):
    msg = {
        "method": "delete_rate",
        "args": {
            "rate_id": rate_id
        }
    }
    return RPC.call(context, msg)


def add_account(context, values):
    msg = {
        "method": "add_account",
        "args": {
            "values": values
        }
    }
    return RPC.call(context, msg)


def get_account(context, account_id):
    msg = {
        "method": "get_account",
        "args": {
            "account_id": account_id
        }
    }
    return RPC.call(context, msg)


def get_accounts(context):
    msg = {
        "method": "get_accounts",
    }
    return RPC.call(context, msg)


def update_account(context, account_id, values):
    msg = {
        "method": "update_account",
        "args": {
            "account_id": account_id,
            "values": values
        }
    }
    return RPC.call(context, msg)


def delete_account(context, account_id):
    msg = {
        "method": "delete_account",
        "args": {
            "account_id": account_id
        }
    }
    return RPC.call(context, msg)


def add_system_account(context, values):
    msg = {
        "method": "add_system_account",
        "args": {
            "values": values
        }
    }
    return RPC.call(context, msg)


def get_system_account(context, account_id):
    msg = {
        "method": "get_system_account",
        "args": {
            "account_id": account_id
        }
    }
    return RPC.call(context, msg)


def get_system_accounts(context):
    msg = {
        "method": "get_system_accounts",
    }
    return RPC.call(context, msg)


def update_system_account(context, account_id, values):
    msg = {
        "method": "update_system_account",
        "args": {
            "account_id": account_id,
            "values": values
        }
    }
    return RPC.call(context, msg)


def delete_system_account(context, account_id):
    msg = {
        "method": "delete_system_account",
        "args": {
            "account_id": account_id
        }
    }
    return RPC.call(context, msg)


def set_polled_at(context, account_id, time):
    msg = {
        "method": "set_polled_at",
        "args": {
            "account_id": account_id,
            "time": time
        }
    }
    return RPC.call(context, msg)


def process_record(context, values):
    msg = {
        "method": "process_record",
        "args": {
            "values": values
        }
    }
    return RPC.call(context, msg)


def process_records(context, records):
    msg = {
        'method': 'process_records',
        'args': {
            'records': records
        }
    }
    return RPC.call(context, msg)
