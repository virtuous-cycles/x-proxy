from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/search_tweets', methods=['GET'])
@token_required
def search_tweets():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing query'}), 400
    tweets = current_app.x_service.search_recent_tweets(query)
    return jsonify({'tweets': tweets})