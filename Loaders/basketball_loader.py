import sqlite3
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

def scrape_historical():
    """ Scrapes all historical basketball data """

    year_data = {}
    event_types = {}
    event_types["REG"] = "Regular Season"
    event_types["CTOURN"] = "Big Ten Tourney"
    event_types["NCAA"] = "NCAA Tourney"
    event_types["NIT"] = "NIT Tourney"
    # scraping basketball data from 1950-2025
    for i in range(1950, 2025):
        url = f'https://www.sports-reference.com/cbb/schools/michigan/men/{i}-schedule.html'
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        games = soup.find_all('tr')
        season_data = {}
        for game in games[1:]:
            game_data = {}
            game_data["date"] = game.find(attrs={"data-stat": "date_game"})
            if not game_data["date"] or game_data["date"].text.strip() == "Date":
                continue
            if game_data["date"]:
                date_str = game.find(attrs={"data-stat": "date_game"}).text.strip()
                date_str = date_str.split(' ', 1)[1]
                date_obj = datetime.strptime(date_str, "%b %d, %Y")
                formatted = date_obj.strftime("%-m/%-d/%Y")
                game_data["date"] = formatted
            

            event = game.find(attrs={"data-stat": "game_type"}).text.strip()
            game_data["event_type"] = event_types.get(event, "Other")
            opponent_name = game.find(attrs={"data-stat": "opp_name"}).text.strip()
            game_data["opponent_name"] = re.sub(r"\s?\(.*\)$", "", opponent_name)
            conf = game.find(attrs={"data-stat": "conf_abbr"}).text.strip()
            game_data["conference"] = False
            if conf == 'Big Ten':
                game_data["conference"] = True
            game_data["michigan_score"] = game.find(attrs={"data-stat": "pts"}).text.strip()
            game_data["opponent_score"] = game.find(attrs={"data-stat": "opp_pts"}).text.strip()

            # if scraping data for an unfinished season
            if not game_data["michigan_score"]:
                continue
            season_data[game_data["date"]] = game_data
        year_data[i] = season_data
    print(year_data)
    return year_data

def load_db(db_file, year_data):
    """Loads the scraped year_data into the football table in the SQLite database."""

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Insert each game's data into the database
    for season, games in year_data.items():
        for date, game_data in games.items():
            game_date = datetime.strptime(game_data['date'], "%m/%d/%Y").date()
            try:
                cursor.execute("""
                INSERT INTO basketball (MichiganScore, OpponentScore, OpponentName, EventType, ConferenceGame, GameDate)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    int(game_data['michigan_score']),
                    int(game_data['opponent_score']),
                    game_data['opponent_name'],
                    game_data['event_type'],
                    "Yes" if game_data.get('conference_game') else "No",
                    game_date
                ))
            except sqlite3.IntegrityError:
                print(f"Duplicate entry skipped: {game_data}")

    connection.commit()
    connection.close()
    print(f"Data successfully loaded.")

def main():
    """ Main Function """

    db_file = "michigami.db"
    print("Scraping Michigan basketball data...")
    year_data = scrape_historical()
    #load_db(db_file, year_data)
    print("All data loaded successfully.")
    
    #print(year_data['2024'])

if __name__ == "__main__":
    main()