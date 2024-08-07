from .oauth_handler import get_oauth1_api

class MediaService:
    def __init__(self):
        self.api = get_oauth1_api()

    def upload_media(self, media_file):
        upload_response = self.api.media_upload(media_file)
        return upload_response.media_id