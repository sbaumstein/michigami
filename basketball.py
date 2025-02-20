import time
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
import sys


def scrape_scores(date, link):

    with open("output.txt", "a") as file:
        file.write("Working\n")

    # Example: Reading from SQLite to Pandas
    connection = sqlite3.connect("michigami.db")
    basketball = pd.read_sql_query("SELECT * FROM basketball", connection)
    reverse_ball = basketball.iloc[::-1].reset_index(drop=True)
    unique_ball = reverse_ball.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)
    #print(unique_ball.size)
    #print(unique_ball.head(20))


    # need this so that ESPN doesn't block the scraping
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.espn.com/",
    }

    date = date
    url = link
    url = "https://www.espn.com/mens-college-basketball/game/_/gameId/401708403"


    final = False
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
                away_score = score_values[0]
                home_score = score_values[-1]
                # TODO: add logic for figuring out if Michigan is home or away
                mich_score = home_score
                opp_score = away_score
                michigami = unique_ball[(unique_ball['MichiganScore'] == mich_score) & (unique_ball['OpponentScore'] == opp_score)]
                with open("output.txt", "a") as file:
                    file.write(f"{away_score}, {home_score}")
                    if not michigami.empty:
                        file.write(" Currently Michigami")
                    else:
                        file.write(" Not Michigami")
                    file.write("\n")
            except Exception as e:
                print("No Score Yet! ", e)
        
        time.sleep(300)

    connection.close()

def main(date, link):
    scrape_scores(date, link)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <date> <link>")
        sys.exit(1)

    date_arg = sys.argv[1]
    link_arg = sys.argv[2]
    main(date_arg, link_arg)
    