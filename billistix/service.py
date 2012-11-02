#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright © 2012 eNovance <licensing@enovance.com>
#
# Author: Julien Danjou <julien@danjou.info>
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
from billistix.openstack.common import cfg
from billistix.openstack.common import context
from billistix.openstack.common.rpc import service as rpc_service


"""
Module for base services
"""


cfg.CONF.register_opts([
    cfg.IntOpt('periodic_interval',
               default=600,
               help='seconds between running periodic tasks')
])


class PeriodicService(rpc_service.Service):
    def start(self):
        super(PeriodicService, self).start()
        admin_context = context.RequestContext('admin', 'admin', is_admin=True)
        self.tg.add_timer(cfg.CONF.periodic_interval,
                self.manager.periodic_tasks,
                context=admin_context)
