import requests
import time
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from os import path, makedirs
from botmodules import *

try:
    sqlite_connection = sqlite3.connect('data/data.db')
    cursor = sqlite_connection.cursor()
    cursor.execute( '''CREATE TABLE STEAM (
                                steam_id INT, 
                                game TEXT,
                                total_hour INT,
                                date DATE
                                );''')
except Exception as err:
    print(err)
    with open(filename + '/data/log_bot.txt', "a") as f:
        f.write(str(datetime.datetime.now()) + ' ' + str(err) + '\n')
    pass
    with open(filename + '/data/log.txt', "a") as f:
        f.write(str(datetime.datetime.now()) + '\n')

def status_check():
  r=requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=4E3BDEA65FDF5D811DA6C9C383356A96&steamids=76561197960435530").json()
  print(r["response"]["players"])


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(status_check, 'interval', seconds=3)
    scheduler.start()

    try:
        while True:
            time.sleep(2)
            print('Printing in the main thread.')
    except KeyboardInterrupt:
        pass

scheduler.shutdown()
