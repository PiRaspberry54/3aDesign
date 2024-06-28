import tkinter as tk
from tkinter import filedialog
import csv
import requests
import customtkinter
from tkinter import END
import sys
 
#text_widget.delete(1.0, tk.END)  # Clear previous content
#text_widget.insert(tk.END, array_file)

# Client id and secret used for authentication
client_id = 'rXGxqKihBJyWiwA01RVirnkrZkXEtmJg'
client_secret = 'Cljv4n0WkEcg6IqF'

# URL to get the access token
token_url = 'https://api.digikey.com/v1/oauth2/token'

# Function to get access token
def get_access_token(client_id, client_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        #Taken from documentation standard entry to be given to parameter
        'grant_type': 'client_credentials'
    }
    #Post command used to make request to authentication server
    response = requests.post(token_url, headers=headers, data=data)
    #response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    token_info = response.json()
    return token_info['access_token']

# Function to make an API call. 
def make_api_call(api_url, access_token):
    #Headers used for REST APIs allowing addititional information to be sent in GET request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-DIGIKEY-Client-Id': client_id,
        'X-DIGIKEY-Locale-Site': 'UK',
        'X-DIGIKEY-Locale-Language': 'en',
        'X-DIGIKEY-Locale-Currency': 'GBP',
        'X-DIGIKEY-Customer-Id': '0',
    }
    response = requests.get(api_url, headers=headers)
    #HTTP error if the HTTP request returned an unsuccessful status code
    #response.raise_for_status()
    return response.json()

def fifty_units(json, units):
    breakpoint_json_data = get_breakpoint(json)
    breakpoint_options = get_breakpoint_options(breakpoint_json_data)
    num_units = units * 50
    breakpoint = choose_breakpoint(breakpoint_options, num_units)

    price = price_calculator(breakpoint_json_data, breakpoint)

    print(breakpoint_options)
    print(num_units)
    print(breakpoint)
    print(price)

    #While loop is to catch any products that are greater than the largest breakpoint and therefore require additional packets to be brought
    while num_units > breakpoint:
        num_units = num_units - breakpoint
        breakpoint = choose_breakpoint(breakpoint_options, num_units)
        price = price + choose_breakpoint(breakpoint_options, num_units)

        print(breakpoint)
        print(price)
    
    return price

def price_calculator(json_data, quantity):
    # Find the corresponding pricing information
    selected_pricing = None
    for pricing_info in json_data['StandardPricing']:
        if pricing_info['BreakQuantity'] == quantity:
            selected_pricing = pricing_info['TotalPrice']
            break
    return selected_pricing

#Compares options available with unit amount to select correct breakpoint
def choose_breakpoint(options, units):
    array_length = len(options)
    option_selected = 0
    
    #For loop iterating through entire length of array of options
    for i in range(array_length):
        #Starts by comparing first option with unit to see if they are the same if so ends search
        if options[i] == units:
            option_selected = options[i]
            break
        #Checks the other options not including last as there be know next option
        elif i < len(options) - 1:
            current_option = options[i]
            next_option = options[i + 1]
            #Looks to see if next option than but bigger then current option
            if current_option <= units < next_option:
                option_selected = next_option
                break
            #Else current option is correct as smaller than current option
            elif units < current_option:
                option_selected = current_option
                break
            else:
                option_selected = next_option
    
    #If unit is larger than biggest option breakpoint returned is large option.
    if units >= options[-1]:
        option_selected = options[-1]
    
    #Used if there is only one option
    if option_selected == 0:
        option_selected = options[0]
    
    return option_selected

#Function will take the json data and discover what the different breakpoint options are
def get_breakpoint_options(json):
        #Array to hold breakpoint options
    breakpoints = []
    for options in json['StandardPricing']:
        breakpoint_value = options['BreakQuantity']
        breakpoints.append(breakpoint_value)
    return breakpoints
        
#Function for getting json data for breakpoint of prices
#Looking to see package type options and return json data for package type option that is appropriate 
def get_breakpoint(json):
    #Iterates through to see if bulk option is available 
    json_data = None
    product_variations = json['Product']['ProductVariations']
    
    # Loop through to find bulk product otion if it exisists 
    for variation in product_variations:
        if variation['PackageType']['Name'] == 'Bulk':
            json_data = variation
            break
    
    for variation in product_variations:
        if variation['PackageType']['Name'] == 'Cut Tape (CT)':
            json_data = variation
            break   

    return json_data

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
            text_widget.delete(1.0, tk.END)  # Clear previous content

            #Initialise empty arrays for storing product info from request of recording records that weren't recored.
            product_found = []
            product_notFound = []

            running_total_price = 0
        
            #By starting at one you can remove the first line which is headers
            x = 1

            access_token = get_access_token(client_id, client_secret)
            #print(f'Access Token: {access_token}')

            #Goes through each line of the file and looks for the two columns and places them into a variable to be used for api call
            while array_file_length > x:
                current_line = array_file[x]
                product_code_value = current_line[4]
                quantity_value = current_line[1]
                x = x+1
                # URL to make the API call taken from documentation (needs to be updated using information from )
                apiProduct = product_code_value 
                api_url = ("https://api.digikey.com/products/v4/search/%s/productdetails" %(apiProduct))

                # Calling make api call function to retrieve information from api on product information
                api_response = make_api_call(api_url, access_token)
                #Checking to see if status has been returned in json data. Indicating product hasn't been found
                if 'status' in api_response:
                    #404 error indicates no product has been found
                    if api_response['status'] == 404:
                        current_line_string = ','.join(current_line)
                        product_notFound.append(current_line_string)
                        #print("Product not found")
                    #Different error being produced and product still hasn't been found.
                    else:
                        product_notFound.append(current_line)
                #No status and therefore no error indicating that everything is working and therefore a product has been found.
                else:
                    unit_price = api_response.get('Product', {}).get('UnitPrice')
                    quantity_value_int = int(quantity_value)
                    total_price = unit_price*quantity_value_int
                    total_price_rounded = round(total_price, 2)
                    unit_price_string = str(unit_price)
                    total_price_string = str(total_price_rounded)
                    running_total_price = running_total_price + total_price_rounded
                    product_found_string = 'Product Number:  ' + product_code_value + '  Unit Price: £' + unit_price_string + '  Quantity: ' + quantity_value + '  Price: £' + total_price_string
                    product_found.append(product_found_string)
                    fifty_units(api_response, quantity_value_int)
            
            num_products_found = len(product_found)
            num_products_notFound = len(product_notFound)

            i = 0
            e = 0

            text_widget.delete(1.0, tk.END)  # Clear previous content
            #Insert each line into the first textbox for products found
            while num_products_found > i:
                current_line_product_found = product_found[i]
                text_widget.insert(tk.END, current_line_product_found + '\n')
                i = i + 1
            
            #Adding total price
            running_total_price_Tostring = str(running_total_price)
            running_total_price_string = "Total Price: £" + running_total_price_Tostring
            text_widget.insert(tk.END, running_total_price_string)
            
            text_widget2.delete(1.0, tk.END)  # Clear previous content
            #Insert each line into the second text box for products not found
            while num_products_notFound > e:
                current_line_product = product_notFound[e]
                text_widget2.insert(tk.END, current_line_product + '\n')
                e = e + 1
 
# Create the main window
application_window = customtkinter.CTk()

# Get the appearance mode from command line arguments
appearance_mode = sys.argv[1] if len(sys.argv) > 1 else "System"
customtkinter.set_appearance_mode(appearance_mode)
customtkinter.set_default_color_theme("green")

# Get the screen width and height
screen_width = application_window.winfo_screenwidth()
screen_height = application_window.winfo_screenheight()

# Set the geometry of the window with the calculated position
application_window.geometry(f"{screen_width}x{screen_height}")

#Name for application
application_window.title("DigiKey Pricing Application")

frame = customtkinter.CTkFrame(master=application_window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

#Title for application
application_window_label = customtkinter.CTkLabel(master=frame, text="DigiKey Price Calculator", font=("Roboto", 30))
application_window_label.pack(pady=30, padx=10)

#Label for text box
text_widget_label = customtkinter.CTkLabel(master=frame, text="DigiKey Product Pricing", font=("Roboto", 20))
text_widget_label .pack(pady=10, padx=5)
# Create a Text widget to display product pricing
text_widget = customtkinter.CTkTextbox(master=frame, font=("Roboto", 16))
text_widget.pack(pady=20, padx=40, fill="both", expand=True)

#Label for text box
text_widget2_label = customtkinter.CTkLabel(master=frame, text="Unfound Products", font=("Roboto", 20))
text_widget2_label.pack(pady=10, padx=5)
#Creatte a Text widget to display information on products not found
text_widget2 = customtkinter.CTkTextbox(master=frame, font=("Roboto", 16))
text_widget2.pack(pady=20, padx=40, fill="both", expand=True)
 
# Create a button to open the file
open_button = customtkinter.CTkButton(master=frame, text="Open File", command=open_file)
open_button.pack(pady=10)
 
# Run the Tkinter event loop
application_window.mainloop()