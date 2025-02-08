from flask import Flask, jsonify
from flask_cors import CORS
from get_song import SpotifyClient

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({'message': 'Are we live??'})
#app.register_blueprint(referrers,    url_prefix='/referrers')

@app.route('/api/random-song', methods=['GET'])
def random_song():
    try:
        spotify_client = SpotifyClient()
        song_info = spotify_client.get_random_song()
        
        if not song_info:
            return jsonify({'error': 'No song found'}), 404
            
        return jsonify(song_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)    