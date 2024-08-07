import tweepy
import json
import os
import time

class OAuth2Handler:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.load_oauth2_token()
        self.setup_oauth2_handler()

    def load_oauth2_token(self):
        if os.path.exists('oauth2_token.json'):
            with open('oauth2_token.json', 'r') as f:
                self.oauth2_token = json.load(f)
        else:
            raise FileNotFoundError("oauth2_token.json not found. Please run the initial OAuth2 setup.")

    def save_oauth2_token(self):
        with open('oauth2_token.json', 'w') as f:
            json.dump(self.oauth2_token, f)

    def setup_oauth2_handler(self):
        self.oauth2_user_handler = tweepy.OAuth2UserHandler(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=[
                "tweet.read", "tweet.write", "tweet.moderate.write",
                "users.read", "follows.read", "follows.write",
                "offline.access", "space.read", "mute.read",
                "mute.write", "like.read", "like.write",
                "list.read", "list.write", "block.read",
                "block.write", "bookmark.read", "bookmark.write"
            ],
            client_secret=self.client_secret
        )

    def ensure_oauth2_token(self):
        if self.oauth2_token.get('expires_at', 0) < time.time():
            try:
                new_token = self.oauth2_user_handler.refresh_token(self.oauth2_token['refresh_token'])
                self.oauth2_token.update(new_token)
                self.oauth2_token['expires_at'] = time.time() + new_token['expires_in'] - 300  # 5 minutes buffer
                self.save_oauth2_token()
                print("OAuth 2.0 token has been refreshed and updated.")
            except Exception as e:
                print(f"Error refreshing token: {e}")
                raise

    def get_client(self):
        self.ensure_oauth2_token()
        return tweepy.Client(self.oauth2_token['access_token'])

def get_oauth1_api():
    auth = tweepy.OAuthHandler(
        os.environ['consumer_key'],
        os.environ['consumer_secret']
    )
    auth.set_access_token(
        os.environ['access_token'],
        os.environ['access_token_secret']
    )
    return tweepy.API(auth)