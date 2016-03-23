import pymongo
import settings
from elasticsearch import Elasticsearch

elastic_search_conn = None

def get_elastic_search_connection():
    """
    :return: connection to elastic search server.
    """
    global elastic_search_conn
    if not elastic_search_conn:
        elastic_search_conn = Elasticsearch(settings.LOCAL_ELASTIC_SERVER, timeout=30)
    return elastic_search_conn


def get_mongo_connection():
    """
    :return: connection to mongo server.
    """
    connection = pymongo.MongoClient(settings.LOCAL_MONGO_HOST, settings.MONGO_PORT)
    return connection
