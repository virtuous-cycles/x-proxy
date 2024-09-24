from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/get_tweet', methods=['GET'])
@token_required
def get_tweet():
    tweet_id = request.args.get('tweet_id')
    if not tweet_id:
        return jsonify({'error': 'Missing tweet_id'}), 400

    # Get the conversation thread, including the original tweet
    thread = current_app.x_service.get_conversation_thread(tweet_id)

    if not thread:
        return jsonify({'error': 'Tweet not found'}), 404

    # Find the original tweet in the thread
    original_tweet = next((tweet for tweet in thread if tweet['id'] == tweet_id), None)

    if not original_tweet:
        return jsonify({'error': 'Original tweet not found in the conversation'}), 404

    result = {
        'original_tweet': original_tweet,
        'thread': thread
    }

    return jsonify(result)