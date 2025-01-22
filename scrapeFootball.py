import sqlite3
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

db_file = "michigami.db"
connection = sqlite3.connect(db_file)
cursor = connection.cursor()
res = requests.get('http://www.jhowell.net/cf/scores/Michigan.htm')
soup = BeautifulSoup(res.content, 'html.parser') 
years = soup.find_all('table')
year_data = {}

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

print(year_data['1904']['Physicians & Surgeons'])

    # Scraping logic goes here
    #pass



    #cursor.execute("""
    #INSERT INTO football (MichiganScore, OpponentScore, OpponentName, EventType)
    #VALUES (?, ?, ?, ?)
    #""", (35, 28, "Ohio State", "Regular Season"))

#connection.commit()
#connection.close()