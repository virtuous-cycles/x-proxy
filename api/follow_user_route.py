from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/follow_user', methods=['POST'])
@token_required
def follow_user():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Missing username'}), 400

    try:
        result = current_app.x_service.follow_user(username)

        if result.get('following') is True and result.get('pending_follow') is False:
            response_message = f"Successfully followed user @{username}."
        elif result.get('following') is False and result.get('pending_follow') is True:
            response_message = f"Follow request sent to @{username}. Waiting for user approval."
        else:
            response_message = f"Follow operation for @{username} completed, but the status is unclear."

        return jsonify({
            'success': True,
            'message': response_message,
            'following': result.get('following'),
            'pending_follow': result.get('pending_follow')
        }), 200

    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': 'User not found',
            'message': str(ve)
        }), 404
    except Exception as e:
        current_app.logger.error(f"Error following user @{username}: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while following the user',
            'message': str(e)
        }), 500