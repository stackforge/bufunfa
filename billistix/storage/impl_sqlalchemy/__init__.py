import copy

from billistix.openstack.common import log
from billistix.storage import base
from billistix.storage.impl_sqlalchemy import models
from billistix.storage.impl_sqlalchemy.session import get_session

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

    def create_rate(self, context, values, session=None):
        rate = models.Rate()
        rate.update(values)
        rate.save()
        return rate

    def get_rates(self, context, session=None):
        query = self.session.query(models.Rate)
        return [row2dict(row) for row in query.all()]


def model_query(*args, **kw):
    session = kw.get("session") or get_session()
    query = session.query(*args)
    return query


def row2dict(row):
    d = copy.copy(row.__dict__)
    for col in ['_sa_instance_state']:
        if col in d:
            del d[col]
    return d
