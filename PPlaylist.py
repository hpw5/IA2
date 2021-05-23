import sqlite3
import os
import csv
import tkinter as tk
from tkinter import ttk

# initialise tkinter
root = tk.Tk()
root.title("PPlaylist")
root.geometry("1300x900")

# Create tkinter variables
songs_status = tk.StringVar(value="Status: Not loaded!")

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

### Create login section
username_text = tk.Label(master=login_tab, text="Username: ")
username_text.grid(column=0, row=0)
password_text = tk.Label(master=login_tab, text="Password: ")
password_text.grid(column=0, row=1)
username_field = tk.Entry(master=login_tab, width=20)
username_field.grid(column=1, row=0, padx=5)
password_field = tk.Entry(master=login_tab, width=20, show="*")
password_field.grid(column=1, row=1)
submit_button = tk.Button(master=login_tab, text="Submit", width=10)
submit_button.grid(column=0, row=2)

### Create register section
name_text = tk.Label(master=register_tab, width=20, text="Name: ")
name_text.grid(column=0, row=0)
username_text = tk.Label(master=register_tab, text="Username: ")
username_text.grid(column=0, row=1)
password_text = tk.Label(master=register_tab, text="Password: ")
password_text.grid(column=0, row=2)
confirm_password_text = tk.Label(master=register_tab, text="Confirm password: ")
confirm_password_text.grid(column=0, row=3)
register_button = tk.Button(master=register_tab, text="Register", width=10)
register_button.grid(column=0, row=4)
name_field = tk.Entry(master=register_tab)
name_field.grid(column=1, row=0)
username_field = tk.Entry(master=register_tab)
username_field.grid(column=1, row=1)
password_field = tk.Entry(master=register_tab, show="*")
password_field.grid(column=1, row=2)
confirm_password_field = tk.Entry(master=register_tab,show="*")
confirm_password_field.grid(column=1, row=3)

# Create bottom frame
bottom_frame = tk.Frame(master=root)
bottom_frame.pack(side=tk.TOP, anchor=tk.NW)

## Create tabs for bottom frame
tab_control_bottom = ttk.Notebook(bottom_frame)
import_tab = ttk.Frame(tab_control_bottom)
tab_control_bottom.add(import_tab, text='Start')
tab_control_bottom.pack()

### Create welcome text
welcome_text = tk.Label(master=import_tab, text="Welcome. ", font="Helvetica, 35")
welcome_text.pack()
info_text = tk.Label(master=import_tab, text= "Import the spotify catalogues to get started.", font="Helvetica, 20")
info_text.pack()

### Create import buttons
import_songs_frame = tk.Frame(master=import_tab)
import_songs_frame.pack(anchor=tk.W)
blank_1 = tk.Label(master=import_songs_frame)
blank_1.pack()
songs_label = tk.Label(master=import_songs_frame, text="Import the spotify song catalogue.", font="Helvetica, 15")
songs_label.pack(anchor=tk.W)
songs_link = tk.Label(master=import_songs_frame, text = "It can be found at https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks/?select=tracks.csv")
songs_link.pack()
import_songs_button = tk.Button(master=import_songs_frame, text="Import songs")
import_songs_button.pack(anchor=tk.W)
import_songs_status = tk.Label(master=import_songs_frame, textvariable=songs_status, fg="red")
import_songs_status.pack(anchor=tk.W)

# Loop main window
root.mainloop()