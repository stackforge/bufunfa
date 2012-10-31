# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os
import socket
from billistix.openstack.common import cfg


cfg.CONF.register_opts([
    cfg.StrOpt('pybasedir',
               default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '../')),
               help='Directory where the nova python module is installed'),
    cfg.StrOpt('host', default=socket.gethostname(),
               help='Name of this node'),
    cfg.StrOpt('control-exchange', default='billistix',
               help='AMQP exchange to connect to if using RabbitMQ or Qpid'),
    cfg.StrOpt('central-topic', default='billing_central', help='Central Topic'),
    cfg.StrOpt('worker-topic', default='billing_worker', help='Worker Topic'),
    cfg.StrOpt('state-path', default='$pybasedir', help='State Path')
])
