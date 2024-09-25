from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/unfollow_user', methods=['POST'])
@token_required
def unfollow_user():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Missing username'}), 400

    try:
        result = current_app.x_service.unfollow_user(username)

        if result['following'] is False:
            response_message = f"Successfully unfollowed user @{username}."
        else:
            response_message = f"Failed to unfollow user @{username}. Current following status: {result['following']}"

        return jsonify({
            'success': True,
            'message': response_message,
            'following': result['following']
        }), 200

    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': 'User not found',
            'message': str(ve)
        }), 404
    except Exception as e:
        current_app.logger.error(f"Error unfollowing user @{username}: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while unfollowing the user',
            'message': str(e)
        }), 500