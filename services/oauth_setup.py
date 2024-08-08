from services.oauth2_handler import OAuth2Handler
from services.oauth1_handler import OAuth1Handler
import sys

def initialize_oauth_handlers(config):
    oauth2_handler = OAuth2Handler(
        client_id=config['CLIENT_ID'],
        client_secret=config['CLIENT_SECRET'],
        redirect_uri=config['REDIRECT_URI']
    )

    oauth1_handler = OAuth1Handler(
        consumer_key=config['CONSUMER_KEY'],
        consumer_secret=config['CONSUMER_SECRET'],
        access_token=config['ACCESS_TOKEN'],
        access_token_secret=config['ACCESS_TOKEN_SECRET']
    )

    return oauth2_handler, oauth1_handler

def validate_oauth(oauth2_handler, oauth1_handler):
    try:
        oauth2_handler.ensure_oauth2_token()
        print("OAuth2 token checked and validated.")

        oauth1_handler.initialize()
        if not oauth1_handler.validate_credentials():
            raise Exception("OAuth 1.0a credentials are invalid.")

        print("OAuth validation successful.")
    except Exception as e:
        print(f"Error setting up OAuth: {e}")
        print("Application cannot start due to authentication failure.")
        print("Please ensure you have the necessary permissions and environment variables set.")
        sys.exit(1)

def setup_and_validate_oauth(config):
    oauth2_handler, oauth1_handler = initialize_oauth_handlers(config)
    validate_oauth(oauth2_handler, oauth1_handler)
    return oauth2_handler, oauth1_handler