import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener #class
from tweepy import OAuthHandler   #class from tweepy. use credential to handle user authentication
from tweepy import Stream   #class

import twitter_credentials

class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth=TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client=API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth=OAuthHandler(twitter_credentials.consumer_key,twitter_credentials.consumer_secret)
        auth.set_access_token(twitter_credentials.access_token,twitter_credentials.access_token_secret)
        return auth

class TwitterStreamer():
    """
    class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator=TwitterAuthenticator()

    def stream_tweets(self,fetched_tweets_filename,hash_tag_list):
        #This handles Twitter authentication and the connection to the Twitter Streaming API.
        listener=TwitterListener(fetched_tweets_filename)
        auth=self.twitter_authenticator.authenticate_twitter_app()
        stream=Stream(auth,listener)
        stream.filter(track=hash_tag_list)
        #filters twitter streams to capture data by the keywords

class TwitterListener(StreamListener):
    #A basic listener that just prints received tweets to stdout
    def __init__(self,fetched_tweets_filename):
        self.fetched_tweets_filename=fetched_tweets_filename

    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s",str(e))
        return True

    def on_error(self,status):
        if status == 420:
            return False
            """
            Returning False on data method in case rate limit occurs. 
            This happens when your API is trying to get info from Twitter 
            and it doesn't like that/think you are abusing the system. Rturns 420
            If I keep accessing tweets despite getting these errors, the delay time 
            increases exponentially and cause you to get locked out
            """
        print(status)
if __name__=="__main__":
    hash_tag_list=['donald trump','hillary clinton','barack obama','bernie sanders']
    fetched_tweets_filename="tweets.txt"

    twitter_client = TwitterClient('pycon')
    print(twitter_client.get_user_timeline_tweets(1))

    #twitter_streamer=TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename,hash_tag_list)

#^creates a dictionary that has information regarding each tweet. 
#who retweeted, how many retweet, etc.
