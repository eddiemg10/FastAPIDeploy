from pymongo  import MongoClient
from app.core.config import settings

connection_string = settings.MONGODB_ATLAS_CONNECTION_STRING
if not connection_string:
    raise ValueError("Missing MONGODB_ATLAS_CONNECTION_STRING environment variable")

mongo_client = MongoClient(connection_string)
db = mongo_client.NourishKe

def get_database():
    return db
