from flask import Flask, request
import requests

app = Flask(__name__)

CLIENT_ID = 'rXGxqKihBJyWiwA01RVirnkrZkXEtmJg'
CLIENT_SECRET = 'Cljv4n0WkEcg6IqF'
REDIRECT_URI = 'https://localhost:5000/callback'
TOKEN_URL = 'https://api.digikey.com/v1/oauth2/token'

access_token = None

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    if code:
        data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        response = requests.post(TOKEN_URL, data=data)
        if response.status_code == 200:
            global access_token
            access_token = response.json().get("access_token")
            return "Authorization complete. You can close this window."
    return "Failed to get authorization code"

if __name__ == '__main__':
    app.run(port=5000)
