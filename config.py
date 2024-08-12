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

    # Airtable configurations
    AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
    AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']
    AIRTABLE_CANDIDATE_TWEETS_TABLE_ID = os.environ['AIRTABLE_CANDIDATE_TWEETS_TABLE_ID']
    AIRTABLE_TWEET_BUFFER_VIEW_ID = os.environ['AIRTABLE_TWEET_BUFFER_VIEW_ID']