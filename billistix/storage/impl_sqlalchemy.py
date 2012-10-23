import copy
import datetime

from billistix.openstack.common import cfg
from billistix.openstack.common import log
from billistix.storage import base
from billistix.storage.sqlalchemy.models import Base, Rate
from billistix.storage.sqlalchemy.session import get_session
import billistix.storage.sqlalchemy.session as session

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
        return

    def _get_connection(self, conf):
        """
        Return a connection to the database.
        """
        return session.get_session()

    def register_models(self):
        Base.metadata.create_all(self.session.bind)

    def get_rates(self, context, session=None):
        q = self.session.query(models.Rate)
        return [row2dict(row) for row in q.all()]


def model_query(*args, **kw):
    session = kwargs.get("session") or get_session()
    q = session.query(*args)
    return query


def row2dict(row):
    d = copy.copy(row.__dict__)
    for col in ['_sa_instance_state']:
        if col in d:
            del d[col]
    return d
