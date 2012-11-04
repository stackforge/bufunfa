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
# NOTE(zykes): Copied verbatim from Moniker
import copy
from uuid import uuid4
from urlparse import urlparse

from sqlalchemy import Column, DateTime, Unicode, Float, Integer, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, backref, object_mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from bufunfa import exceptions
import bufunfa.openstack.common.cfg as cfg
from bufunfa.openstack.common import log
from bufunfa.openstack.common import timeutils
from bufunfa.storage.impl_sqlalchemy.session import get_session
from bufunfa.storage.impl_sqlalchemy.types import JSONBlob, UUID

LOG = log.getLogger(__name__)

sql_opts = [
    cfg.IntOpt('mysql_engine', default='InnoDB', help='MySQL engine')
]

cfg.CONF.register_opts(sql_opts)


def table_args():
    engine_name = urlparse(cfg.CONF.database_connection).scheme
    if engine_name == 'mysql':
        return {'mysql_engine': cfg.CONF.mysql_engine}
    return None


class Base(object):
    __abstract__ = True

    id = Column(UUID, default=uuid4, primary_key=True)

    created_at = Column(DateTime, default=timeutils.utcnow)
    updated_at = Column(DateTime, onupdate=timeutils.utcnow)

    __table_args__ = table_args()
    __table_initialized__ = False

    def save(self, session):
        """ Save this object """
        session.add(self)

        try:
            session.flush()
        except IntegrityError, e:
            if 'is not unique' in str(e):
                raise exceptions.Duplicate(str(e))
            else:
                raise

    def delete(self, session):
        """ Delete this object """
        session.delete(self)
        session.flush()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __iter__(self):
        columns = dict(object_mapper(self).columns).keys()
        # NOTE(russellb): Allow models to specify other keys that can be looked
        # up, beyond the actual db columns.  An example would be the 'name'
        # property for an Instance.
        if hasattr(self, '_extra_keys'):
            columns.extend(self._extra_keys())
        self._i = iter(columns)
        return self

    def next(self):
        n = self._i.next()
        return n, getattr(self, n)

    def update(self, values):
        """ Make the model object behave like a dict """
        for k, v in values.iteritems():
            setattr(self, k, v)

    def iteritems(self):
        """
        Make the model object behave like a dict.

        Includes attributes from joins.
        """
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                      if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()


Base = declarative_base(cls=Base)


class Account(Base):
    """
    A way to correlate multiple tenants or future Domains in OpenStack into
    a single aggregation point
    """
    __tablename__ = 'accounts'
    name = Column(Unicode(100), nullable=False)


class SystemAccount(Base):
    """
    Bind a System's Account representation to a Account

    Examples:
        OpenStack Domain or Tenant to a Account
        Credit card Account representation to a Account

    id: The ID of the account in the System
    name: The name of the system

    account_id: The ID of the Account internally
    """
    __tablename__ = "system_accounts"

    id = Column(Unicode(40), primary_key=True)
    name = Column(Unicode(100))

    account = relationship("Account", backref="systems")
    account_id = Column(UUID, ForeignKey('accounts.id'))


class Record(Base):
    __tablename__ = 'records'

    resource_id = Column(Unicode(80), nullable=False)
    type = Column(Unicode(80), nullable=False)
    volume = Column(Float, nullable=False)
    extra = Column(JSONBlob, nullable=True)
    start_timestamp = Column(DateTime)
    end_timestamp = Column(DateTime)

    account = relationship("SystemAccount", backref="records")
    account_id = Column(Unicode(100),
                                ForeignKey('system_accounts.id'),
                                nullable=False)


class Rate(Base):
    """
    The rate to charge for something
    """
    __tablename__ = 'rates'

    name = Column(Unicode(60), nullable=False, unique=True)
    value = Column(Float, nullable=False)
