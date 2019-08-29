
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

import pyrebase

config = {
    "apiKey": "AIzaSyA2CU0xOpT1kXXSKEDeuLc8Rf604kCiWj8",
    "authDomain": "researchdb-39220.firebaseapp.com",
    "databaseURL": "https://researchdb-39220.firebaseio.com",
    "projectId": "researchdb-39220",
    "storageBucket": "researchdb-39220.appspot.com",
    "messagingSenderId": "33539234789",
    "appId": "1:33539234789:web:264cb7f4ad23c724"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
db.child("names").push({"name":"Lakshitha"})

