import sqlite3
import pandas as pd

def play_around():
    
    # Example: Reading from SQLite to Pandas
    connection = sqlite3.connect("michigami.db")
    basketball = pd.read_sql_query("SELECT * FROM basketball", connection)
    unique_ball = basketball.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)
    mich_score = 62
    opp_score = 79
    michigami =  not ((unique_ball["MichiganScore"] == mich_score) & (unique_ball["OpponentScore"] == opp_score)).any()
    print(mich_score, opp_score, michigami)
    print(((basketball["MichiganScore"] == mich_score) & (basketball["OpponentScore"] == opp_score)).sum())

    filtered_df = basketball[(basketball["MichiganScore"] == mich_score) & 
                         (basketball["OpponentScore"] == opp_score)]

    most_recent_date = filtered_df["GameDate"].max()
    first_date = filtered_df["GameDate"].min()

    print(unique_ball.shape[0])
    #print(unique_ball.tail(20))
    #print(basketball.tail(20))
    print(basketball.shape[0])
    print(most_recent_date, first_date)

    connection.close()

def main():
    play_around()

if __name__ == "__main__":
    main()
