from paste import deploy
from billistix.openstack.common import log as logging
from billistix.openstack.common import wsgi
from billistix.openstack.common import cfg
from billistix import utils


class Service(wsgi.Service):
    def __init__(self, backlog=128, threads=1000):
        super(Service, self).__init__(threads)

        self.host = cfg.CONF.api_host
        self.port = cfg.CONF.api_port
        self.backlog = backlog

        config_path = cfg.CONF.api_paste_config
        config_path = utils.find_config(config_path)

        self.application = deploy.loadapp("config:%s" % config_path,
                                            name='osapi_billing')

    def start(self):
        return super(Service, self).start(application=self.application,
                                          port=self.port, host=self.host,
                                          backlog=self.backlog)
