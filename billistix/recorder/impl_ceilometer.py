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

        client = self.get_client()

        for project_id in client.get_projects():
            if project_id is None:
                continue

            for resource in client.get_resources(project_id=project_id):
                resource_id = resource['resource_id']
                resource_metadata = resource["metadata"]
                meters = [item.get('counter_name') for item in resource['meter']]

                for meter in meters:
                    type_ = None
                    volume = resource_metadata.get('size')
                    metadata = {}

                    if meter.startswith('instance:'):
                        type_ = 'instance'
                        metadata['flavor'] = meter.partition(':')[-1]
                    elif meter == 'volume.size':
                        type_ = 'volume'
                        volume = client.get_resource_volume_max(
                            resource_id=resource_id,
                            meter=meter,
                            )
                    elif meter == 'image.size':
                        type_ = 'image'
                    elif meter == 'network':
                        type_ = 'network'
                    elif meter == 'subnet':
                        type_ = 'subnet'
                        metadata['network_id'] = resource_metadata.get('network_id')
                        metadata['cidr'] = resource_metadata.get('cidr')
                    elif meter == 'port':
                        type_ = 'port'
                        metadata['network_id'] = resource_metadata.get('network_id')
                        metadata['mac'] = resource_metadata.get('mac_address')
                        metadata['ips'] = ','.join([item['ip_address']
                                        for item in resource_metadata.get('fixed_ips', [])
                                        if 'ip_address' in item])

                    if type_ is not None:
                        duration_info = client.get_resource_duration_info(
                            resource_id=resource_id,
                            meter=meter,
                            )

                        record = dict(
                            resource_id=resource_id,
                            type=type_,
                            volume=volume,
                            extra=metadata,
                            start=duration_info.get('start_timestamp'),
                            end_timestamp=duration_info.get('end_timestamp'),
                            duration=duration_info.get('duration')
                        )
                        records.append(record)
                        import pprint
                        print pprint.pformat(record)
        LOG.debug("Returning %d records", len(records))
        return records
