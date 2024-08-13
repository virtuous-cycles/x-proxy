from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/post_draft_tweet', methods=['POST'])
@token_required
def post_draft_tweet():
    data = request.json
    draft_tweet_record_id = data.get('draft_tweet_record_id')

    if not draft_tweet_record_id:
        return jsonify({'error': 'Missing draft_tweet_record_id'}), 400

    result = current_app.combined_services.post_draft_tweet(draft_tweet_record_id)

    if 'error' in result:
        return jsonify(result[0]), result[1]

    return jsonify(result)