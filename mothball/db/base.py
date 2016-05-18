import abc

class DatabaseBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def connect(self):
        return

    @abc.abstractmethod
    def close(self):
        return

    @abc.abstractmethod
    def update(self):
        return

