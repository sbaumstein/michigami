import time
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import json
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess


def get_api_data():

    scheduler = BackgroundScheduler()
    scheduler.remove_all_jobs()
    current_year = datetime.now().year
    one_hour_from_now = datetime.now() + timedelta(hours=1)

    michigan_football_api = "https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/teams/130"
    football_response = requests.get(michigan_football_api)
    next_football_date = ""
    next_football_link = ""
    if football_response.status_code == 200:
        try:
            data = football_response.json()
            next_football_date = (data['team']['nextEvent'][0]['competitions'][0]['status']['type']['shortDetail'])
            next_football_link = (data["team"]["nextEvent"][0]["links"][0]["href"])
            first_team = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][0]["team"]["shortDisplayName"])
            first_value = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][0]["homeAway"])
            second_team = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][1]["team"]["shortDisplayName"])
            second_value = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][1]["homeAway"])  

            date_str_with_year = parser.parse(f"{current_year} {next_football_date}")
            format_str = "%Y %-m/%d - %I:%M %p %Z"
            dt = datetime.strptime(date_str_with_year, format_str)
            game_today = dt.date() == datetime.now().date()

            if(game_today and datetime.now() <= dt <= one_hour_from_now):
                scheduler.add_job(run_football, 'date', run_date=dt, args=[dt, next_football_link, first_team, first_value, second_team, second_value], misfire_grace_time=300)
                for job in scheduler.get_jobs():
                    print(job)
            else:
                print("No football game until", dt)
        except Exception as e:
            print("Error: No Football Game Coming Up", e)
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
            first_team = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][0]["team"]["shortDisplayName"])
            first_value = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][0]["homeAway"])
            second_team = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][1]["team"]["shortDisplayName"])
            second_value = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][1]["homeAway"])                

            date_str_with_year = f"{current_year} {next_basketall_date}"
            format_str = "%Y %-m/%d - %I:%M %p %Z"
            dt = datetime.strptime(date_str_with_year, format_str)
            game_today = dt.date() == datetime.now().date()
            if(game_today and datetime.now() <= dt <= one_hour_from_now):
                scheduler.add_job(run_basketball, 'date', run_date=dt, args=[dt, next_basketball_link, first_team, first_value, second_team, second_value], misfire_grace_time=300)
                for job in scheduler.get_jobs():
                    print(job)
            else:
                print("No basketbll game until", dt)
        except Exception as e:
            print("Error: No Basketball Game Coming Up", e)
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


def run_basketball(dt, link, first_team, first_value, second_team, second_value):
    subprocess.run(["python3", "basketball.py", str(dt), link, first_team, first_value, second_team, second_value])
    
def run_football(dt, link, first_team, first_value, second_team, second_value):
    subprocess.run(["python3", "football.py", str(dt), link, first_team, first_value, second_team, second_value])
    

def main():
    get_api_data()

if __name__ == "__main__":
    main()
