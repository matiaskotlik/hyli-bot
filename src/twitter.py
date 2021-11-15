import config
import tweepy

def get_twitter_connection():
    auth = tweepy.AppAuthHandler(config.TWITTER_API_KEY, config.TWITTER_API_KEY_SECRET)
    api = tweepy.API(auth)
    print('Connected to Twitter API')
    return api