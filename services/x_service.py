from .tweet_service import TweetService
from .media_service import MediaService

class XService:
    def __init__(self, oauth2_handler, oauth1_api):
        self.media_service = MediaService(oauth1_api)
        self.tweet_service = TweetService(oauth2_handler, self.media_service)

    def __getattr__(self, name):
        return getattr(self.tweet_service, name)