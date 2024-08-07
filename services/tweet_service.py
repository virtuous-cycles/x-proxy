class TweetService:
    def __init__(self, oauth_handler):
        self.oauth_handler = oauth_handler

    def post_reply(self, tweet_id, text):
        client = self.oauth_handler.get_client()
        response = client.create_tweet(
            text=text,
            in_reply_to_tweet_id=tweet_id,
            user_auth=False
        )
        return response.data['id']

    def pull_mentions(self, user_id):
        client = self.oauth_handler.get_client()
        response = client.get_users_mentions(
            id=user_id,
            max_results=15,
            expansions=[
                'author_id', 'referenced_tweets.id',
                'referenced_tweets.id.author_id',
                'edit_history_tweet_ids',
                'in_reply_to_user_id',
                'attachments.media_keys',
                'attachments.poll_ids',
                'geo.place_id',
                'entities.mentions.username',
            ],
            tweet_fields=[
                'username', 'public_metrics', 'referenced_tweets',
                'conversation_id', 'created_at', 'attachments'
            ]
        )
        return response.data

    def post_tweet(self, text, in_reply_to_tweet_id=None, media_ids=None):
        client = self.oauth_handler.get_client()
        response = client.create_tweet(
            text=text,
            in_reply_to_tweet_id=in_reply_to_tweet_id,
            media_ids=media_ids,
            user_auth=False
        )
        return response.data['id']

    def get_tweet(self, tweet_id):
        client = self.oauth_handler.get_client()
        response = client.get_tweet(tweet_id)
        return response.data

    def search_recent_tweets(self, query):
        client = self.oauth_handler.get_client()
        response = client.search_recent_tweets(query)
        return response.data