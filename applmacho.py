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
# from dictionary import cities_dic

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

app = Flask(__name__, template_folder='templates')
CORS(app)

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
                "duration": timeOutput1,
                "distance": disOutput1,
                "route": routeOutput1,
            })        

        db.child("traffic").child(source+" to "+dest).child(day).child(hour+":"+minute).push(outputList)

    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

    driver.close()
    
    return outputList;
cities_list=["colombo", "borella", "rajagiriya", "battaramulla", "koswatta", "malabe", "SLIIT","kaduwela"]

@app.route('/')
def script():
    # for i in range (1,len(cities_dic)+1):
    #     source=cities_dic.get("city"+str(i)).get("source")
    #     destination=cities_dic.get("city"+str(i)).get("destination")
    #     print (source)
    #     print(destination)
    #     try:
    #         routes = get_routes(source, destination)
    #         time.sleep(30)
    #     except:
    #         print('error')
    for x in range(0,len(cities_list)):
      for y in range(0,len(cities_list)):
        if x!=y:
            print(cities_list[x]+" to "+cities_list[y])
            source=cities_list[x]
            destination=cities_list[y]
            try:
                routes = get_routes(source, destination)
                time.sleep(30)
            except:
                print('error')

    schedule.every().hour.at(":30").do(lambda: get_routes(source, destination))
    while True:
        schedule.run_pending()
        time.sleep(20)
    print(type(routes))
    return jsonify(routes)

if __name__=='__main__':
    app.run(debug=True)
