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


def scrape_scores(date, link, first_team, first_value, second_team, second_value):
    
    # Example: Reading from SQLite to Pandas
    connection = sqlite3.connect("michigami.db")
    football = pd.read_sql_query("SELECT * FROM football", connection)
    reverse_foot = football.iloc[::-1].reset_index(drop=True)
    unique_foot = reverse_foot.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)
   
   # need this so that ESPN doesn't block the scraping
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.espn.com/",
    }

    date = date
    url = link
    michigan_home = True
    opp_name = " "
    if first_team == "Michigan":
        opp_name = second_team
        if first_value == "away":
            michigan_home = False
    elif second_team == "Michigan":
        opp_name = first_team
        if second_value == "away":
            michigan_home = False
    
    with open("output.txt", "a") as file:
        file.write(f"{michigan_home}\n {opp_name} \n")
    
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
                michigami =  not ((unique_foot["MichiganScore"] == mich_score) & (unique_foot["OpponentScore"] == opp_score)).any()
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
        num_michigami = unique_foot.shape[0]
        michigami_tweet(mich_score, opp_score, opp_name, num_michigami, "football")
    

    else:
        num_times = ((football["MichiganScore"] == mich_score) & (football["OpponentScore"] == opp_score)).sum()
        filtered_df = football[(football["MichiganScore"] == mich_score) & (football["OpponentScore"] == opp_score)]
        most_recent = filtered_df["GameDate"].max()
        earliest = filtered_df["GameDate"].min()
        not_michigami_tweet(mich_score, opp_score, opp_name, num_times, most_recent, earliest, "football")
    
    #adds to SQL
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO football (MichiganScore, OpponentScore, OpponentName, EventType, ConferenceGame, GameDate)
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


    connection.close()

def main():
    scrape_scores()

if __name__ == "__main__":
    main()
