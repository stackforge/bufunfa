# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
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
# NOTE(zykes): Copied from Moniker / Ceilometer
import copy

from bufunfa import exceptions
from bufunfa.openstack.common import log
from bufunfa.storage import base
from bufunfa.storage.impl_sqlalchemy import models
from bufunfa.storage.impl_sqlalchemy.session import get_session

from pprint import pformat

LOG = log.getLogger(__name__)


class SQLAlchemyStorage(base.StorageEngine):
    OPTIONS = []

    def register_opts(self, conf):
        conf.register_opts(self.OPTIONS)

    def get_connection(self, conf):
        return Connection(conf)


class Connection(base.Connection):
    """
    SQLAlchemy connection
    """

    def __init__(self, conf):
        LOG.info('connecting to %s', conf.database_connection)
        self.session = self._get_connection(conf)
        # NOTE: Need to fix this properly...
        self.setup_schema()

    def _get_connection(self, conf):
        """
        Return a connection to the database.
        """
        return get_session()

    def setup_schema(self):
        """ Semi-Private Method to create the database schema """
        models.Base.metadata.create_all(self.session.bind)

    def teardown_schema(self):
        """ Semi-Private Method to reset the database schema """
        models.Base.metadata.drop_all(self.session.bind)

    def _get_id(self, context, model, id):
        """
        Helper to not write the same code x times
        """
        query = self.session.query(model)
        obj = query.get(id)
        if not obj:
            raise exceptions.NotFound(id)
        else:
            return obj

    def _add(self, context, model, values):
        obj = model()
        obj.update(values)
        obj.save(self.session)
        return obj

    def _update(self, context, model, id, values):
        obj = self._get_id(context, model, id)
        obj.update(values)
        try:
            obj.save(self.session)
        except exceptions.Duplicate:
            raise
        return dict(obj)

    def _add_or_update(self, context, model, values, id=None):
        if id is None:
            return self._add(context, model, values)
        else:
            return self._update(context, model, values, id)

    # NOTE: Rates
    def add_rate(self, context, values, session=None):
        return self._add(context, models.Rate, values)

    def get_rates(self, context, session=None):
        query = self.session.query(models.Rate)
        return [row2dict(row) for row in query.all()]

    def update_rate(self, context, rate_id, values):
        return self._update(context, models.Rate, rate_id, values)

    def delete_rate(self, context, rate_id):
        obj = self._get_id(context, models.Rate, rate_id)
        obj.delete(self.session)

    # NOTE: System Accounts
    def add_system_account(self, context, values, session=None):
        return self._add(context, models.SystemAccount, values)

    def get_system_account(self, context, account_id, session=None):
        return self._get_id(context, models.SystemAccount, account_id)

    def get_systems_account(self, context, session=None):
        query = self.session.query(models.SystemAccount)
        return [row2dict(row) for row in query.all()]

    def update_system_account(self, context, account_id, values):
        return self._update(context, models.SystemAccount, account_id, values)

    def delete_system_account(self, context, account_id):
        obj = self._get_id(context, models.SystemAccount, account_id)
        obj.delete(self.session)

    # NOTE: Records
    def add_record(self, context, values):
        self._add(context, models.Record, values)


def row2dict(row):
    d = copy.copy(row.__dict__)
    for col in ['_sa_instance_state']:
        if col in d:
            del d[col]
    return d
