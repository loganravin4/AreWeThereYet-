from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({'message': 'Are we live??'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)