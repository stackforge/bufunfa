import os
from billistix.openstack.common import log as logging
from billistix.openstack.common import cfg
from billistix.openstack.common.notifier import api as notifier_api
from billistix import exceptions

LOG = logging.getLogger(__name__)


def notify(context, service, event_type, payload):
    priority = 'INFO'
    publisher_id = notifier_api.publisher_id(service)

    notifier_api.notify(context, publisher_id, event_type, priority, payload)


def find_config(config_path):
    """
    Find a configuration file using the given hint.

    Code nabbed from cinder.

    :param config_path: Full or relative path to the config.
    :returns: Full path of the config, if it exists.
    :raises: `billistix.exceptions.ConfigNotFound`
    """
    possible_locations = [
        config_path,
        os.path.join("etc", "billistix", config_path),
        os.path.join("etc", config_path),
        os.path.join(cfg.CONF.state_path, "etc", "billistix", config_path),
        os.path.join(cfg.CONF.state_path, "etc", config_path),
        os.path.join(cfg.CONF.state_path, config_path),
        "/etc/billistix/%s" % config_path,
    ]

    for path in possible_locations:
        LOG.debug('Checking path: %s' % path)
        if os.path.exists(path):
            return os.path.abspath(path)
    raise exceptions.ConfigNotFound(config_path)
