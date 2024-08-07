from .tweet_service import TweetService
from .media_service import MediaService
from config import Config

class XService:
    def __init__(self, oauth2_handler, oauth1_api):
        self.media_service = MediaService(oauth1_api)
        self.tweet_service = TweetService(oauth2_handler, self.media_service)

    def post_reply(self, tweet_id, text):
        return self.tweet_service.post_reply(tweet_id, text)

    def pull_mentions(self):
        return self.tweet_service.pull_mentions(Config.TRUTH_TERMINAL_TWITTER_ID)

    def post_tweet(self, text, in_reply_to_tweet_id=None, media_url=None):
        return self.tweet_service.post_tweet(text, in_reply_to_tweet_id, media_url)

    def get_tweet(self, tweet_id):
        return self.tweet_service.get_tweet(tweet_id)

    def search_recent_tweets(self, query):
        return self.tweet_service.search_recent_tweets(query)