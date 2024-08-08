import os

class Config:
    # OAuth 2.0 credentials
    CLIENT_ID = os.environ['client_id']
    CLIENT_SECRET = os.environ['client_secret']
    REDIRECT_URI = os.environ['redirect_uri']

    # OAuth 1.0a credentials
    CONSUMER_KEY = os.environ['consumer_key']
    CONSUMER_SECRET = os.environ['consumer_secret']
    ACCESS_TOKEN = os.environ['access_token']
    ACCESS_TOKEN_SECRET = os.environ['access_token_secret']
    # ACCESS_TOKEN = os.environ['const_labs_access_token']
    # ACCESS_TOKEN_SECRET = os.environ['const_labs_access_token_secret']

    # Other configurations
    API_SECRET_KEY = os.environ['API_SECRET_KEY']
    TRUTH_TERMINAL_TWITTER_ID = os.environ['truth_terminal_twitter_id']