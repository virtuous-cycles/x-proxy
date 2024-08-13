from flask import jsonify, current_app
from api import api_bp
from auth import token_required

@api_bp.route('/get_drafts', methods=['GET'])
@token_required
def get_drafts():
    drafts = current_app.airtable_service.get_candidate_tweets()
    return jsonify({'drafts': drafts})