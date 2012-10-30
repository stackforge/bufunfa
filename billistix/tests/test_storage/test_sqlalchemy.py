from billistix.openstack.common import log as logging
from billistix.tests.test_storage import StorageDriverTestCase

LOG = logging.getLogger(__name__)


class SqlalchemyTest(StorageDriverTestCase):
    __test__ = True

    def setUp(self):
        super(SqlalchemyTest, self).setUp()
        self.config(database_connection='sqlite://')
