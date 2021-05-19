import sqlite3
import os
import csv
import tkinter as tk

# initialise tkinter
root = tk.Tk()
root.title("PPlaylist")
root.geometry("700x900")

# Create top frame
top_frame = tk.Frame(master=root, bg="black", height=120)
top_frame.pack(side=tk.TOP, fill=tk.X)

## Create login section
username_text = tk.Label(master=top_frame, text="Username: ")
username_text.grid(column=0, row=0)
password_text = tk.Label(master=top_frame, text="Password: ")
password_text.grid(column=0, row=1)
username_field = tk.Entry(master=top_frame, width=20)
username_field.grid(column=1, row=0, padx=5)
password_field = tk.Entry(master=top_frame, width=20)
password_field.grid(column=1, row=1)
submit_button = tk.Button(master=top_frame, text="Submit", width=10)
submit_button.grid(column=0, row=2)
register_button = tk.Button(master=top_frame, text="Register", width=10)
register_button.grid(column=0, row=3)

# Create bottom frame
bottom_frame = tk.Frame(master=root)
bottom_frame.pack(side=tk.BOTTOM)

# Loop main window
root.mainloop()