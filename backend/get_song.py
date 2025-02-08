import os
import random
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify

app = Flask(__name__)

# load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token():
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, data={"grant_type": "client_credentials"}, headers={"Authorization": f"Basic {requests.auth._basic_auth_str(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)}"})
    return response.json().get("access_token")

def get_random_song():
    token = get_token()
    if not token:
        return {'error': 'Failed to get token'}
    
    playlist_id = "37i9dQZF1DXcBWIGoYBM5M?si=e40e9fb3aa50467c"
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(playlist_url, headers=headers)

    if response.status_code != 200:
        return jsonify({'error': f'Failed to fetch playlist: {response.status_code}'}), 500
    
    tracks = response.json().get('tracks', {}).get('items', [])
    if not tracks:
        return jsonify({'error': 'No tracks found in playlist'}), 404
    
    random_track = random.choice(tracks)['track']

    return jsonify({
        'name': random_track['name'],
        'artist': random_track['artists'][0]['name'],
        'album': random_track['album']['name'],
        'release_date': random_track['album']['release_date'],
        'image': random_track['album']['images'][0]['url'],
        'preview': random_track['preview_url']
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)