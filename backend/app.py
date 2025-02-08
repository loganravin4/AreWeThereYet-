from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from get_song import get_random_song

app = Flask(__name__)
get_random_song = Blueprint('get_random_song', __name__)

# Enable CORS for all routes
CORS(app)

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({'message': 'Are we live??'})

@get_random_song.route('/api/random-song', methods=['GET'])
def random_song():
    song_info = get_random_song()
    return jsonify(song_info)

app.register_blueprint(get_random_song)

if __name__ == '__main__':
    app.run(port=5000, debug=True)    