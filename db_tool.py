import pymongo
import env


def create_mongo_session(host=env.mongo_host, port=env.mongo_port):
    return pymongo.MongoClient(host=host, port=port)
