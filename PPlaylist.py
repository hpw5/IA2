import sqlite3
import os
import csv
import tkinter as tk

# initialise tkinter
root = tk.Tk()
root.title("PPlaylist")
root.geometry("700x900")

# Create top frame
sign_in_frame = tk.Frame(root, bg="black", height=120)
sign_in_frame.pack(side=tk.TOP, fill=tk.X)

# Create bottom frame
welcome_frame = tk.Frame(root)
welcome_frame.pack(side=tk.BOTTOM)

# Loop main window
root.mainloop()