import copy

from billistix import exceptions
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

    def add_rate(self, context, values, session=None):
        rate = models.Rate()
        rate.update(values)
        rate.save(self.session)
        return rate

    def get_rates(self, context, session=None):
        query = self.session.query(models.Rate)
        return [row2dict(row) for row in query.all()]

    def update_rate(self, context, rate_id, values):
        rate = self._get_id(context, model, rate_id)
        rate.update(values)
        try:
            rate.save(self.session)
        except exceptions.Duplicate:
            raise
        return dict(rate)

    def delete_rate(self, context, rate_id):
        rate = self._get_id(context, rate_id)
        rate.delete(self.session)


def row2dict(row):
    d = copy.copy(row.__dict__)
    for col in ['_sa_instance_state']:
        if col in d:
            del d[col]
    return d
