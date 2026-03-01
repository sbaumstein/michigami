import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from dateutil import parser
from zoneinfo import ZoneInfo


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
            first_team = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][0]["team"]["shortDisplayName"])
            first_value = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][0]["homeAway"])
            second_team = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][1]["team"]["shortDisplayName"])
            second_value = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][1]["homeAway"])

            dt = parse_espn_shortdetail(next_football_date, current_year)
            dt = dt.replace(tzinfo=ZoneInfo("America/New_York"))
            now = datetime.now(ZoneInfo("America/New_York"))
            game_today = dt.date() == now.date()
            sec_difference = int((dt - now).total_seconds())

            if game_today and sec_difference < 3600:
                scheduler.add_job(run_football, 'date', run_date=dt, args=[dt, next_football_link, first_team, first_value, second_team, second_value], misfire_grace_time=300)
                for job in scheduler.get_jobs():
                    print(job)
            else:
                print(f"No football game this hour (), next game at: ", dt)
        except Exception as e:
            print("Error: No football Game Coming Up", e)
    else:
        print("Error:", football_response.status_code)

    michigan_basketball_api = "https://site.web.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/130"
    basketball_response = requests.get(michigan_basketball_api)
    next_basketball_date = ""
    next_basketball_link = ""
    if basketball_response.status_code == 200:
        try:
            data = basketball_response.json()
            next_basketball_date = (data['team']['nextEvent'][0]['competitions'][0]['status']['type']['shortDetail'])
            next_basketball_link = (data["team"]["nextEvent"][0]["links"][0]["href"])
            first_team = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][0]["team"]["shortDisplayName"])
            first_value = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][0]["homeAway"])
            second_team = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][1]["team"]["shortDisplayName"])
            second_value = (data["team"]["nextEvent"][0]["competitions"][0]["competitors"][1]["homeAway"])                

            dt = parse_espn_shortdetail(next_basketball_date, current_year)
            dt = dt.replace(tzinfo=ZoneInfo("America/New_York"))
            now = datetime.now(ZoneInfo("America/New_York"))
            game_today = dt.date() == now.date()
            sec_difference = int((dt - now).total_seconds())
            if game_today and sec_difference < 3600:
                scheduler.add_job(
                    run_basketball,
                    'date',
                    run_date=dt,
                    args=[dt, next_basketball_link, first_team, first_value, second_team, second_value],
                    misfire_grace_time=300
                )
                for job in scheduler.get_jobs():
                    print(job)
            else:
                print("No basketball game this hour (next game at", dt, ")")
                
        except Exception as e:
            print("Error: No basketball Game Coming Up", e)
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

def parse_espn_shortdetail(date_str, current_year):
    """
    Parse ESPN shortDetail strings into a datetime, handling many formats:
      - "3/1 - 7:30 PM EST"          (basketball M/D style)
      - "11/04 - 7:30 PM EDT"        (zero-padded)
      - "Sat, March 1 at 7:30 PM"    (football verbose)
      - "2026-03-01T23:30Z"          (ISO)
    Raises ValueError for non-schedulable statuses like "In Progress", "Final", "TBD".
    """
    NON_DATE_STATUSES = {
        "in progress", "final", "tbd", "postponed",
        "cancelled", "canceled", "halftime", "end of period",
    }
    clean = date_str.strip()
    if clean.lower() in NON_DATE_STATUSES:
        raise ValueError(f"Game status, not a schedulable time: {clean!r}")

    # Strategy 1: "M/D - H:MM AM/PM [TZ]" — replace " - " with space, prepend year
    if " - " in clean:
        date_part, time_part = clean.split(" - ", 1)
        time_tokens = time_part.strip().split()
        clean_time = " ".join(time_tokens[:2])  # keep "H:MM AM/PM", drop TZ abbreviation
        try:
            return parser.parse(f"{current_year}/{date_part} {clean_time}")
        except Exception:
            pass

    # Strategy 2: direct parse (ISO strings, verbose football formats)
    try:
        return parser.parse(clean)
    except Exception:
        pass

    # Strategy 3: fuzzy parse with year prepended (catches remaining edge cases)
    return parser.parse(f"{current_year} {clean}", fuzzy=True)
    

def main():
    get_api_data()

if __name__ == "__main__":
    main()
