from flask import request, jsonify, current_app
from . import api_bp
from auth import token_required

@api_bp.route('/post_tweet', methods=['POST'])
@token_required
def post_tweet():
    data = request.json
    text = data.get('text')
    in_reply_to_tweet_id = data.get('in_reply_to_tweet_id')
    media_ids = data.get('media_ids')
    if not text:
        return jsonify({'error': 'Missing text'}), 400
    tweet_id = current_app.x_service.post_tweet(text, in_reply_to_tweet_id, media_ids)
    return jsonify({'tweet_id': tweet_id})