import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyClient:
    def __init__(self):
        # Initialize Spotify client with credentials
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
        )
        self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_random_song(self):
        # List of random search characters to get diverse results
        chars = 'abcdefghijklmnopqrstuvwxyz'
        random_char = random.choice(chars)
        
        # Random offset for pagination (0-1000 is Spotify's limit)
        random_offset = random.randint(0, 1000)
        
        # Search for tracks with random character and offset
        results = self.spotify.search(
            q=f'track:{random_char}',
            type='track',
            limit=1,
            offset=random_offset
        )

        if not results['tracks']['items']:
            return None

        track = results['tracks']['items'][0]
        return {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'preview_url': track['preview_url'],
            'external_url': track['external_urls']['spotify'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
        } 