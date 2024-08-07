import os

class Config:
    API_SECRET_KEY = os.environ['API_SECRET_KEY']
    REDIRECT_URI = os.environ['redirect_uri']
    CLIENT_ID = os.environ['client_id']
    CLIENT_SECRET = os.environ['client_secret']
    # ACCESS_TOKEN = os.environ['access_token']
    ACCESS_TOKEN = os.environ['const_labs_access_token']
    # ACCESS_TOKEN_SECRET = os.environ['access_token_secret']
    ACCESS_TOKEN_SECRET = os.environ['const_labs_access_token_secret']
    CONSUMER_KEY = os.environ['consumer_key']
    CONSUMER_SECRET = os.environ['consumer_secret']
    TRUTH_TERMINAL_TWITTER_ID = os.environ['truth_terminal_twitter_id']

    # These are only used for initial setup or if the JSON file is missing
    OAUTH2_OFFLINE_FULL_ACCESS_TOKEN = os.environ.get('oauth2_offline_full_access_token', '')
    OAUTH2_REFRESH_TOKEN = os.environ.get('oauth2_refresh_token', '')