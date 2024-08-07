import tweepy
import json
import os
import time
import webbrowser
import threading

class OAuth2Handler:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.oauth2_token = None
        self.setup_oauth2_handler()
        self.refresh_lock = threading.Lock()
        self.refresh_thread = None

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

    def load_oauth2_token(self):
        if os.path.exists('oauth2_token.json'):
            with open('oauth2_token.json', 'r') as f:
                self.oauth2_token = json.load(f)
        else:
            print("oauth2_token.json not found. Running initial OAuth2 setup.")
            self.initial_oauth2_setup()

    def save_oauth2_token(self):
        with open('oauth2_token.json', 'w') as f:
            json.dump(self.oauth2_token, f)

    def initial_oauth2_setup(self):
        auth_url = self.oauth2_user_handler.get_authorization_url()
        print(f"Please open this URL to authorize the application: {auth_url}")
        webbrowser.open(auth_url)

        oauth2_authorization_url = input("Please paste the authorization response URL here: ")

        token = self.oauth2_user_handler.fetch_token(oauth2_authorization_url)

        self.oauth2_token = token
        self.oauth2_token['expires_at'] = time.time() + token['expires_in'] - 300
        self.save_oauth2_token()

        print("OAuth2 token has been generated and saved.")

    def refresh_token(self):
        with self.refresh_lock:
            try:
                new_token = self.oauth2_user_handler.refresh_token(self.oauth2_token['refresh_token'])
                self.oauth2_token.update(new_token)
                self.oauth2_token['expires_at'] = time.time() + new_token['expires_in'] - 300
                self.save_oauth2_token()
                print("OAuth 2.0 token has been refreshed and updated.")
            except Exception as e:
                print(f"Error refreshing token: {e}")
                print("Running initial OAuth2 setup again.")
                self.initial_oauth2_setup()

    def ensure_oauth2_token(self):
        if not self.oauth2_token:
            self.load_oauth2_token()

        if self.oauth2_token.get('expires_at', 0) < time.time():
            self.refresh_token()

    def start_refresh_thread(self):
        def refresh_loop():
            while True:
                time_to_expiry = self.oauth2_token.get('expires_at', 0) - time.time()
                if time_to_expiry < 1800:  # Refresh if less than 30 minutes to expiry
                    self.refresh_token()
                    sleep_time = 3600  # Sleep for 1 hour after a refresh
                else:
                    sleep_time = min(time_to_expiry - 1800, 3600)  # Sleep until 30 mins before expiry or for 1 hour, whichever is shorter
                time.sleep(sleep_time)

        self.refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        self.refresh_thread.start()

    def get_client(self):
        self.ensure_oauth2_token()
        return tweepy.Client(self.oauth2_token['access_token'])

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