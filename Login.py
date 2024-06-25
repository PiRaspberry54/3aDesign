import customtkinter
import tkinter
from tkinter import END
import hashlib
import subprocess

#Used to set the appearance setting of the application being created. Using dark theme if not set application will use the devices settings.
customtkinter.set_appearance_mode("dark")
#Setting the colour theme of the application to dark blue but can also be set to green or blue. 
customtkinter.set_default_color_theme("green")

login_window = customtkinter.CTk()

# Represents the size of the window for the application
window_width = 600
window_height = 400

# Get the screen width and height
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()

# Calculate the position coordinates to center the window
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

# Set the geometry of the window with the calculated position
login_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

#Name for application
login_window.title("DigiKey Pricing Application")

#Function responsible for login authentication 
def login():

    #This is just for demonstration purposes in actual delivery application this will be substituted for reading from and comparing records in the login database
    username = str("admin")
    password = str("admin")

    #Retrieving data from user input from login form
    entered_username = entry_username.get()
    entered_password = entry_password.get()

    #Hashing password
    enc = password.encode()
    hash = hashlib.sha384(enc).hexdigest()

    #Hashing retrieved user password entered in
    enc_entered_password = entered_password.encode()
    entered_password_hash = hashlib.sha384(enc_entered_password).hexdigest()

    if hash == entered_password_hash and entered_username == username:
            selected_appearance_mode = appearance_mode_optionemenu.get()
            subprocess.run(["python3", "DigikeyPricing.py", selected_appearance_mode])
    else:
          entry_username.delete(0, END)
          entry_password.delete(0, END)

def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

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


login_window.mainloop()