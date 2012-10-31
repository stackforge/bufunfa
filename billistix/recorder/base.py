import abc


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

        resource_id: The ID of the resource that's billed (External ID typically)
        type: The type, application, instance, network etc
        volume: The volume that's currently pulled
        metadata: JSON
        start_timestamp: Start of the pulling period
        end_timestamp: End of the pulling period
        customer_system_id: The customer id in the external system
        """
