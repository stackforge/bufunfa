import ceilometerclient

from billistix.openstack.common import log
from billistix.recorder.openstack import OpenstackEngine

LOG = log.getLogger(__name__)


class RecordEngine(OpenstackEngine):
    def get_client(self):
        """
        Get a ceilometerclient
        """
        keystone_client = self.get_ksclient()
        return ceilometerclient.Client(keystone_client=keystone_client)

    def get_records(self):
        records = []

        try:
            self.client = self.get_client()
            projects = self.client.get_projects()
        except Exception, e:
            LOG.exception(e)
            return

        for project_id in projects:
            if project_id is None:
                continue
            for record in self.get_project_records(project_id):
                import pprint
                print pprint.pformat(record)
                records.append(record)
        return records

    def get_project_records(self, project_id):
        records = []
        for resource in self.client.get_resources(project_id=project_id):
            meters = [item.get('counter_name') for item in resource['meter']]
            for meter in meters:
                type_, volume, metadata = self.get_meter_data(resource, meter)

                if type_ is not None:
                    duration_info = self.client.get_resource_duration_info(
                        resource_id=resource['resource_id'],
                        meter=meter,
                    )
                    record = dict(
                        resource_id=resource['resource_id'],
                        type=type_,
                        volume=volume,
                        extra=metadata,
                        start_timestamp=duration_info.get('start_timestamp'),
                        end_timestamp=duration_info.get('end_timestamp'),
                        duration=duration_info.get('duration')
                    )
                    records.append(record)
        LOG.debug("Returning %d records", len(records))
        return records

    def get_meter_data(self, resource, meter):
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
            metadata['ips'] = ','.join([item['ip_address'] \
                for item in resource['metadata'].get('fixed_ips', []) \
                    if 'ip_address' in item])
        return type_, volume, metadata
