from flask import request, jsonify, current_app
from . import api_bp
from auth import token_required

@api_bp.route('/get_tweet', methods=['GET'])
@token_required
def get_tweet():
    tweet_id = request.args.get('tweet_id')
    if not tweet_id:
        return jsonify({'error': 'Missing tweet_id'}), 400
    tweet = current_app.x_service.get_tweet(tweet_id)
    return jsonify({'tweet': tweet.data if tweet else None})