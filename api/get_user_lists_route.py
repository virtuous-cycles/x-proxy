from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/get_user_lists', methods=['GET'])
@token_required
def get_user_lists():
    """
    Get lists owned by and/or followed by a specified user.

    Query Parameters:
    - user_id: The ID of the user whose lists to retrieve
    - include_owned: Optional boolean (default: true) - Whether to include owned lists
    - include_followed: Optional boolean (default: true) - Whether to include followed lists
    - max_results: Optional integer (1-100, default: 100) - Number of results to return
    - pagination_token: Optional string - Token for pagination
    """
    user_id = request.args.get('user_id')
    include_owned = request.args.get('include_owned', 'true').lower() == 'true'
    include_followed = request.args.get('include_followed', 'true').lower() == 'true'
    max_results = request.args.get('max_results', type=int)
    pagination_token = request.args.get('pagination_token')

    if not user_id:
        return jsonify({'error': 'Missing user_id parameter'}), 400

    if not include_owned and not include_followed:
        return jsonify({'error': 'At least one of include_owned or include_followed must be true'}), 400

    try:
        user_lists = current_app.x_service.get_user_lists(
            user_id=user_id,
            include_owned=include_owned,
            include_followed=include_followed,
            max_results=max_results,
            pagination_token=pagination_token
        )
        return jsonify(user_lists)
    except Exception as e:
        current_app.logger.error(f"Error retrieving user lists: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'An error occurred while retrieving user lists',
            'message': str(e)
        }), 500