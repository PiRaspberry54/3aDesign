import customtkinter
import tkinter as tk
from tkinter import END
from customtkinter import filedialog
import hashlib
import csv

# Set appearance and color theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

def open_file():
    file_path = filedialog.askopenfilename(
        title="Select a Text File", filetypes=[("Text files", "*.csv")])
    if file_path:
        with open(file_path, 'r') as file:
          #Uses CSV library to correctly read the csv file
          csv_reader = csv.reader(file)
          #Place each line of the file into a list
          array_file = list(csv_reader)
          #Used to discover length of the file to be used for while loop to go through each line
          array_file_length = len(array_file)

          product_code = []
          quantity = []
      
          #By starting at one you can remove the first line which is headers
          x = 1

          #Goes through each line of the file and looks for the two columns and places them into a variable to be used for api call
          while array_file_length > x:
              current_line = array_file[x]
              product_code_value = current_line[4]
              quantity_value = current_line[1]
              product_code.append(product_code_value)
              quantity.append(quantity_value)
              x = x+1
          
          print(f"Total rows: {array_file_length}")
          print(f"Product Codes: {product_code}")
          print(f"Quantities: {quantity}")

# Function to create the main application window
def main_application():
    # Close the login window
    login_window.destroy()

    # Create the main application window
    application_window = customtkinter.CTk()

    # Get screen dimensions
    application_screen_width = application_window.winfo_screenwidth()
    application_screen_height = application_window.winfo_screenheight()

    # Size the window to fill the entire screen
    application_window.geometry(f"{application_screen_width}x{application_screen_height}")

    # Set the name of the application
    application_window.title("DigiKey Pricing Application")

    # Create a frame for the main application window
    application_window_frame = customtkinter.CTkFrame(master=application_window)
    application_window_frame.pack(pady=75, padx=150, fill="both", expand=True)

    # Create a label for the main application window
    application_window_label = customtkinter.CTkLabel(master=application_window_frame, text="DigiKey Price Calculation", font=("Roboto", 30))
    application_window_label.pack(pady=30, padx=10)

    open_button = customtkinter.CTkButton(master=application_window_frame, text="Open file", command=open_file)
    open_button.pack(pady=10)
    # Start the main application window's event loop
    application_window.mainloop()

# Create the login window
login_window = customtkinter.CTk()

# Set the size of the login window
window_width = 600
window_height = 400

# Get screen width and height
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()

# Calculate the position coordinates to center the window
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

# Set the geometry of the window with the calculated position
login_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Set the name of the login window
login_window.title("DigiKey Pricing Application")

# Function responsible for login authentication
def login():
    username = "admin"
    password = "admin"

    # Retrieve data from user input
    entered_username = entry_username.get()
    entered_password = entry_password.get()

    # Hash the password
    enc = password.encode()
    hash = hashlib.sha384(enc).hexdigest()

    # Hash the entered password
    enc_entered_password = entered_password.encode()
    entered_password_hash = hashlib.sha384(enc_entered_password).hexdigest()

    # Check if the hashed passwords match
    if hash == entered_password_hash and entered_username == username:
        main_application()
    else:
        entry_username.delete(0, END)
        entry_password.delete(0, END)

# Function to change appearance mode
def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

# Create the login window frame
frame = customtkinter.CTkFrame(master=login_window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Create the login system label
label = customtkinter.CTkLabel(master=frame, text="Login System", font=("Roboto", 28))
label.pack(pady=20, padx=10)

# Create the username entry
entry_username = customtkinter.CTkEntry(master=frame, placeholder_text="Username", width=300)
entry_username.pack(pady=24, padx=10)

# Create the password entry
entry_password = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*", width=300)
entry_password.pack(pady=24, padx=10)

# Create the login button
button = customtkinter.CTkButton(master=frame, text="login", command=login)
button.pack(pady=12, padx=10)

# Create the appearance mode option menu
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(master=frame, values=["Light", "Dark", "System"], command=change_appearance_mode_event, width=200)
appearance_mode_optionemenu.pack(pady=30, padx=20)

# Start the login window's event loop
login_window.mainloop()