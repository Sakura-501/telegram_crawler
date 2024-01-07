import pymongo
from .config import config_all

config_all = config_all()


class mongo_latest:
    def __init__(self):
        # mongo_url = "mongodb://{}:{}@{}:{}/?authSource={}".format(config_all.mongo_username,config_all.mongo_password,config_all.mongo_host, config_all.mongo_port,config_all.mongo_database)
        self.client = pymongo.MongoClient(host=config_all.mongo_host,port=int(config_all.mongo_port),username=config_all.mongo_username,password=config_all.mongo_password)
        self.db = self.client[config_all.mongo_database]

    # def create_onion_list_collection(self):
    #     collection_names=self.db.list_collection_names()
    #     if "onion_list" not in collection_names:
    #         tmp_collection=db["onion_list"]
