from urlparse import urlparse

from keystoneclient.v2_0 import client as ksclient

from billistix.openstack.common import cfg
from billistix.recorder.base import RecorderEngine


class OpenstackEngine(RecorderEngine):
    def get_ksclient(self):
        """
        Get a keystone client
        """
        insecure = urlparse(cfg.CONF.os_auth_url).scheme != 'https'
        return ksclient.Client(username=cfg.CONF.os_username,
                               password=cfg.CONF.os_password,
                               tenant_id=cfg.CONF.os_tenant_id,
                               tenant_name=cfg.CONF.os_tenant_name,
                               auth_url=cfg.CONF.os_auth_url,
                               insecure=insecure)
