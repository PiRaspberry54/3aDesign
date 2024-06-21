import customtkinter
import tkinter
from tkinter import END
import hashlib
import requests
import webbrowser
import urllib.parse
from flask import Flask, request, redirect

# Digi-Key API credentials and endpoints
CLIENT_ID = 'rXGxqKihBJyWiwA01RVirnkrZkXEtmJg'
CLIENT_SECRET = 'Cljv4n0WkEcg6IqF'
REDIRECT_URI = 'https://localhost:5000/callback'
AUTHORIZATION_URL = 'https://api.digikey.com/v1/oauth2/authorize'
TOKEN_URL = 'https://api.digikey.com/v1/oauth2/token'

# Initialize Flask app
app = Flask(__name__)

# Set up Flask route to handle the callback
@app.route('/callback')
def callback():
    code = request.args.get('code')
    exchange_code_for_token(code)
    return "Authorization complete. You can close this window."

# Function to open the authorization URL in the default web browser
def get_authorization_code():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI
    }
    auth_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    webbrowser.open(auth_url)

# Function to exchange authorization code for access token
def exchange_code_for_token(code):
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
        print("Access token:", access_token)
    else:
        print("Failed to get access token")

# Function to fetch data from Digi-Key API
def fetch_data():
    url = "https://api.digikey.com/Search/v3/Products/{product_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-DIGIKEY-Client-Id": CLIENT_ID
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        display_data(data)
    else:
        print("Failed to retrieve data")

def display_data(data):
    # Placeholder function to display fetched data
    print(data)

# Function responsible for loading main application
def main_application():
    login_window.destroy()
    application_window = customtkinter.CTk()
    application_window.geometry(f"{screen_width}x{screen_height}")
    application_window.title("DigiKey Pricing Application")

    application_window_frame = customtkinter.CTkFrame(master=application_window)
    application_window_frame.pack(pady=75, padx=150, fill="both", expand=True)

    application_window_label = customtkinter.CTkLabel(master=application_window_frame, text="DigiKey Price Calculation", font=("Roboto", 30))
    application_window_label.pack(pady=30, padx=10)

    fetch_button = customtkinter.CTkButton(master=application_window_frame, text="Fetch Data", command=fetch_data)
    fetch_button.pack(pady=12, padx=10)

    application_window.mainloop()

# Function to handle the login and open authorization URL
def login():
    # This is just for demonstration purposes
    username = "admin"
    password = "admin"

    entered_username = entry_username.get()
    entered_password = entry_password.get()

    enc = password.encode()
    hash = hashlib.sha384(enc).hexdigest()

    enc_entered_password = entered_password.encode()
    entered_password_hash = hashlib.sha384(enc_entered_password).hexdigest()

    if hash == entered_password_hash and entered_username == username:
        main_application()
        get_authorization_code()
    else:
        entry_username.delete(0, END)
        entry_password.delete(0, END)

# Function to change appearance mode
def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

# Set up the login window
login_window = customtkinter.CTk()
window_width = 600
window_height = 400
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
login_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
login_window.title("DigiKey Pricing Application")

frame = customtkinter.CTkFrame(master=login_window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login System", font=("Roboto", 28))
label.pack(pady=20, padx=10)

entry_username = customtkinter.CTkEntry(master=frame, placeholder_text="Username", width=300)
entry_username.pack(pady=24, padx=10)

entry_password = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*", width=300)
entry_password.pack(pady=24, padx=10)

button = customtkinter.CTkButton(master=frame, text="login", command=login)
button.pack(pady=12, padx=10)

appearance_mode_optionemenu = customtkinter.CTkOptionMenu(master=frame, values=["Light", "Dark", "System"], command=change_appearance_mode_event, width=200)
appearance_mode_optionemenu.pack(pady=30, padx=20)

# Start the Flask server in a separate thread to handle the OAuth callback
import threading
flask_thread = threading.Thread(target=lambda: app.run(port=5000, debug=True, use_reloader=False))
flask_thread.start()

login_window.mainloop()
