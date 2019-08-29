from datetime import date,datetime
import  schedule
import time

today = datetime.now()
print("Today's date:", today)
print(today.strftime("%A"))
def job():
    print("I'm working...")
schedule.every().hour.at(":30").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)