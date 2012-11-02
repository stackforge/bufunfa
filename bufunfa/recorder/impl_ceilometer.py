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
# NOTE(zykes): Copied verbatim from ceilometerclient
from datetime import datetime, timedelta

import ceilometerclient

from bufunfa.openstack.common import cfg
from bufunfa.openstack.common import log
from bufunfa.recorder.openstack import OpenstackEngine

LOG = log.getLogger(__name__)


class RecordEngine(OpenstackEngine):
    def get_client(self):
        """
        Get a ceilometerclient
        """
        keystone_client = self.get_ksclient()
        return ceilometerclient.Client(keystone_client=keystone_client)

    def get_records(self):
        """
        Get the records between a period of time
        """
        records = []

        try:
            self.client = self.get_client()
            projects = self.client.get_projects()
        except Exception, e:
            LOG.exception(e)
            return

        poll_start = datetime.now() - timedelta(seconds=cfg.CONF.poll_age)

        for project_id in projects:
            if project_id is None:
                continue
            project_records = self.get_project_records_between(project_id,
                start_timestamp=poll_start)
            for record in project_records:
                records.append(record)
        return records

    def get_project_records_between(self, project_id, start_timestamp=None,
                                    end_timestamp=None):
        """
        Get the given project id's records between given timestamps

        :param project_id: Project ID to get Records for.
        :param start_timestamp: Start timestamp
        :param end_timestamp: End timestamp
        """
        records = []
        for resource in self.client.get_resources(project_id=project_id):
            meters = [item.get('counter_name') for item in resource['meter']]
            for meter in meters:
                record = self.get_record_between(
                    resource, meter,
                    start_timestamp=start_timestamp,
                    end_timestamp=end_timestamp)
                if record is not None:
                    records.append(record)
        LOG.debug("Returning %d records for project %s", len(records),
                  project_id)
        return records

    def get_record_between(self, resource, meter,
                           start_timestamp=None, end_timestamp=None):
        """
        :param resource: A resource in Dict form
        :param meter: Meter name
        :param start_timestamp: Start timestamp
        :param end_timestamp: End timestamp
        """
        # NOTE: No type, skip it. Needs re-amp
        type_, volume, metadata = self._get_meter_data(resource, meter)
        if type_ is None:
            return

        duration_info = self.client.get_resource_duration_info(
            resource_id=resource['resource_id'], meter=meter,
            start_timestamp=start_timestamp, end_timestamp=end_timestamp
        )

        # NOTE: Not sure on this but I think we can skip returning events that
        # don't have volume or duration
        if not volume and not duration_info.get('duration'):
            return

        record = dict(
            resource_id=resource['resource_id'],
            type=type_,
            volume=volume,
            extra=metadata,
            start_timestamp=duration_info.get('start_timestamp'),
            end_timestamp=duration_info.get('end_timestamp'),
            duration=duration_info.get('duration')
        )
        if cfg.CONF.record_audit_logging:
            LOG.debug("Record: %s", record)
        return record

    def _get_meter_data(self, resource, meter):
        """
        :param resource: A resource in Dict form
        :param meter: Meter name
        """
        type_ = None
        volume = resource['metadata'].get('size')
        metadata = {}

        if meter.startswith('instance:'):
            type_ = 'instance'
            metadata['flavor'] = meter.partition(':')[-1]
        elif meter == 'volume.size':
            type_ = 'volume'
            volume = self.client.get_resource_volume_max(
                resource_id=resource['resource_id'],
                meter=meter,
            )
        elif meter == 'image.size':
            type_ = 'image'
        elif meter == 'network':
            type_ = 'network'
        elif meter == 'subnet':
            type_ = 'subnet'
            metadata['network_id'] = resource['metadata'].get('network_id')
            metadata['cidr'] = resource['metadata'].get('cidr')
        elif meter == 'port':
            type_ = 'port'
            metadata['network_id'] = resource['metadata'].get('network_id')
            metadata['mac'] = resource['metadata'].get('mac_address')
            ips = []
            for item in resource['metadata'].get('fixed_ips', []):
                if 'ip_address' in item:
                    ips.append(item['ip_address'])
            metadata['ips'] = ','.join(ips)
        return type_, volume, metadata
