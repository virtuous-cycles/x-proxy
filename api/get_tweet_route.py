from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/get_tweet', methods=['GET'])
@token_required
def get_tweet():
    """
    Get a tweet along with its context in the conversation.

    Returns:
    - requested_tweet: The tweet requested by the user
    - root_tweet: The root tweet of the conversation
    - ancestor_chain: Chain of tweets from root to the parent of the requested tweet
    - sibling_tweets: Tweets that share the same parent as the requested tweet, ordered from oldest to newest
    - children_tweets: Direct replies to the requested tweet, ordered from oldest to newest
    """
    tweet_id = request.args.get('tweet_id')
    if not tweet_id:
        return jsonify({'error': 'Missing tweet_id'}), 400

    try:
        result = current_app.x_service.get_tweet_with_thread(tweet_id)

        if not result:
            return jsonify({'error': 'Tweet not found or unable to retrieve thread'}), 404

        return jsonify(result)

    except Exception as e:
        # Log the error
        current_app.logger.error(f"Error retrieving tweet {tweet_id}: {str(e)}", exc_info=True)
        # Re-raise the exception to be handled by the global error handler
        raise