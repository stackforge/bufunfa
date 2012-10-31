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
from billistix.openstack.common import cfg
from billistix.openstack.common import log
from billistix.openstack.common.rpc import service as rpc_service
from billistix import storage


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

    def get_rates(self, context):
        return self.storage_conn.get_rates(context)

    def update_rate(self, context, rate_id, values):
        return self.storage_conn.update_rate(context, rate_id, values)

    def delete_rate(self, context, rate_id):
        return self.storage_conn.delete_rate(context, rate_id)

    def process_record(self, context, values):
        return self.storage_conn.process_record(context, values)
