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
from urlparse import urlparse

from keystoneclient.v2_0 import client as ksclient

from bufunfa.openstack.common import cfg
from bufunfa.recorder.base import RecorderEngine


class OpenstackEngine(RecorderEngine):
    def get_ksclient(self):
        """
        Get a keystone client
        """
        insecure = urlparse(cfg.CONF.os_auth_url).scheme != 'https'
        return ksclient.Client(username=cfg.CONF.os_username,
                               password=cfg.CONF.os_password,
                               tenant_id=cfg.CONF.os_tenant_id,
                               tenant_name=cfg.CONF.os_tenant_name,
                               auth_url=cfg.CONF.os_auth_url,
                               insecure=insecure)
