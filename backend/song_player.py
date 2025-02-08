import json 
import spotipy 
import webbrowser 
import os
import requests
from dotenv import load_dotenv
from get_song import get_random_song

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
def play_random_song():
    random_song = get_random_song()  # Use the function from spotify_utils.py
    if 'error' in random_song:
        print(f"Error: {random_song['error']}")
    else:
        print(f"Playing random song: {random_song['name']} by {random_song['artist']}")
        webbrowser.open(random_song['name'])
        print('Random song preview opened in your browser.')
