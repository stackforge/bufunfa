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
