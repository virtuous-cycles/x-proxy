from flask import jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/pull_mentions', methods=['GET'])
@token_required
def pull_mentions():
    mentions = current_app.x_service.pull_mentions()
    return jsonify({'mentions': mentions})