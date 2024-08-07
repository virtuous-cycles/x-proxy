from flask import Flask
from api import api_bp
from config import Config
from services.x_service import XService

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize XService and attach it to the app context
    x_service = XService()
    app.x_service = x_service

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def hello():
        return "Greetings, your pseudo-X-API is up and running!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)



# import os
# import tweepy

# # Redirect URI
# redirect_uri = os.environ['redirect_uri']

# # Client ID and Secret
# client_id = os.environ['client_id']
# client_secret = os.environ['client_secret']

# # Access Token and Secret
# access_token = os.environ['access_token']
# access_token_secret = os.environ['access_token_secret']

# # Consumer Key and Secret 
# consumer_key = os.environ['consumer_key']
# consumer_secret = os.environ['consumer_secret']

# # Truth Terminal Twitter ID
# truth_terminal_twitter_id = os.environ['truth_terminal_twitter_id']


# #
# # OAuth 2.0 Client
# #

# # ###############
# # UNCOMMENT AND RUN THIS SECTION FIRST

# oauth2_user_handler = tweepy.OAuth2UserHandler(
#     client_id=client_id,
#     redirect_uri=redirect_uri,
#     scope=[
#         "tweet.read",
#         "tweet.write",
#         "tweet.moderate.write", # Hide and unhide replies to your Tweets
#         "users.read",
#         "follows.read",
#         "follows.write", # Follow and unfollow people for you
#         "offline.access", # Stay connected to your account until you revoke access
#         "space.read",
#         "mute.read",
#         "mute.write", # Mute and unmute accounts for you
#         "like.read",
#         "like.write",
#         "list.read",
#         "list.write", # Create and manage Lists for you
#         "block.read",
#         "block.write", # Block and unblock accounts for you
#         "bookmark.read",
#         "bookmark.write" # Bookmark and remove Bookmarks from Tweets
#     ],
#     client_secret=client_secret
# )

# print("Step 1: Open this URL and approve: " + oauth2_user_handler.get_authorization_url() + "\n")

# print("Step 2: Copy the authorization response URL" + "\n")

# oauth2_authorization_url = input("Step 3: Paste authorization response URL here and press enter: ")

# token = oauth2_user_handler.fetch_token(
#     oauth2_authorization_url
# )
# print()
# print("-- Received: ", token, "\n")

# print("Step 4: set 'oauth2_offline_full_access_token' in Secrets to: ", token['access_token'])