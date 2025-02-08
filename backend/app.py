# from flask import Flask, jsonify
# from flask_cors import CORS
# from get_song import SpotifyClient

# app = Flask(__name__)
# CORS(app)

# @app.route('/api/test', methods=['GET'])
# def test_api():
#     return jsonify({'message': 'Are we live??'})
# #app.register_blueprint(referrers,    url_prefix='/referrers')

# @app.route('/api/random-song', methods=['GET'])
# def random_song():
#     try:
#         spotify_client = SpotifyClient()
#         song_info = spotify_client.get_random_song()
        
#         if not song_info:
#             return jsonify({'error': 'No song found'}), 404
            
#         return jsonify(song_info)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)    
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from get_song import get_random_song
from input_song import check_song_match
from flask import request

app = Flask(__name__)
get_random_song_bp = Blueprint('get_random_song', __name__)
song_blueprint = Blueprint('songs', __name__)

# Enable CORS for all routes
CORS(app)

def test_api():
    return jsonify({'message': 'Are we live??'})

@get_random_song_bp.route('/api/random-song', methods=['GET'])
def random_song():
    song_info = get_random_song()
    return jsonify(song_info)

@song_blueprint.route('/api/validate-song', methods=['POST'])
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
# @play_random_song_bp.route('/api/random-song-play', methods=['GET'])
# def random_song():
#    song_info = get_random_song()
#    if isinstance(song_info, tuple):  # In case there is a tuple returned (data, status_code)
#         return jsonify(song_info[0]), song_info[1]
#    return jsonify(song_info)

app.register_blueprint(get_random_song_bp)
app.register_blueprint(song_blueprint)

if __name__ == '__main__':
    app.run(port=5000, debug=True)    