from flask import Flask, escape, request, jsonify, render_template, Response
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
import schedule
from datetime import datetime,date
import time
# import pandas as pd
from flask_cors import CORS
from pymongo import MongoClient
from flask_pymongo import PyMongo
import json 
from bson import ObjectId
from collections import Iterable
from bson import json_util
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

# from mongoengine import MongoEngineJSONEncode

# class MongoengineEncoder(json.JSONEncoder):

#     def default(self, obj):
#         if isinstance(obj, Iterable):
#             out = {}
#             for key in obj:
#                 out[key] = getattr(obj, key)
#             return out

#         if isinstance(obj, ObjectId):
#             return unicode(obj)

#         if isinstance(obj, datetime):
#             return str(obj)

#         return json.JSONEncoder.default(self, obj)


# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)

# DB_Conncetion
# client = MongoClient('mongodb://localhost:27017')
# database = client.research_db

app = Flask(__name__, template_folder='templates')
CORS(app)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/research_db"
# mongo = PyMongo(app)

def get_routes(source,dest):    
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)

    driver.implicitly_wait(20)
    parent_han  = driver.window_handles
    try:
        driver.get("https://www.google.com/maps/@6.829237,80.0981046,10z/data=!5m1!1e1")
        inputElement1 = WebDriverWait(driver , 3000).until(lambda driver: driver.find_element_by_class_name("tactile-searchbox-input"))
        inputElement1.send_keys(dest)
        inputElement1.send_keys(u'\ue007')
        directionsButton = driver.find_element_by_class_name("iRxY3GoUYUY__taparea")
        directionsButton.click()

        inputElement2 = WebDriverWait(driver , 3000).until(lambda driver: driver.find_element_by_xpath("//input[@placeholder='Choose starting point, or click on the map...']"))
        inputElement2.send_keys(source)
        inputElement2.send_keys(u'\ue007')

        car=driver.find_element_by_xpath("//div[@class='directions-travel-mode-icon directions-drive-icon']")
        car.click()

        details = driver.find_elements_by_xpath("//div[@class='section-directions-trip-description']")

        number_of_routes = len(details)
        outputList = [];

        for i in range(0, number_of_routes):
            details = driver.find_elements_by_xpath("//div[@class='section-directions-trip-description']")

            link = details[i]                                                
            i = 1
            while i < 6:
                try:
                    link.click()
                    break
                except:
                    pass
                    i = i + 1
                            
            i = 1
            while i < 6:
                try:
                    link.click()
                    break
                except:
                    pass
                    i = i + 1

            time1 = driver.find_element_by_xpath("//h1[@class='section-trip-summary-title']//span[1]//span[1]")
            timeOutput1= time1.text
            distance1 = driver.find_element_by_xpath("//div[@class='section-trip-summary-header']//span[1]//span[2]")
            disOutput1= distance1.text
            route1= driver.find_element_by_xpath("//h1[@class='section-directions-trip-title']/child::*")
            routeOutput1= route1.text
            # descr1= driver.find_element_by_xpath("//span[@class='renderable-component-text renderable-component-text-not-line']")
            # descrOutput1= descr1.text
            time.sleep(1)                                       
            backButton=driver.find_element_by_xpath("//button[@class='section-trip-header-back maps-sprite-common-arrow-back-white']")
            backButton.click()
            today = datetime.now()
            day=today.strftime("%A")
            hour=today.strftime("%H")
            minute=today.strftime("%M")
            outputList.append({
                "source": source,
                "destination": dest,
                "day": today.strftime("%A"),
                "current time": today.strftime("%X"),
                "time": timeOutput1,
                "distance": disOutput1,
                "route": routeOutput1,
                # "description": descrOutput1
            })        

        # database.traffic_data.insert(outputList)
        # mongo.db.traffic_data.insert(outputList)
        db.child("traffic").child(source+" to "+dest).child(day).child(hour+":"+minute).push(outputList)

    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

    driver.close()
    
    return outputList;

@app.route('/')
def script():
    source = request.args.get('source')
    destination = request.args.get('dest')
    try:
        routes = get_routes(source, destination)
    except:
        print('error')

    schedule.every().minute.at(":45").do(lambda: get_routes(source, destination))
    while True:
        schedule.run_pending()
        time.sleep(1)

    # return Response(json.dumps(routes), mimetype='application/json')
    print(type(routes))
    # return MongoengineEncoder (routes)
    # return JSONEncoder.get_routes(source, destination)
    return jsonify(routes)
    # return routes
    # return json.encode(routes, cls=JSO NEncoder)
    # JSONEncoder().encode(routes)
    # return MongoEngineJSONEncode (routes)

@app.route('/home')
def home():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)