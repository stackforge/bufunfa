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
import os

from billistix.openstack.common import cfg
from billistix.openstack.common import log
from billistix.openstack.common.context import get_admin_context
from billistix.openstack.common.loopingcall import LoopingCall
from billistix.openstack.common.rpc import service as rpc_service
from billistix.recorder import get_plugin
from billistix.central import api


LOG = log.getLogger(__name__)

cfg.CONF.register_opts([
    cfg.IntOpt('periodic_interval',
                default=1,
                help='seconds between running periodic tasks'),
])

CLI_OPTIONS = [
    cfg.StrOpt('os-username',
               default=os.environ.get('OS_USERNAME', 'glance'),
               help='Username to use for openstack service access'),
    cfg.StrOpt('os-password',
               default=os.environ.get('OS_PASSWORD', 'admin'),
               help='Password to use for openstack service access'),
    cfg.StrOpt('os-tenant-id',
               default=os.environ.get('OS_TENANT_ID', ''),
               help='Tenant ID to use for openstack service access'),
    cfg.StrOpt('os-tenant-name',
               default=os.environ.get('OS_TENANT_NAME', 'admin'),
               help='Tenant name to use for openstack service access'),
    cfg.StrOpt('os-auth-url',
               default=os.environ.get('OS_AUTH_URL',
                                      'http://localhost:5000/v2.0'),
               help='Auth URL to use for openstack service access'),
]

cfg.CONF.register_cli_opts(CLI_OPTIONS)


class Service(rpc_service.Service):
    def __init__(self, *args, **kw):
        kw.update(
            host=cfg.CONF.host,
            topic=cfg.CONF.worker_topic)

        super(Service, self).__init__(*args, **kw)

        self.plugin = get_plugin(cfg.CONF)

        self.timers = []

    def start(self):
        task = LoopingCall(self.poll_records)
        task.start(interval=cfg.CONF.periodic_interval,
                initial_delay=cfg.CONF.periodic_interval)
        self.timers.append(task)
        super(Service, self).start()

    def poll_records(self):
        context = get_admin_context()
        records = self.plugin.get_records()
