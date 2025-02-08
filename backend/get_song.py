import os
import random
import requests
from dotenv import load_dotenv

# load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.token = self.get_token()

    def get_token(self):
        url = "https://accounts.spotify.com/api/token"
        response = requests.post(
            url, 
            data={"grant_type": "client_credentials"}, 
            headers={"Authorization": f"Basic {requests.auth._basic_auth_str(self.client_id, self.client_secret)}"}
        )
        return response.json().get("access_token")

    def get_random_song(self):
        if not self.token:
            return {'error': 'Failed to get token'}
        
        # use 'Today's Top Hits' playlist for popular songs
        playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
        playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(playlist_url, headers=headers)

        if response.status_code != 200:
            return jsonify({'error': 'No tracks found in playlist'}), 404
        
        tracks = response.json().get('tracks', {}).get('items', [])
        if not tracks:
            return None
        
        random_track = random.choice(tracks)['track']

        return {
            'name': random_track['name'],
            'artist': random_track['artists'][0]['name'],
            'album': random_track['album']['name'],
            'release_date': random_track['album']['release_date'],
            'image_url': random_track['album']['images'][0]['url'],
            'preview_url': random_track['preview_url'],
            'external_url': random_track['external_urls']['spotify']
        }