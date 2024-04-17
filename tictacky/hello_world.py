# cron_job.py
import schedule
import time

def job():
    print("Game Registered Successfully! Game ID: ")

schedule.every(10).seconds.do(job)  # Adjust frequency as needed

while True:
    schedule.run_pending()
    time.sleep(1)
