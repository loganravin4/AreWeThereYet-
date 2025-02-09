import os
import requests
from flask import Flask, request, redirect, session, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID") 
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:5000/callback"  # Spotify Redirect URI

# redirects the user to login
@app.route("/login")
def login():
    scope = "user-read-playback-state user-modify-playback-state streaming"
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={SPOTIFY_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&scope={scope}"
    )
    return redirect(auth_url)

# Step 2: Handle Spotify callback & get access token
@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    token_info = response.json()
    
    session["access_token"] = token_info["access_token"]
    session["refresh_token"] = token_info["refresh_token"]
    
    return redirect("http://localhost:5173") 

# Step 3: Endpoint for frontend to get access token
@app.route("/get_token")
def get_token():
    return jsonify({"access_token": session.get("access_token")})

if __name__ == "__main__":
    app.run(debug=True)
