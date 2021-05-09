from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    #class for streaming an processing live tweets

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweet(self, fetched_tweets_file, hash_tags_list ):
        #this handle Twitter authentication and streaming API
        listener = TwitterListener(fetched_tweets_file)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tags_list)

class TwitterListener(StreamListener):
    #prints recieved tweets 

    def __init__(self,fetched_tweets_file):
        self.fetched_tweets_file =  fetched_tweets_file

    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_file,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s", str(e))
        return True

    def on_error(self, status):
        if status == 420:
            #Break connection if rate limit is reached
            return False
        print(status)
        

if __name__ == "__main__":
    hash_tags_list = ['covid-19','work from home stress','online therapy','sucide']
    fetched_tweets_file = "tweets.json"
    twitterStreamer = TwitterStreamer()
    twitterStreamer.stream_tweet(fetched_tweets_file,hash_tags_list)
    