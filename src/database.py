
from pymongo import MongoClient

import config


def get_client_connection():
    client = MongoClient(config.DATABASE_URL)
    client.server_info()
    print('Connected to MongoDB server')
    return client