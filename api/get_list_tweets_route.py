from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/get_list_tweets', methods=['GET'])
@token_required
def get_list_tweets():
  """
  Get tweets from a specified X list.

  Query Parameters:
  - list_id: The ID of the list to fetch tweets from
  - max_results: Optional. Number of tweets to return (1-100, default 100)
  - pagination_token: Optional. Token for pagination
  """
  list_id = request.args.get('list_id')
  max_results = request.args.get('max_results', type=int)
  pagination_token = request.args.get('pagination_token')

  if not list_id:
      return jsonify({'error': 'Missing list_id parameter'}), 400

  try:
      tweets = current_app.x_service.get_list_tweets(
          list_id=list_id,
          max_results=max_results,
          pagination_token=pagination_token
      )
      return jsonify(tweets)
  except Exception as e:
      current_app.logger.error(f"Error retrieving list tweets: {str(e)}", exc_info=True)
      return jsonify({
          'error': 'An error occurred while retrieving list tweets',
          'message': str(e)
      }), 500