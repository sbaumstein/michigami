import sqlite3
import pandas as pd

def play_around():
    
    # Example: Reading from SQLite to Pandas
    connection = sqlite3.connect("michigami.db")
    football = pd.read_sql_query("SELECT * FROM football", connection)
    unique_foot = football.drop_duplicates(subset=["MichiganScore", "OpponentScore"]).reset_index(drop=True)

    print(football.head(20))
    print(unique_foot.shape[0])
    #print(unique_ball.tail(20))
    #print(basketball.tail(20))

    connection.close()

def main():
    play_around()

if __name__ == "__main__":
    main()
