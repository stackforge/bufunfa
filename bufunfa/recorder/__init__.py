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
from stevedore import driver
from bufunfa.openstack.common import cfg
from bufunfa.openstack.common import log

LOG = log.getLogger(__name__)

DRIVER_NAMESPACE = "bufunfa.recorder"


def get_plugin(conf):
    name = "ceilometer"
    LOG.debug("Looking for driver %s in %s", name, DRIVER_NAMESPACE)
    mgr = driver.DriverManager(DRIVER_NAMESPACE, name, invoke_on_load=True)
    return mgr.driver
