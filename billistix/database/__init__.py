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
from billistix.openstack.common import cfg

cfg.CONF.register_opts([
    cfg.StrOpt('database-driver', default='sqlalchemy',
               help='The database driver to use'),
])


class BaseDatabase(object):
    def get_rates(self, context):
        raise NotImplementedError()

    def add_rate(self, context, name, value):
        raise NotImplementedError()


def get_driver(*args, **kwargs):
    # TODO: Switch to the config var + entry point loading
    from billistix.database.sqlalchemy import Sqlalchemy

    return Sqlalchemy(*args, **kwargs)


def reinitialize(*args, **kwargs):
    """ Reset the DB to default - Used for testing purposes """
    from billistix.database.sqlalchemy.session import reset_session
    reset_session(*args, **kwargs)
