# imports
from abc import ABCMeta, abstractmethod

from core.config.config import ConfigSetup
from core.database.billingdb import BillingDB


class SanityCheck(object, metaclass=ABCMeta):
    @abstractmethod
    def run():
        raise NotImplementedError()


class CheckDBConnection(SanityCheck):
    @staticmethod
    def run():
        ConfigSetup().init()
        db = BillingDB()
        db.check_connection()


class CheckCollectionExists(SanityCheck):
    @staticmethod
    def run():
        pass
