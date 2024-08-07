from .oauth_handler import OAuth2Handler
from .tweet_service import TweetService
from .media_service import MediaService
from config import Config

class XService:
    def __init__(self):
        self.oauth_handler = OAuth2Handler(
            client_id=Config.CLIENT_ID,
            client_secret=Config.CLIENT_SECRET,
            redirect_uri=Config.REDIRECT_URI
        )
        self.tweet_service = TweetService(self.oauth_handler)
        self.media_service = MediaService()

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