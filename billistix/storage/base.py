import abc


class StorageEngine(object):
    """
    Base class for storage engines
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def register_opts(self, conf):
        """
        Register any configuration options used by this engine.
        """

    @abc.abstractmethod
    def get_connection(self, conf):
        """
        Return a Connection instance based on the configuration settings.
        """

class Connection(object):
    """
    A Connection
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, conf):
        """
        Constructor...
        """

    @abc.abstractmethod
    def get_rates(self, context):
        """
        Get all rates
        """
