import time
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json


def scrape_scores(date, link):
    
    # Example: Reading from SQLite to Pandas
    connection = sqlite3.connect("michigami.db")
    football = pd.read_sql_query("SELECT * FROM football", connection)
    reverse_foot = football.iloc[::-1].reset_index(drop=True)
    unique_foot = reverse_foot.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)
    #print(unique_foot.size)
    #print(unique_foot.head(20))


    # need this so that ESPN doesn't block the scraping
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.espn.com/",
    }

    date = date
    url = link
    # figure out to scrape football scores

    connection.close()

def main():
    scrape_scores()

if __name__ == "__main__":
    main()
