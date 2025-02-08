import os
import random
import requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def get_random_song():
    token = ACCESS_TOKEN
    if not token:
        return {'error': 'Failed to get token'}
    playlist_url = f"https://api.spotify.com/v1/playlists/2xutOn4Ea4RyjuaRaD3jl3"
    response = requests.get(playlist_url, headers={"Authorization": f"Bearer {token}"})
    print(response.text)

    if response.status_code != 200:
        return {'error': f'Failed to fetch playlist: {response.status_code}'}, 500
    
    tracks = response.json().get('tracks', {}).get('items', [])
    if not tracks:
        return {'error': 'No tracks found in playlist'}, 404
    
    random_track = random.choice(tracks)['track']
    return {
        'name': random_track['name'],
        'artist': random_track['artists'][0]['name'],
        'album': random_track['album']['name'],
        'release_date': random_track['album']['release_date'],
        'image': random_track['album']['images'][0]['url'],
        'preview': random_track['preview_url']
    }