import tkinter as tk
from tkinter import ttk, messagebox
import requests
import subprocess

# fetches the list of currencies
def fetch_currency_list():

    try:

        response = requests.get( f"https://api.exchangerate-api.com/v4/latest/PHP" )
        rates = response.json().get( "rates", {} )
        return sorted( rates.keys() )
    
    except Exception as e:

        messagebox.showerror("Error", f"Failed to fetch currency list: {e}")
        return []

# fetches the exchange rates in REAL TIME
def fetch_exchange_rate( currency ):

    try:

        response = requests.get( f"https://api.exchangerate-api.com/v4/latest/PHP" )
        rates = response.json().get("rates", {})
        return rates.get( currency, None )
    
    except Exception as e:

        messagebox.showerror( "Error", f"Failed to fetch exchange rate: {e}" )
        return None

# performs conversion using the Ruby script
def convert_currency():

    try:

        amount = float( entry_amount.get() )
        currency = combo_currency.get()
        rate = fetch_exchange_rate( currency )

        if rate is None:

            messagebox.showerror( "Error", "Invalid currency or failed to fetch rate." )
            return

        # calls Ruby script with subprocess
        result = subprocess.run( ["ruby", "converter.rb", str( amount ), str( rate ) ], capture_output = True, text = True )
        converted_amount = result.stdout.strip()

        label_result.config( text = f"{ amount } PHP = { converted_amount } { currency }" )

    except ValueError:

        messagebox.showerror( "Error", "Please enter a valid amount." )

# creates the main window
root = tk.Tk()
root.title( "PHP Currency Converter" )

# sets the size of the window
root.geometry( "700x400" )

# coffee shop color scheme
main_color = "#6F4E37"  # coffee brown
secondary_color = "#C19A6B"  # light brown
accent_color = "#D2B48C"  # tan
text_color = "#FFF8DC"  # cornsilk

root.configure( bg = main_color )

# title label
label_title = tk.Label( root, text = "PHP Currency Converter", font = ( "Lucida Handwriting", 18, "bold" ), bg = main_color, fg = text_color )
label_title.pack( pady = 20 )

# input field
frame_inputs = tk.Frame( root, bg = main_color )
frame_inputs.pack( pady = 10 )

# amount entry
label_amount = tk.Label( frame_inputs, text = "Amount in PHP:", font = ( "Courier New", 14, "bold" ), bg = main_color, fg = text_color )
label_amount.grid( row = 0, column = 0, padx = 10, pady = 10 )
entry_amount = tk.Entry( frame_inputs, bg = secondary_color, fg = text_color, font = ( "Courier New", 12 ), relief = "flat", insertbackground = text_color )
entry_amount.grid( row = 0, column = 1, padx = 10, pady = 10 )

# dropdown box
label_currency = tk.Label( frame_inputs, text = "Target Currency:", font = ( "Courier New", 14, "bold" ), bg = main_color, fg = text_color )
label_currency.grid( row = 1, column = 0, padx = 10, pady = 10 )

currency_options = fetch_currency_list()
combo_currency = ttk.Combobox( frame_inputs, values = currency_options, state = "normal", font = ( "Courier New", 12 ) )
combo_currency.grid( row = 1, column = 1, padx = 10, pady = 10 )
combo_currency.current(0)  # defaults to the first currency in the list (AED)

# style for the dropdown
style = ttk.Style()
style.theme_use('clam')
style.configure( "TCombobox", fieldbackground = secondary_color, background = accent_color, foreground = text_color, relief = "flat", padding = 5 )

# convert button
button_convert = tk.Button( root, text = "CONVERT", command = convert_currency, font = ( "Lucida Handwriting", 12 ), bg = accent_color, fg = main_color, relief = "flat", padx = 10, pady = 5 )
button_convert.pack( pady = 20)

# result label
label_result = tk.Label( root, text = "", font = ( "Courier New", 14 ), bg = main_color, fg = text_color )
label_result.pack( pady = 10 )

root.mainloop()
