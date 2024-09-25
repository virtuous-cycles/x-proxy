from flask import request, jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/follow_user', methods=['POST'])
@token_required
def follow_user():
    data = request.json
    target_user_id = data.get('target_user_id')

    if not target_user_id:
        return jsonify({'error': 'Missing target_user_id'}), 400

    try:
        result = current_app.x_service.follow_user(target_user_id)

        if result.get('following') is True and result.get('pending_follow') is False:
            response_message = "Successfully followed the user."
        elif result.get('following') is False and result.get('pending_follow') is True:
            response_message = "Follow request sent. Waiting for user approval."
        else:
            response_message = "Follow operation completed, but the status is unclear."

        return jsonify({
            'success': True,
            'message': response_message,
            'following': result.get('following'),
            'pending_follow': result.get('pending_follow')
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error following user {target_user_id}: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while following the user',
            'message': str(e)
        }), 500