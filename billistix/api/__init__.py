import flask.helpers

from billistix.openstack.common import cfg
from billistix.openstack.common import jsonutils

# Replace the json module used by flask with the one from
# openstack.common so we can take advantage of the fact that it knows
# how to serialize more complex objects.
flask.helpers.json = jsonutils

# Register options for the service
API_SERVICE_OPTS = [
    cfg.IntOpt('listen_port',
                default=9001,
                help='The port for the billistix API server'),
]
cfg.CONF.register_opts(API_SERVICE_OPTS)
