from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/get_home_timeline', methods=['GET'])
@token_required
def get_home_timeline():
    max_results = request.args.get('max_results', default=15, type=int)
    pagination_token = request.args.get('pagination_token', default=None, type=str)

    try:
        timeline = current_app.x_service.get_home_timeline(
            max_results=max_results,
            pagination_token=pagination_token
        )
        return jsonify(timeline)
    except Exception as e:
        current_app.logger.error(f"Error retrieving home timeline: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while retrieving the home timeline'}), 500