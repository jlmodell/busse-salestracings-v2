import sys
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from constants import BUSSE_SALES_REPS, BUSSE_SALES_REPS_COLLECTIONS, MONGODB_URI


def GET_CLIENT() -> MongoClient:
    return MongoClient(MONGODB_URI)


def GET_DATABASE(client: MongoClient, database: str) -> Database:
    if database == BUSSE_SALES_REPS:
        return client[database]

    return None


def GET_COLLECTION(db: Database, collection_key: str) -> Collection:
    __db_name__ = db.name

    if __db_name__ == BUSSE_SALES_REPS:
        try:
            if collection_key in BUSSE_SALES_REPS_COLLECTIONS.values():
                return db[collection_key]
            elif collection_key in BUSSE_SALES_REPS_COLLECTIONS.keys():
                return db[BUSSE_SALES_REPS_COLLECTIONS[collection_key]]

        except Exception as e:
            print(e)
            sys.exit(1)

    return None
