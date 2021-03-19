
from pymongo import MongoClient

import config


def get_client_connection():
    return MongoClient(config.DATABASE_URL)
