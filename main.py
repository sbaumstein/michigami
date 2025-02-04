import time
import requests
import sqlite3
import pandas as pd

def scrape_scores():
    # Example: Reading from SQLite to Pandas
    connection = sqlite3.connect("michigami.db")
    football = pd.read_sql_query("SELECT * FROM football", connection)
    reverse_foot = football.iloc[::-1].reset_index(drop=True)
    unique_foot = reverse_foot.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)
    basketball = pd.read_sql_query("SELECT * FROM basketball", connection)
    reverse_ball = basketball.iloc[::-1].reset_index(drop=True)
    unique_ball = reverse_ball.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)
    print(unique_ball.size)
    print(unique_ball.head(20))

    connection.close()

def main():
    scrape_scores()

if __name__ == "__main__":
    main()
