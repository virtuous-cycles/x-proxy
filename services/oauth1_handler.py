import tweepy

class OAuth1Handler:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.api = None

    def initialize(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

    def validate_credentials(self):
        try:
            self.api.verify_credentials()
            print("OAuth 1.0a credentials are valid.")
            return True
        except tweepy.TweepError as e:
            print(f"Error validating OAuth 1.0a credentials: {e}")
            return False