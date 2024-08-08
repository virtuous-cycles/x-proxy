import tweepy
import json
import os
import time
import webbrowser
import threading

class MyOAuth2UserHandler(tweepy.OAuth2UserHandler):
    def refresh_token(self, refresh_token):
        new_token = super().refresh_token(
            "https://api.twitter.com/2/oauth2/token",
            refresh_token=refresh_token,
            body=f"grant_type=refresh_token&client_id={self.client_id}",
        )
        return new_token

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
        # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Allow OAuth2 over HTTP for development
        self.oauth2_user_handler = MyOAuth2UserHandler(
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
            print("Loaded existing OAuth2 token from file.")
            return True
        else:
            print("oauth2_token.json not found.")
            return False

    def save_oauth2_token(self):
        with open('oauth2_token.json', 'w') as f:
            json.dump(self.oauth2_token, f)
        print("OAuth2 token saved to file.")

    def initial_oauth2_setup(self):
        auth_url = self.oauth2_user_handler.get_authorization_url()
        print(f"Please open this URL to authorize the application: {auth_url}")
        webbrowser.open(auth_url)

        oauth2_authorization_url = input("Please paste the authorization response URL here: ")

        self.oauth2_token = self.oauth2_user_handler.fetch_token(oauth2_authorization_url)
        self.oauth2_token['expires_at'] = time.time() + self.oauth2_token['expires_in'] - 300
        self.save_oauth2_token()

        print("New OAuth2 token has been generated and saved.")

    def refresh_token(self):
        with self.refresh_lock:
            try:
                print("Attempting to refresh OAuth2 token...")
                new_token = self.oauth2_user_handler.refresh_token(self.oauth2_token['refresh_token'])
                self.oauth2_token.update(new_token)
                self.oauth2_token['expires_at'] = time.time() + new_token['expires_in'] - 300
                self.save_oauth2_token()
                print("OAuth2 token has been successfully refreshed and updated.")
                return True
            except Exception as e:
                print(f"Error refreshing token: {e}")
                return False

    def ensure_oauth2_token(self):
        if not self.oauth2_token:
            if not self.load_oauth2_token():
                print("No existing token found. Running initial OAuth2 setup.")
                self.initial_oauth2_setup()
                return

        current_time = time.time()
        if self.oauth2_token.get('expires_at', 0) - current_time < 600:  # Less than 10 minutes until expiry
            print("Token close to expiry, attempting to refresh...")
            if not self.refresh_token():
                print("Token refresh failed. Running initial OAuth2 setup again.")
                self.initial_oauth2_setup()

    def start_refresh_thread(self):
        def refresh_loop():
            while True:
                self.ensure_oauth2_token()
                time_to_expiry = self.oauth2_token.get('expires_at', 0) - time.time()
                sleep_time = min(time_to_expiry - 600, 3600)  # Sleep until 10 mins before expiry or for 1 hour, whichever is shorter
                time.sleep(max(sleep_time, 60))  # Ensure we sleep for at least 1 minute

        self.refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        self.refresh_thread.start()

    def get_client(self):
        self.ensure_oauth2_token()
        return tweepy.Client(self.oauth2_token['access_token'])