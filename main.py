import time
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess


def get_api_data():

    scheduler = BackgroundScheduler()
    scheduler.remove_all_jobs()
    current_year = datetime.now().year

    michigan_football_api = "https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/teams/130"
    football_response = requests.get(michigan_football_api)
    next_football_date = ""
    next_football_link = ""
    if football_response.status_code == 200:
        try:
            data = football_response.json()
            next_football_date = (data['team']['nextEvent'][0]['competitions'][0]['status']['type']['shortDetail'])
            next_football_link = (data["team"]["nextEvent"][0]["links"][0]["href"])
            date_str_with_year = f"{current_year} {next_football_date}"
            format_str = "%Y %m/%d - %I:%M %p %Z"
            dt = datetime.strptime(date_str_with_year, format_str)
            game_today = dt.date() == datetime.now().date()

            #if(game_today):
               #scheduler.add_job(run_foolball, 'date', run_date=test_date, args=[dt, next_football_link])
        except:
            print("No Football Game Coming Up")
    else:
        print("Error:", football_response.status_code)

    michigan_basketball_api = "https://site.web.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/130"
    basketball_response = requests.get(michigan_basketball_api)
    next_basketball_date = ""
    next_basketball_link = ""
    if basketball_response.status_code == 200:
        try:
            data = basketball_response.json()
            next_basketall_date = (data['team']['nextEvent'][0]['competitions'][0]['status']['type']['shortDetail'])
            next_basketball_link = (data["team"]["nextEvent"][0]["links"][0]["href"])
            date_str_with_year = f"{current_year} {next_basketall_date}"
            format_str = "%Y %m/%d - %I:%M %p %Z"
            dt = datetime.strptime(date_str_with_year, format_str)
            #today_date = datetime.now()
            #test_date = today_date.replace(minute=51, second=0)
            game_today = dt.date() == datetime.now().date()
            game_today = True

            if(game_today):
                scheduler.add_job(run_basketball, 'date', run_date=dt, args=[dt, next_basketball_link], misfire_grace_time=300)
                for job in scheduler.get_jobs():
                    print(job)
        except Exception as e:
            print("No Basketball Game Coming Up", e)
    else:
        print("Error:", basketball_response.status_code)
    
    print("Scheduler started")
    scheduler.start()

    while scheduler.get_jobs():
        time.sleep(5)

    print("All jobs completed. Shutting down scheduler.")
    scheduler.shutdown()
    print("Scheduler ended")
    return


def run_basketball(dt, link):
    subprocess.run(["python3", "basketball.py", str(dt), link])
    
def run_foolball(dt, link):
    subprocess.run(["python3", "football.py", str(dt), link])
    

def main():
    get_api_data()

if __name__ == "__main__":
    main()
