from stevedore import driver
from billistix.openstack.common import cfg
from billistix.openstack.common import log

LOG = log.getLogger(__name__)

DRIVER_NAMESPACE = "billistix.recorder"


def get_plugin(conf):
    name = "ceilometer"
    LOG.debug("Looking for driver %s in %s", name, DRIVER_NAMESPACE)
    mgr = driver.DriverManager(DRIVER_NAMESPACE, name, invoke_on_load=True)
    return mgr.driver
