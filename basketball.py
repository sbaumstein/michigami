import time
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
import sys
from urllib.parse import urlparse
from twitter import michigami_tweet, not_michigami_tweet


def scrape_scores(date, link):

    with open("output.txt", "a") as file:
        file.write("Working\n")

    # Example: Reading from SQLite to Pandas
    connection = sqlite3.connect("michigami.db")
    basketball = pd.read_sql_query("SELECT * FROM basketball", connection)
    unique_ball = basketball.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)

    # need this so that ESPN doesn't block the scraping
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.espn.com/",
    }

    date = date
    url = link
    michigan_home = True
    path_segments = urlparse(url).path.strip("/").split("/")[-1].split("-")
    opp_name = ""
    if "michigan" in path_segments[0]:
        michigan_home = False
        opp_name = path_segments[1]
        with open("output.txt", "a") as file:
            file.write(f"Michigan Away")
            file.write("\n")
    elif "michigan" in path_segments[1]:
        michigan_home = True
        opp_name = path_segments[0]
        with open("output.txt", "a") as file:
            file.write(f"Michigan Home")
            file.write("\n")
    
    final = False
    michigami = False
    while not final:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"Request failed with status code: {res.status_code}")
            final = True
        else:
            try:
                soup = BeautifulSoup(res.content, "html.parser")
                scores = soup.find_all("div", class_=lambda x: x and "Gamestrip__Score" in x)
                score_values = [re.search(r'\d+', score.get_text(strip=True)).group() for score in scores]
                gamestrip = soup.find("svg", class_=lambda x: x and "Gamestrip__WinnerIcon" in x)
                if gamestrip:
                    final = True
                away_score = int(score_values[0])
                home_score = int(score_values[-1])
                if michigan_home:
                    mich_score = home_score
                    opp_score = away_score
                else:
                    mich_score = away_score
                    opp_score = home_score
                michigami =  not ((unique_ball["MichiganScore"] == mich_score) & (unique_ball["OpponentScore"] == opp_score)).any()
                with open("output.txt", "a") as file:
                    file.write(f"Michigan: {mich_score}, Opponent: {opp_score}, Michigami = {michigami}, Final = {final}")
                    file.write("\n")
            except Exception as e:
                with open("output.txt", "a") as file:
                    file.write(f"No Score yet!")
        
        if final:
            break
        time.sleep(300)

    #twweeting logic
    if michigami:
        num_michigami = unique_ball.shape[0]
        michigami_tweet(mich_score, opp_score, opp_name, num_michigami, "basketball")
    

    else:
        num_times = ((basketball["MichiganScore"] == mich_score) & (basketball["OpponentScore"] == opp_score)).sum()
        filtered_df = basketball[(basketball["MichiganScore"] == mich_score) & (basketball["OpponentScore"] == opp_score)]
        most_recent = filtered_df["GameDate"].max()
        earliest = filtered_df["GameDate"].min()
        not_michigami_tweet(mich_score, opp_score, opp_name, num_times, most_recent, earliest, "basketball")
    
    #adds to SQL
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO basketball (MichiganScore, OpponentScore, OpponentName, EventType, ConferenceGame, GameDate)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                int(mich_score),
                int(opp_score),
                opp_name,
                "Fade",
                "No",
                date
            ))
    except sqlite3.IntegrityError as e:
        print(f"{e}")
    connection.commit()
    connection.close()
    return

def main(date, link):
    scrape_scores(date, link)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <date> <link>")
        sys.exit(1)

    date_arg = sys.argv[1]
    link_arg = sys.argv[2]
    main(date_arg, link_arg)
    