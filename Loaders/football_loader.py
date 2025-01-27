import sqlite3
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

def scrape_historical():
    """ Scrapes all historical football data """

    res = requests.get('http://www.jhowell.net/cf/scores/Michigan.htm')
    soup = BeautifulSoup(res.content, 'html.parser') 
    years = soup.find_all('table')
    year_data = {}

    # scraping all historical data from 1892-2013
    for year in years[1:-2]:
        season = year.find('a').text[:4]
        game_data = {}
        games = year.find_all('tr')
        for game in games[1:-1]:
            game_stats = {}
            values = game.find_all('td')
            opponent_name = None
            for value in values:
                if value.find('a') != None:
                    opponent_name = value.find('a').text
                    game_stats['opponent_name'] = opponent_name
                    game_stats['conference_game'] = True
                    if game_stats['opponent_name'].startswith('*'):
                        game_stats['conference_game'] = True
                        game_stats['opponent_name'] = game_stats['opponent_name'][1:]
            if opponent_name == None:
                game_stats['opponent_name'] = values[2].text
                opponent_name = values[2].text
            cleaned_name = re.sub(r'\s?\(.*\)$', '', opponent_name)
            game_stats['opponent_name'] = cleaned_name
            opponent_name = cleaned_name

            game_stats['date'] = values[0].text
            game_stats['date'] = game_stats['date'] + f"/{season}"
            game_stats['michigan_score'] = values[4].text
            game_stats['opponent_score'] = values[5].text
            game_stats['event_type'] = 'Regular Season Game'
            if len(values) > 7:
                game_stats['event_type'] = values[7].text

            game_data[opponent_name] = game_stats

        year_data[season] = game_data
    
    #2024 hard coded data
    games2024 = {}
    game = {}
    game['opponent_name'] = "Fresno State"
    game['conference_game'] = False
    game['date'] = '8/31/2024'
    game['michigan_score'] = '30'
    game['opponent_score'] = '10'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Texas"
    game['conference_game'] = False
    game['date'] = '9/7/2024'
    game['michigan_score'] = '12'
    game['opponent_score'] = '31'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Arkansas State"
    game['conference_game'] = False
    game['date'] = '9/14/2024'
    game['michigan_score'] = '28'
    game['opponent_score'] = '18'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Southern California"
    game['conference_game'] = True
    game['date'] = '9/21/2024'
    game['michigan_score'] = '27'
    game['opponent_score'] = '24'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Minnesota"
    game['conference_game'] = True
    game['date'] = '9/28/2024'
    game['michigan_score'] = '27'
    game['opponent_score'] = '24'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Washington"
    game['conference_game'] = True
    game['date'] = '10/5/2024'
    game['michigan_score'] = '17'
    game['opponent_score'] = '27'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Illinois"
    game['conference_game'] = True
    game['date'] = '10/19/2024'
    game['michigan_score'] = '7'
    game['opponent_score'] = '21'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Michigan State"
    game['conference_game'] = True
    game['date'] = '10/26/2024'
    game['michigan_score'] = '24'
    game['opponent_score'] = '27'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Oregon"
    game['conference_game'] = True
    game['date'] = '11/2/2024'
    game['michigan_score'] = '38'
    game['opponent_score'] = '17'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Indiana"
    game['conference_game'] = True
    game['date'] = '11/9/2024'
    game['michigan_score'] = '15'
    game['opponent_score'] = '20'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Northwestern"
    game['conference_game'] = True
    game['date'] = '11/23/2024'
    game['michigan_score'] = '50'
    game['opponent_score'] = '6'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Ohio State"
    game['conference_game'] = True
    game['date'] = '11/30/2024'
    game['michigan_score'] = '13'
    game['opponent_score'] = '10'
    game['event_type'] = 'Regular Season Game'
    games2024[game['opponent_name']] = game

    game['opponent_name'] = "Alabama"
    game['conference_game'] = False
    game['date'] = '12/31/2024'
    game['michigan_score'] = '19'
    game['opponent_score'] = '13'
    game['event_type'] = 'ReliaQuest Bowl'
    games2024[game['opponent_name']] = game


    year_data['2024'] = games2024
    
    return year_data

def load_db(db_file, year_data):
    """Loads the scraped year_data into the football table in the SQLite database."""

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Insert each game's data into the database
    for season, games in year_data.items():
        for opponent_name, game_stats in games.items():
            game_date = datetime.strptime(game_stats['date'], "%m/%d/%Y")
            try:
                cursor.execute("""
                INSERT INTO football (MichiganScore, OpponentScore, OpponentName, EventType, ConferenceGame, GameDate)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    int(game_stats['michigan_score']),
                    int(game_stats['opponent_score']),
                    game_stats['opponent_name'],
                    game_stats['event_type'],
                    "Yes" if game_stats.get('conference_game') else "No",
                    game_date
                ))
            except sqlite3.IntegrityError:
                print(f"Duplicate entry skipped: {game_stats}")

    connection.commit()
    connection.close()
    print(f"Data successfully loaded.")

def main():
    """ Main Function """

    db_file = "../SQL/michigami.db"
    print("Scraping Michigan football data...")
    year_data = scrape_historical()
    load_db(db_file, year_data)
    print("All data loaded successfully.")
    
    #print(year_data['2024'])

if __name__ == "__main__":
    main()