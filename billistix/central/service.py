from billistix.openstack.common import cfg
from billistix.openstack.common import log
from billistix.openstack.common.rpc import service as rpc_service
from billistix import storage


LOG = log.getLogger(__name__)


class Service(rpc_service.Service):
    def __init__(self, *args, **kw):
        kw.update(
            host=cfg.CONF.host,
            topic=cfg.CONF.central_topic)

        super(Service, self).__init__(*args, **kw)

        self.storage_conn = storage.get_connection(cfg.CONF)

    def add_rate(self, context, values):
        return self.storage_conn.add_rate(context, values)

    def get_rates(self, context):
        return self.storage_conn.get_rates(context)

    def update_rate(self, context, rate_id, values):
        return self.storage_conn.update_rate(context, rate_id, values)

    def delete_rate(self, context, rate_id):
        return self.storage_conn.delete_rate(context, rate_id)
