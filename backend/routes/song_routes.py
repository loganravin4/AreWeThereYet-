from flask import Blueprint, jsonify
from flask import request
from backend.input_song import check_song_match
from backend.get_song import get_random_song
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
    
@song_blueprint.route('/validate-song', methods=['POST'])
def validate_song():
    """
    Validate the song that the user has guessed
    IM LAYING OUT FOUNDATION, WE NEED TO CHANGE VARIABLE NAMES AND STUFF BASED ON THE NAMES OF FIELDS IN FRONTEND
    """
    try:
        data = request.get_json()
        if "user_input" not in data or "correct_song" not in data:
            return jsonify({'error': 'Invalid request'}), 400
        
        user_input = data['user_input']
        correct_song = data['correct_song']

        is_match = check_song_match(user_input, correct_song)

        return jsonify({'is_match': is_match})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500