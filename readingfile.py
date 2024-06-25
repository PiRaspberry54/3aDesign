import tkinter as tk
from tkinter import filedialog
import csv
import requests
 
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

            product_code = []
            quantity = []

            product_found = []
            product_notFound = []
        
            #By starting at one you can remove the first line which is headers
            x = 1

            access_token = get_access_token(client_id, client_secret)
            #print(f'Access Token: {access_token}')

            #Goes through each line of the file and looks for the two columns and places them into a variable to be used for api call
            while array_file_length > x:
                current_line = array_file[x]
                product_code_value = current_line[4]
                quantity_value = current_line[1]
                product_code.append(product_code_value)
                quantity.append(quantity_value)
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
                    product_found_string = 'Product Number: ' + product_code_value + ' Unit Price: £' + unit_price_string + ' Quantity: ' + quantity_value + ' Total Price: £' + total_price_string
                    product_found.append(product_found_string)
            
            num_products_found = len(product_found)
            num_products_notFound = len(product_notFound)
            #print(f"Product found unit price: {product_found}")
            #print(f"Product not found: {product_notFound}")
            #print(num_products_found)
            #print(num_products_notFound)

            i = 0
            e = 0

            while num_products_found > i:
                #print("Products found: ")
                current_line_product_found = product_found[i]
                #print(current_line_product_found)
                text_widget.insert(tk.END, current_line_product_found)
                i = i + 1
            
            while num_products_notFound > e:
                #print("Products not found: ")
                current_line_product = product_notFound[e]
                #print(current_line_product)
                text_widget2.insert(tk.END, current_line_product)
                e = e + 1
            #print(f"Quantities: {quantity}")
 
# Create the main window
root = tk.Tk()
root.title("Text File Reader")
 
# Create a Text widget to display product pricing
text_widget = tk.Text(root, wrap="word", width=40, height=10)
text_widget.pack(pady=10)

#Creatte a Text widget to display information on products not found
text_widget2 = tk.Text(root, wrap="word", width=40, height=10)
text_widget2.pack(pady=10)
 
# Create a button to open the file
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(pady=10)
 
# Run the Tkinter event loop
root.mainloop()