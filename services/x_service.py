from .tweet_service import TweetService
from .media_service import MediaService
from config import Config

class XService:
    def __init__(self, oauth2_handler, oauth1_api):
        self.oauth2_handler = oauth2_handler
        self.oauth1_api = oauth1_api
        self.tweet_service = TweetService(self.oauth2_handler)
        self.media_service = MediaService(self.oauth1_api)

    def post_reply(self, tweet_id, text):
        return self.tweet_service.post_reply(tweet_id, text)

    def pull_mentions(self):
        return self.tweet_service.pull_mentions(Config.TRUTH_TERMINAL_TWITTER_ID)

    def post_tweet(self, text, in_reply_to_tweet_id=None, media_ids=None):
        return self.tweet_service.post_tweet(text, in_reply_to_tweet_id, media_ids)

    def upload_media(self, media_file):
        return self.media_service.upload_media(media_file)

    def get_tweet(self, tweet_id):
        return self.tweet_service.get_tweet(tweet_id)

    def search_recent_tweets(self, query):
        return self.tweet_service.search_recent_tweets(query)