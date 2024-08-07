from flask import request, jsonify, current_app
from . import api_bp
from auth import token_required

@api_bp.route('/upload_media', methods=['POST'])
@token_required
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    media_id = current_app.x_service.upload_media(file)
    return jsonify({'media_id': media_id})