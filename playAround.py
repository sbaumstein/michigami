import sqlite3
import pandas as pd

def scrape_scores():
    
    # Example: Reading from SQLite to Pandas
    connection = sqlite3.connect("michigami.db")
    basketball = pd.read_sql_query("SELECT * FROM basketball", connection)
    reverse_ball = basketball.iloc[::-1].reset_index(drop=True)
    unique_ball = reverse_ball.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)
    mich_score = 65
    opp_score = 71
    michigami =  not ((unique_ball["MichiganScore"] == mich_score) & (unique_ball["OpponentScore"] == opp_score)).any()
    print(mich_score, opp_score, michigami)
    #print(unique_foot.size)
    #print(unique_foot.head(20))

    connection.close()

def main():
    scrape_scores()

if __name__ == "__main__":
    main()
