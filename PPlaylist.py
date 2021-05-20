import sqlite3
import os
import csv
import tkinter as tk
from tkinter import ttk

# initialise tkinter
root = tk.Tk()
root.title("PPlaylist")
root.geometry("700x900")

# Create top frame
top_frame = tk.Frame(master=root, bg="black", height=120)
top_frame.pack(side=tk.TOP, fill=tk.X)

## Create tabs for top frame
tab_control_top = ttk.Notebook(top_frame)
login_tab = ttk.Frame(tab_control_top)
register_tab = ttk.Frame(tab_control_top)
tab_control_top.add(login_tab, text='Login')
tab_control_top.add(register_tab, text='Register')
tab_control_top.pack(side=tk.LEFT)
## Create login section
username_text = tk.Label(master=login_tab, text="Username: ")
username_text.grid(column=0, row=0)
password_text = tk.Label(master=login_tab, text="Password: ")
password_text.grid(column=0, row=1)
username_field = tk.Entry(master=login_tab, width=20)
username_field.grid(column=1, row=0, padx=5)
password_field = tk.Entry(master=login_tab, width=20)
password_field.grid(column=1, row=1)
submit_button = tk.Button(master=login_tab, text="Submit", width=10)
submit_button.grid(column=0, row=2)

# Create bottom frame
bottom_frame = tk.Frame(master=root)
bottom_frame.pack(side=tk.BOTTOM)

# Loop main window
root.mainloop()