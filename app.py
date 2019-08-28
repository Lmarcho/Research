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