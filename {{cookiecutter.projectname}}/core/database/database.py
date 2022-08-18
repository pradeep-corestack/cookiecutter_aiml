import urllib.parse
from abc import ABCMeta
from abc import abstractmethod

import pymongo
from loguru import logger
from oslo_config import cfg
from pymongo import MongoClient

from config import config

logger.add("logs/{}.log".format(__name__), filter=__name__, rotation="1 week")


mongo_client = None


class MongoDBClient:
    def __init__(self, client_config):
        self.mongo_client = None
        self.config = client_config

    def __fetch_uri_for_config(self):
        if self.config.replica_set_name and self.config.replica_set_hosts:
            if all([self.config.username, self.config.password, self.config.auth_database]):
                uri = "mongodb://{username}:{password}@{host}:{port},{replica_set_hosts}/{auth_database}"
            else:
                uri = "mongodb://{username}:{port},{replica_set_hosts}"
        else:
            if all([self.config.username, self.config.password, self.config.auth_database]):
                uri = "mongodb://{username}:{password}@{host}:{port}/?authSource={auth_database}&readPreference=secondaryPreferred"
            elif self.config.username and self.config.password:
                uri = (
                    "mongodb://{username}:{password}@{host}:{port}/?authSource=admin&readPreference=secondaryPreferred"
                )
            else:
                uri = "mongodb://{host}:{port}"
        # logger.debug("mongodb uri - {}".format(uri))
        return uri

    def connect(self):
        try:
            if not self.mongo_client:
                # if password present in config parse with urllib's parser
                if self.config.password:
                    self.config.update({"password": urllib.parse.quote_plus(self.config.password)})
                mongo_uri = self.__fetch_uri_for_config()
                mongo_client = MongoClient(mongo_uri, maxPoolSize=200)
                logger.info("connected with MongoDB client")
        except pymongo.errors.ConnectionFailure as e:
            logger.error("Could not connect to server: %s" % e)

        return mongo_client

    def check_connect(self):
        self.mongo_client.server_info()

    def close(self):
        self.mongo_client.close()


class CollectionBase(object, metaclass=ABCMeta):
    def __init__(self, collection):
        self.collection = collection


class Database(object, metaclass=ABCMeta):
    def __init__(self, client_config):
        self.db = None
        self.config = client_config
        self.mongo_client = None

    @abstractmethod
    def connect(self, db_name: str):
        if not self.mongo_client:
            mongo_client = MongoDBClient(self.config).connect()
        self.db = mongo_client[db_name]

    def check_connection(self):
        try:
            self.mongo_client.server_info()
            return True
        except Exception as err:
            logger.error("check_connection failed due to {}".format(err))
            return False

    def check_collection_exists(self, collection):
        """Check if the passed in collection exists in mongo db"""

        # First get list of all the collections in mongo db
        return collection in self.db.list_collection_names()
