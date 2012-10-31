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
# NOTE(zykes): Copied from Moniker
from paste import deploy
from billistix.openstack.common import log as logging
from billistix.openstack.common import wsgi
from billistix.openstack.common import cfg
from billistix import utils


class Service(wsgi.Service):
    def __init__(self, backlog=128, threads=1000):
        super(Service, self).__init__(threads)

        self.host = cfg.CONF.api_host
        self.port = cfg.CONF.api_port
        self.backlog = backlog

        config_path = cfg.CONF.api_paste_config
        config_path = utils.find_config(config_path)

        self.application = deploy.loadapp("config:%s" % config_path,
                                            name='osapi_billing')

    def start(self):
        return super(Service, self).start(application=self.application,
                                          port=self.port, host=self.host,
                                          backlog=self.backlog)
