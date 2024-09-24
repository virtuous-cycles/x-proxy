import os
from config import Config
from .process_x_response import process_x_response

class TweetService:
    # Common tweet fields to request
    TWEET_FIELDS = [
        'author_id', 'public_metrics', 'referenced_tweets',
        'conversation_id', 'created_at', 'attachments'
    ]

    # Common expansions to request
    EXPANSIONS = [
        'author_id', 'referenced_tweets.id', 'referenced_tweets.id.author_id',
        'edit_history_tweet_ids', 'in_reply_to_user_id', 'attachments.media_keys',
        'attachments.poll_ids', 'geo.place_id', 'entities.mentions.username'
    ]

    # Common user fields to request
    USER_FIELDS = [
        'created_at', 'description', 'entities', 'id', 'location',
        'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_image_url',
        'protected', 'public_metrics', 'url', 'username', 'verified',
        'verified_type', 'withheld'
    ]

    def __init__(self, oauth2_handler, media_service):
        self.oauth2_handler = oauth2_handler
        self.media_service = media_service

    def post_reply(self, tweet_id, text):
        client = self.oauth2_handler.get_client()
        response = client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
        return response.data['id']

    def pull_mentions(self):
        client = self.oauth2_handler.get_client()
        response = client.get_users_mentions(
            id=Config.TRUTH_TERMINAL_TWITTER_ID,
            max_results=10, # default is 10
            # since_id (int | str | None) – Returns results with a Tweet ID greater than (that is, more recent than) the specified ‘since’ Tweet ID. There are limits to the number of Tweets that can be accessed through the API. If the limit of Tweets has occurred since the since_id, the since_id will be forced to the oldest ID available.
            # start_time (datetime.datetime | str | None) – YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339). The oldest UTC timestamp from which the Tweets will be provided. Timestamp is in second granularity and is inclusive (for example, 12:00:01 includes the first second of the minute).
            expansions=self.EXPANSIONS,
            tweet_fields=self.TWEET_FIELDS,
            user_fields=self.USER_FIELDS
        )
        return process_x_response(response)

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
        response = client.get_tweet(
            id=tweet_id,
            expansions=self.EXPANSIONS,
            tweet_fields=self.TWEET_FIELDS,
            user_fields=self.USER_FIELDS
        )
        return process_x_response(response)

    def search_recent_tweets(self, query):
        client = self.oauth2_handler.get_client()
        response = client.search_recent_tweets(
            query,
            expansions=self.EXPANSIONS,
            tweet_fields=self.TWEET_FIELDS,
            user_fields=self.USER_FIELDS
        )
        return process_x_response(response)

    def get_conversation_thread(self, tweet_id):
        client = self.oauth2_handler.get_client()

        # Get the requested tweet
        requested_tweet = self.get_tweet(tweet_id)
        if not requested_tweet:
            return None

        conversation_id = requested_tweet.get('conversation_id')
        if not conversation_id:
            return [requested_tweet]  # If there's no conversation_id, return just the requested tweet

        # Get the root tweet of the conversation
        root_tweet = self.get_tweet(conversation_id)
        if not root_tweet:
            return [requested_tweet]  # If we can't get the root tweet, return just the requested tweet

        # Search for all tweets in the conversation
        query = f"conversation_id:{conversation_id}"
        response = client.search_recent_tweets(
            query,
            max_results=25,  # Adjust as needed
            expansions=self.EXPANSIONS,
            tweet_fields=self.TWEET_FIELDS,
            user_fields=self.USER_FIELDS
        )
        thread = process_x_response(response)

        # If no tweets were found in the conversation, return just the requested tweet
        if not thread:
            return [requested_tweet]

        # Ensure both the requested tweet and root tweet are in the thread
        thread = self.add_tweet_if_missing(thread, requested_tweet)
        thread = self.add_tweet_if_missing(thread, root_tweet)

        # Sort the thread by created_at timestamp
        thread.sort(key=lambda x: x['created_at'])

        return thread

    def add_tweet_if_missing(self, thread, tweet):
        if not any(t['id'] == tweet['id'] for t in thread):
            thread.append(tweet)
        return thread