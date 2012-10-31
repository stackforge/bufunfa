from billistix.openstack.common import cfg
from billistix.openstack.common import log as logging
from billistix.openstack.common.rpc.proxy import RpcProxy

DEFAULT_VERSION = "1.0"

LOG = logging.getLogger(__name__)
RPC = RpcProxy(cfg.CONF.central_topic, DEFAULT_VERSION)


def add_rate(context, values):
    msg = {
        "method": "add_rate",
        "args": {
            "values": values
        }
    }
    return RPC.call(context, msg)


def get_rates(context):
    msg = {
        "method": "get_rates",
    }
    return RPC.call(context, msg)


def update_rate(context, rate_id, values):
    msg = {
        "method": "update_rate",
        "args": {
            "rate_id": rate_id,
            "values": values
        }
    }
    return RPC.call(context, msg)


def delete_rate(context, rate_id):
    msg = {
        "method": "delete_rate",
        "args": {
            "rate_id": rate_id
        }
    }
    return RPC.call(context, msg)


def process_record(context, values):
    msg = {
        "method": "process_record",
        "args": {
            "values": values
        }
    }
    return RPC.call(context, msg)
