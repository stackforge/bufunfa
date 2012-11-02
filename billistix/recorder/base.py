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
import abc

from billistix.openstack.common import cfg


cfg.CONF.register_opt(
    cfg.BoolOpt('record_audit_logging', default=False,
                help='Logs individual records pr get_records()')
)


cfg.CONF.register_opt(
    cfg.IntOpt('poll_age', default=86400,
                help='How far back to pull data from the source service')
)


class RecorderEngine(object):
    """
    Base Record engine for getting Records from external systems
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_records(self):
        """
        Return a list of billables in the format of
        {
            "resource_id": "0cc13414-905d-4563-b61a-e80702566fd5",
            "type": "instance",
            "volume": 3.41,
            "metadata": "{'test': 1}",
            "start_timestamp": "2012-10-31T08:29:29.574000",
            "end_timestamp": "2012-10-31T08:29:45.574000",
            "customer_system_id": "c97027dd880d4c129ae7a4ba7edade05"
        }

        resource_id: The ID of the resource that's billed
                    (External ID typically)
        type: The type, application, instance, network etc
        volume: The volume that's currently pulled
        metadata: JSON
        start_timestamp: Start of the pulling period
        end_timestamp: End of the pulling period
        customer_system_id: The customer id in the external system
        """
