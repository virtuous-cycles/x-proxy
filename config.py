import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists, otherwise Replit should still load its secrets
load_dotenv()


class Config:
    # OAuth 2.0 credentials
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    REDIRECT_URI = os.environ['REDIRECT_URI']

    # OAuth 1.0a credentials
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

    # Other configurations
    API_SECRET_KEY = os.environ['API_SECRET_KEY']
    TWITTER_USER_ID = os.environ['TWITTER_USER_ID']

    # Airtable configurations
    AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
    AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']
    AIRTABLE_CANDIDATE_TWEETS_TABLE_ID = os.environ['AIRTABLE_CANDIDATE_TWEETS_TABLE_ID']
    AIRTABLE_EXOS_DRAFT_TWEETS_VIEW_ID = os.environ['AIRTABLE_EXOS_DRAFT_TWEETS_VIEW_ID']
