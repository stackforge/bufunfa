import flask
from billistix.openstack.common import cfg
from billistix.openstack.common import jsonutils
from billistix.api.v1 import blueprint as bp_v1


# Replace the json module used by flask with the one from
# billistix.openstack.common so we can take advantage of the fact that it knows
# how to serialize more complex objects.
flask.helpers.json = jsonutils


cfg.CONF.register_opts([
    cfg.StrOpt('api_host', default='0.0.0.0',
               help='API Host'),
    cfg.IntOpt('api_port', default=9001,
               help='API Port Number'),
    cfg.StrOpt('api_paste_config', default='billistix-api-paste.ini',
               help='File name for the paste.deploy config for billistix-api'),
    cfg.StrOpt('auth_strategy', default='noauth',
               help='The strategy to use for auth. Supports noauth or '
                    'keystone'),
])
