import requests
import tempfile
import os

class MediaService:
    def __init__(self, oauth1_api):
        self.api = oauth1_api

    def upload_media(self, media_file):
        upload_response = self.api.media_upload(filename=media_file)
        return upload_response.media_id

    def download_media(self, media_url):
        try:
            response = requests.get(media_url, stream=True)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile(delete=False, suffix=self._get_file_extension(media_url)) as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                return temp_file.name
        except requests.RequestException as e:
            print(f"Error downloading media: {e}")
            return None

    def _get_file_extension(self, url):
        return os.path.splitext(url)[1]