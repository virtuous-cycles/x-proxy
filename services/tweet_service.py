import os

class TweetService:
    def __init__(self, oauth2_handler, media_service):
        self.oauth2_handler = oauth2_handler
        self.media_service = media_service

    def post_reply(self, tweet_id, text):
        client = self.oauth2_handler.get_client()
        response = client.create_tweet(
            text=text,
            in_reply_to_tweet_id=tweet_id
        )
        return response.data['id']

    def pull_mentions(self, user_id):
        client = self.oauth2_handler.get_client()
        response = client.get_users_mentions(id=user_id, max_results=15)
        return response.data

    def post_tweet(self, text, in_reply_to_tweet_id=None, media_url=None):
        client = self.oauth2_handler.get_client()
        media_ids = None
        
        if media_url:
            temp_file_path = self.media_service.download_media(media_url)
            if temp_file_path:
                try:
                    media_id = self.media_service.upload_media(temp_file_path)
                    if media_id:
                        media_ids = [media_id]
                finally:
                    os.unlink(temp_file_path)

        response = client.create_tweet(
            text=text,
            in_reply_to_tweet_id=in_reply_to_tweet_id,
            media_ids=media_ids,
            user_auth=False
        )
        return response.data['id']

    def get_tweet(self, tweet_id):
        client = self.oauth2_handler.get_client()
        response = client.get_tweet(tweet_id)
        return response.data

    def search_recent_tweets(self, query):
        client = self.oauth2_handler.get_client()
        response = client.search_recent_tweets(query)
        return response.data