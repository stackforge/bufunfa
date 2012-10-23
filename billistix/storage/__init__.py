# Copyright 2012 Bouvet ASA
#
# Author: Endre Karlson <endre.karlson@bouvet.no>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from stevedore import driver

from billistix.openstack.common import cfg
from billistix.openstack.common import log

from urlparse import urlparse

LOG = log.getLogger(__name__)

STORAGE_ENGINE_NAMESPACE = 'billistix.storage'

cfg.CONF.register_opts([
    cfg.StrOpt('database_connection',
                default='sqlite:///billistix.db',
                help='The database driver to use'),
])


def register_opts(conf):
    p = get_engine(conf)
    p.register_opts(conf)


def get_engine(conf):
    engine_name = urlparse(conf.database_connection).scheme
    LOG.debug('looking for %r driver in %r',
            engine_name, STORAGE_ENGINE_NAMESPACE)
    mgr = driver.DriverManager(STORAGE_ENGINE_NAMESPACE,
                                engine_name,
                                invoke_on_load=True)
    return mgr.driver


def get_connection(conf):
    engine = get_get_engine(conf)
    engine.register_opts(conf)
    return engine.get_connection(conf)


def reinitialize(*args, **kwargs):
    """ Reset the DB to default - Used for testing purposes """
    from billistix.database.sqlalchemy.session import reset_session
    reset_session(*args, **kwargs)
