import tkinter as tk
from tkinter import filedialog
import csv
 
#text_widget.delete(1.0, tk.END)  # Clear previous content
#text_widget.insert(tk.END, array_file)

def open_file():
    file_path = filedialog.askopenfilename(
        title="Select a Text File", filetypes=[("Text files", "*.csv")])
    if file_path:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            array_file = list(csv_reader)
            array_file_length = len(array_file)
            text_widget.delete(1.0, tk.END)  # Clear previous content

            product_code = []
            quantity = []

            x = 1

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
 
# Create the main window
root = tk.Tk()
root.title("Text File Reader")
 
# Create a Text widget to display the content
text_widget = tk.Text(root, wrap="word", width=40, height=10)
text_widget.pack(pady=10)
 
# Create a button to open the file
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(pady=10)
 
# Run the Tkinter event loop
root.mainloop()