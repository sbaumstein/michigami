import time
import requests
import sqlite3
import pandas as pd

def scrape_scores():
    # Example: Reading from SQLite to Pandas
    connection = sqlite3.connect("michigami.db")
    df = pd.read_sql_query("SELECT * FROM football", connection)
    reverse = df.iloc[::-1].reset_index(drop=True)
    unique_scores = reverse.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)
    print(unique_scores.tail(18))

    connection.close()

def main():
    scrape_scores()

if __name__ == "__main__":
    main()
