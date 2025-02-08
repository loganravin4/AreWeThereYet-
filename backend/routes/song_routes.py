from flask import Blueprint, jsonify
from get_song import SpotifyClient

song_blueprint = Blueprint('songs', __name__)

@song_blueprint.route('/test', methods=['GET'])
def test_api():
    return jsonify({'message': 'Are we live??'})


@song_blueprint.route('/random-song', methods=['GET'])
def random_song():
    try:
        spotify_client = SpotifyClient()
        song_info = spotify_client.get_random_song()
        
        if isinstance(song_info, tuple):  # Error response
            return song_info
        
        if not song_info:
            return jsonify({'error': 'No song found'}), 404
            
        return jsonify(song_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500