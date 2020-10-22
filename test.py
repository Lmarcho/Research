from datetime import date,datetime
import  schedule
import time

today = datetime.now()
print("Today's date:", today)
print(today.strftime("%A"))
def job():
    print("I'm working...")

# schedule.every().minutes.at(':15').do(job) and schedule.every().minutes.at(':18').do(job)
# schedule.every().days.at("20:16").do(job)
run =schedule.every(2).to(5).seconds.do(job)
timesa=today.strftime("%X")
print (timesa)
print (type(timesa))
if(timesa =="20:35:00"):
    print ("fuck u")
    

while True:
    schedule.run_pending()
    time.sleep(1)