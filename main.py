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

            date_str_with_year = f"{current_year} {next_football_date}"
            clean_date_str = date_str_with_year.rsplit(" ", 1)[0]
            format_str = "%Y %m/%d - %I:%M %p"
            dt = datetime.strptime(clean_date_str, format_str)
            game_today = dt.date() == datetime.now().date()

            if game_today and dt.year == datetime.now().year and dt.month == datetime.now().month and dt.day == datetime.now().day and dt.hour == datetime.now().hour:
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

            date_str_with_year = f"{current_year} {next_basketball_date}"
            clean_date_str = date_str_with_year.rsplit(" ", 1)[0]
            format_str = "%Y %m/%d - %I:%M %p"
            dt = datetime.strptime(clean_date_str, format_str)
            game_today = dt.date() == datetime.now().date()
            if game_today and dt.year == datetime.now().year and dt.month == datetime.now().month and dt.day == datetime.now().day and dt.hour == datetime.now().hour:
                scheduler.add_job(
                    run_football,
                    'date',
                    run_date=dt,
                    args=[dt, next_football_link, first_team, first_value, second_team, second_value],
                    misfire_grace_time=300
                )
                for job in scheduler.get_jobs():
                    print(job)
            else:
                print("No football game this hour (next game at", dt, ")")
                
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

def zero_pad_month_day(date_str):
    """
    Input: "2025 8/3 - 7:30 PM EDT" or "2025 11/4 - 7:30 PM EDT"
    Output: "2025 08/03 - 7:30 PM"
    """
    # Split year and rest
    year, rest = date_str.split(" ", 1)

    # Split month/day and the time part
    month_day, time_part = rest.split(" - ", 1)
    month, day = month_day.split("/")

    # Zero-pad month if 1-9
    month = month.zfill(2) if int(month) < 10 else month
    # Zero-pad day if 1-9
    day = day.zfill(2) if int(day) < 10 else day

    # Remove timezone (optional)
    time_part = time_part.split(" ")[0] + " " + time_part.split(" ")[1]  # keeps HH:MM AM/PM

    return f"{year} {month}/{day} - {time_part}"
    

def main():
    get_api_data()

if __name__ == "__main__":
    main()
