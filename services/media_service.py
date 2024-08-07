class MediaService:
    def __init__(self, oauth1_api):
        self.api = oauth1_api

    def upload_media(self, media_file):
        upload_response = self.api.media_upload(media_file)
        return upload_response.media_id