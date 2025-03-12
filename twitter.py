import tweepy
import sys

API_KEY = "FErbNZOD6azW53f3RxVkaj9cD"
API_SECRET = "2Tz3ArjIcQ9ZAQKje5KM72eXqd02RN0l1qgJkxlAVrIQKvqbXN"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIuWzwEAAAAA8HtCkLOUTqDb0bnfsKS5QSh3XsE%3D4aqak399g1Mv7MCIDJJbQcNSRJWH6XKRytSRbHPXzNLHgpPpEW"
ACCESS_TOKEN = "1899914528755773440-hZ4eJlVs0ZTA77YKvIaYbWeyJPmniC"
ACCESS_TOKEN_SECRET = "TqykG6s5xNQW1qINVy80nULG1Ej4EmDPEZ1ZepU52VJrm"
CLIENT_ID = "MlJtR2tnTDI1OHZEeVktX2dlSmE6MTpjaQ"
CLIENT_SECRET = "_-Fv8BSe-7n7kmkX6XKDvs5LgWhEoY_Y4Gq6qzN_01xbInX9rI"

def michigami_tweet(mich_score, opp_score, opp_name, num_michigami, sport):
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    if mich_score > opp_score:
        tweet_text = f"UMICH {mich_score} - {opp_score} {opp_name} \nFinal! Michigan gets the win! \n \nThat's Michigami! There have been {num_michigami} unique scores in Michigan {sport} history! \nGO BLUE!"
    
    else:
        tweet_text = f"UMICH {mich_score} - {opp_score} {opp_name} \nFinal. \n \nDespite the loss, this game is a Michigami! There have been {num_michigami} unique scores in Michigan {sport} history! \ngo blue."

    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully:", response)
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

def not_michigami_tweet(mich_score, opp_score, opp_name, num_times, most_recent, earliest, sport):
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    if mich_score > opp_score:
        if num_times == 1:
            tweet_text = f"UMICH {mich_score} - {opp_score} {opp_name} \nFinal! Michigan gets the win! \n \nNo Michigami. That {sport} score has happened {num_times} time before, most recently on {most_recent}. GO BLUE!"
        else:
            tweet_text = f"UMICH {mich_score} - {opp_score} {opp_name} \nFinal! Michigan gets the win! \n \nNo Michigami. That {sport} score has happened {num_times} times before, most recently on {most_recent}, and for the first time ever on {earliest}. GO BLUE!"
    
    else:
        if num_times == 1:
            tweet_text = f"UMICH {mich_score} - {opp_score} {opp_name} \nFinal. \n \nNo Michigami. That {sport} score has happened {num_times} time before, most recently on {most_recent}. go blue."
        else:
            tweet_text = f"UMICH {mich_score} - {opp_score} {opp_name} \nFinal. \n \nNo Michigami. That {sport} score has happened {num_times} times before, most recently on {most_recent}, and for the first time ever on {earliest}. go blue."

    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully:", response)
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

if __name__ == "__main__":
    mich_score = int(sys.argv[1])
    opp_score = int(sys.argv[2])
    opp_name = sys.argv[3]
    num_times = sys.argv[4]
    last_date = sys.argv[5]
    sport = sys.argv[6]

    not_michigami_tweet(mich_score, opp_score, opp_name, num_times, last_date, sport)