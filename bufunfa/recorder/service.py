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
from stevedore.named import NamedExtensionManager

from bufunfa.openstack.common import cfg
from bufunfa.openstack.common import log
from bufunfa.openstack.common.context import get_admin_context
from bufunfa.openstack.common.rpc.service import Service
from bufunfa.central import api as central_api
from bufunfa.recorder.base import RecordEngine


LOG = log.getLogger(__name__)

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


cfg.CONF.register_opts([
    cfg.ListOpt('record-engines', default=[], help="What engines to enable")
])


class RecordService(Service):
    def __init__(self, *args, **kw):
        kw.update(
            host=cfg.CONF.host,
            topic=cfg.CONF.worker_topic)

        super(RecordService, self).__init__(*args, **kw)

        self.admin_context = get_admin_context()

        self.engines = self._init_extensions()

    def _init_extensions(self):
        """ Loads and prepares all enabled extensions """
        self.extensions_manager = NamedExtensionManager(
            RecordEngine.__plugin_ns__, names=cfg.CONF.record_engines)

        def _load_extension(ext):
            handler_cls = ext.plugin
            handler_cls.register_opts(cfg.CONF)
            return handler_cls(record_service=self)

        try:
            return self.extensions_manager.map(_load_extension)
        except RuntimeError:
            # No handlers enabled. No problem.
            return []

    def start(self):
        """
        Start underlying engines
        """
        super(RecordService, self).start()
        for engine in self.engines:
            engine.start()

    def stop(self):
        """
        Stop underlying engines
        """
        super(RecordService, self).stop()
        for engine in self.engines:
            engine.stop()

    def publish_records(self, context, records):
        """
        Publish a record to the central service

        :param record: The record
        """
        return central_api.process_records(context, records)
