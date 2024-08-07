from flask import request, jsonify, current_app
from . import api_bp
from auth import token_required

@api_bp.route('/post_reply', methods=['POST'])
@token_required
def post_reply():
    data = request.json
    tweet_id = data.get('tweet_id')
    text = data.get('text')
    if not tweet_id or not text:
        return jsonify({'error': 'Missing tweet_id or text'}), 400
    reply_id = current_app.x_service.post_reply(tweet_id, text)
    return jsonify({'reply_id': reply_id})