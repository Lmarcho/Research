
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
database = client.research_db
from mongoengine_jsonencoder import MongoEngineJSONEncode
class MongoengineEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Iterable):
            out = {}
            for key in obj:
                out[key] = getattr(obj, key)
            return out

        if isinstance(obj, ObjectId):
            return unicode(obj)

        if isinstance(obj, datetime):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

