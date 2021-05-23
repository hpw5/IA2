import sqlite3
import os
import csv
import tkinter as tk
from tkinter import ttk
PATH = "./"
DB_FILE = PATH + "catalogue.db"

## BACKEND ##
# Run sql command
def sqlcommand(sql_command):
    with sqlite3.connect(DB_FILE) as database:
        cursor = database.cursor()
        cursor.execute(sql_command)

# Run sql many command
def sqlmanycommand(sql_command,values):
    with sqlite3.connect(DB_FILE) as database:
        cursor = database.cursor()
        cursor.executemany(sql_command,values)

# Create tables
def create_database():
    artists_table = """
                        CREATE TABLE Artists (
                            artist TEXT PRIMARY KEY
                        );
                        """
    genres_table = """
                        CREATE TABLE Genres (
                            genre TEXT PRIMARY KEY
                        );
                        """
    artistsgenres_table = """
                        CREATE TABLE ArtistsGenre (
                            artist TEXT,
                            genre TEXT,
                            FOREIGN KEY (artist)
                                REFERENCES Artists (artist),
                            FOREIGN KEY (genre)
                                REFERENCES Artists (genre),
                            PRIMARY KEY(artist,genre)
                        );
                        """
    songs_table = """
                        CREATE TABLE Songs (
                            id TEXT PRIMARY KEY,
                            name TEXT,
                            acousticness NUMERIC,
                            danceability NUMERIC,
                            energy NUMERIC,
                            duration_ms NUMERIC,
                            instrumentals NUMERIC,
                            valence NUMERIC,
                            popularity NUMERIC,
                            tempo NUMERIC,
                            liveness NUMERIC,
                            loudness NUMERIC,
                            speechiness NUMERIC,
                            mode INTEGER,
                            key INTEGER,
                            explict INTERGER,
                            release_date TEXT
                        );
                        """
    artistssongs_table = """
                        CREATE TABLE ArtistsSongs (
                            song_id TEXT,
                            artist TEXT,
                            FOREIGN KEY (artist)
                                REFERENCES Artists (artist),
                            FOREIGN KEY (song_id)
                                REFERENCES Songs (id),
                            PRIMARY KEY (artist,song_id)
                        );
                        """
    sqlcommand(artists_table)
    sqlcommand(genres_table)
    sqlcommand(artistsgenres_table)
    sqlcommand(songs_table)
    sqlcommand(artistssongs_table)

# Put csv values into database
def import_csv(file_name):
    # Import artists and genres
    if file_name == "data_by_artist_o.csv":
        artist_list = []
        genre_list = []
        # Open artist and genre csv file
        with open(file_name, encoding = "utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ",")
            next(csv_reader)
            for row in csv_reader:
                # Import artists
                artists = row[1]
                artists = artists.replace('"','')
                artist_list.append((artists,))
                
                
                # Import Genres
                genres = row[0]
                genres = genres.replace('[', '').replace(']', '')
                if genres != '':
                    genres = genres.split(',')
                    for genre_raw in genres:
                        genre_list.append((genre_raw.strip()[1:-1],))
                        
        sqlmanycommand("INSERT OR IGNORE INTO Artists VALUES (?)",artist_list)
        sqlmanycommand("INSERT OR IGNORE INTO Genres VALUES (?)",genre_list)
    # Import Songs
    else:
        song_list = []
        # Open tracks file
        with open(file_name, encoding = "utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ",")
            next(csv_reader)
            for row in csv_reader:
                # Import id
                id_values = row[0]
                # import names
                name_values = row[1]
                # import acousticness values
                acousticness_values = row[14]
                # import danceability values
                danceability_values = row[8]
                # import energy values
                energy_values = row[9]
                # import duration values
                duration_values = row[3]
                # import instrumentals values
                instrumentals_values = row[15]
                # import valance values
                valence_values = row[17]
                # import popularity values
                popularity_values = row[2]
                # import tempo values
                tempo_values = row[18]
                # import liveness values
                liveness_values = row[16]
                # import loudness values
                loudness_values = row[11]
                # import speechiness values
                speechiness_values = row[13]
                # import mode values
                mode_values = row[12]
                # import key values
                key_values = row[10]
                # import explict values
                explict_values = row[4]
                # import mode values
                release_dates = row[7]
                song_list.append((id_values,name_values,acousticness_values,danceability_values,energy_values,duration_values,instrumentals_values,valence_values,popularity_values,tempo_values,liveness_values,loudness_values,speechiness_values,mode_values,key_values,explict_values,release_dates))
        sqlmanycommand("INSERT OR IGNORE INTO Songs (id, name, acousticness, danceability, energy, duration_ms, instrumentals, valence, popularity, tempo, liveness, loudness, speechiness, mode, key, explict, release_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",song_list)

# Create linking table
def linking_table():
    # ArtistsGenre table
    artistgenre = []
    with open("data_by_artist_o.csv", encoding = "utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        next(csv_reader)
        for row in csv_reader:
            # Artists
            artists = row[1]
            artists = artists.replace('"','')
            
            # Genres
            genres = row[0]
            genres = genres.replace('[', '').replace(']', '')
            if genres != '':
                genres = genres.split(',')
                for genre_raw in genres:
                    genre_raw = genre_raw.strip().replace("'","")
                    artistgenre.append((artists,genre_raw))
        # Put list into database
        sqlmanycommand("INSERT OR IGNORE INTO ArtistsGenre VALUES (?,?)",artistgenre)
    # ArtistsSongs table
    artistsong = []
    with open("tracks.csv", encoding = "utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        next(csv_reader)
        for row in csv_reader:
            # Song_id
            id_values = row[0]

            # artist
            artists = row[5]
            artists = artists.replace('[', '').replace(']', '').split(',')
            for artist_raw in artists:
                artist_raw = artist_raw.strip().replace("'","")
                artistsong.append((id_values,artist_raw))
        # Put list into database
        sqlmanycommand("INSERT OR IGNORE INTO ArtistsSongs VALUES (?,?)",artistsong)

## GUI ##
# initialise tkinter
root = tk.Tk()
root.title("PPlaylist")
root.geometry("1300x900")

# Create tkinter variables
songs_status = tk.StringVar(value="Status: Not loaded!")
mode_selection = tk.StringVar(value="-")
key_selection = tk.StringVar(value="-")
genre_selection = tk.StringVar(value="-")
features_saved = tk.StringVar()

# Create top frame
top_frame = tk.Frame(master=root, bg="black", height=120)
top_frame.pack(side=tk.TOP, fill=tk.X)

# Create tabs for top frame
tab_control_top = ttk.Notebook(top_frame)
login_tab = ttk.Frame(tab_control_top)
register_tab = ttk.Frame(tab_control_top)
tab_control_top.add(login_tab, text='Login')
tab_control_top.add(register_tab, text='Register')
tab_control_top.pack(side=tk.LEFT)

# Create login section
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

# Create register section
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

# Create tabs for bottom frame
tab_control_bottom = ttk.Notebook(bottom_frame)
import_tab = ttk.Frame(tab_control_bottom)
create_playlist_tab = ttk.Frame(tab_control_bottom)
tab_control_bottom.add(import_tab, text='Start')
tab_control_bottom.add(create_playlist_tab, text="Create playlist")
tab_control_bottom.pack()

# Create welcome text
welcome_text = tk.Label(master=import_tab, text="Welcome. ", font="Helvetica, 35")
welcome_text.pack()
info_text = tk.Label(master=import_tab, text= "Import the spotify catalogues to get started.", font="Helvetica, 20")
info_text.pack()

# Create import buttons
import_songs_frame = tk.Frame(master=import_tab)
import_songs_frame.pack(anchor=tk.W, padx=15)
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

import_artists_frame = tk.Frame(master=import_tab)
import_artists_frame.pack(anchor=tk.W, padx=15)
blank_1 = tk.Label(master=import_artists_frame)
blank_1.pack()
artists_label = tk.Label(master=import_artists_frame, text="Import the spotify artist catalogue.", font="Helvetica, 15")
artists_label.pack(anchor=tk.W)
artists_link = tk.Label(master=import_artists_frame, text = "It can be found at https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks/?select=data_by_artist_o.csv")
artists_link.pack()
import_artists_button = tk.Button(master=import_artists_frame, text="Import artists")
import_artists_button.pack(anchor=tk.W)
import_artists_status = tk.Label(master=import_artists_frame, textvariable=songs_status, fg="red")
import_artists_status.pack(anchor=tk.W)

# Create prefrences side
prefrences_frame = tk.Frame(master=create_playlist_tab)
prefrences_frame.pack(side=tk.LEFT,anchor=tk.NW, padx=15)
create_prefrences_label = tk.Label(master=prefrences_frame, text="Create playlist", font="Helvetica, 35")
create_prefrences_label.pack()
prefrences_guide_label = tk.Label(master=prefrences_frame, text="Fill out the fields with what audio features you want your music to have.", font="Helvetica, 15")
prefrences_guide_label.pack()

# Create prefrences table
prefrences_table_frame = tk.Frame(master=prefrences_frame)
prefrences_table_frame.pack(anchor=tk.W)
audio_feature_label = tk.Label(master=prefrences_table_frame, text="Audio Feature")
audio_feature_label.grid(row=0, column=1)
audio_feature_value_label = tk.Label(master=prefrences_table_frame, text="Value")
audio_feature_value_label.grid(row=0, column=2)
# Acousticness
acousticness_checkbox = tk.Checkbutton(master=prefrences_table_frame)
acousticness_checkbox.grid(row=1, column=0)
acousticness_label = tk.Label(master=prefrences_table_frame, text="Acousticness")
acousticness_label.grid(row=1, column=1)
acousticness_entry = tk.Entry(master=prefrences_table_frame)
acousticness_entry.grid(row=1, column=2)
acousticness_example = tk.Label(master=prefrences_table_frame, text="0-100")
acousticness_example.grid(row=1, column=3)
# Danceability
danceability_checkbox = tk.Checkbutton(master=prefrences_table_frame)
danceability_checkbox.grid(row=2, column=0)
danceability_label = tk.Label(master=prefrences_table_frame, text="Danceability")
danceability_label.grid(row=2, column=1)
danceability_entry = tk.Entry(master=prefrences_table_frame)
danceability_entry.grid(row=2, column=2)
danceability_example = tk.Label(master=prefrences_table_frame, text="0-100")
danceability_example.grid(row=2, column=3)
# Energy
energy_checkbox = tk.Checkbutton(master=prefrences_table_frame)
energy_checkbox.grid(row=3, column=0)
energy_label = tk.Label(master=prefrences_table_frame, text="Energy")
energy_label.grid(row=3, column=1)
energy_entry = tk.Entry(master=prefrences_table_frame)
energy_entry.grid(row=3, column=2)
energy_example = tk.Label(master=prefrences_table_frame, text="0-100")
energy_example.grid(row=3, column=3)
# Duration_ms
duration_checkbox = tk.Checkbutton(master=prefrences_table_frame)
duration_checkbox.grid(row=4, column=0)
duration_label = tk.Label(master=prefrences_table_frame, text="Duration in seconds")
duration_label.grid(row=4, column=1)
duration_entry = tk.Entry(master=prefrences_table_frame)
duration_entry.grid(row=4, column=2)
duration_example = tk.Label(master=prefrences_table_frame, text="")
# Instrumentalness
intrumentalness_checkbox = tk.Checkbutton(master=prefrences_table_frame)
intrumentalness_checkbox.grid(row=5, column=0)
intrumentalness_label = tk.Label(master=prefrences_table_frame, text="Instrumentalness")
intrumentalness_label.grid(row=5, column=1)
intrumentalness_entry = tk.Entry(master=prefrences_table_frame)
intrumentalness_entry.grid(row=5, column=2)
intrumentalness_example = tk.Label(master=prefrences_table_frame, text="0-100")
intrumentalness_example.grid(row=5, column=3)
# Valance
valance_checkbox = tk.Checkbutton(master=prefrences_table_frame)
valance_checkbox.grid(row=6, column=0)
valance_label = tk.Label(master=prefrences_table_frame, text="Valance (Happiness)")
valance_label.grid(row=6, column=1)
valance_entry = tk.Entry(master=prefrences_table_frame)
valance_entry.grid(row=6, column=2)
valance_example = tk.Label(master=prefrences_table_frame, text="0-100")
valance_example.grid(row=6, column=3)
# Popularity
popularity_checkbox = tk.Checkbutton(master=prefrences_table_frame)
popularity_checkbox.grid(row=7, column=0)
popularity_label = tk.Label(master=prefrences_table_frame, text="Popularity")
popularity_label.grid(row=7, column=1)
popularity_entry = tk.Entry(master=prefrences_table_frame)
popularity_entry.grid(row=7, column=2)
popularity_example = tk.Label(master=prefrences_table_frame, text="0-100")
popularity_example.grid(row=7, column=3)
# Tempo
tempo_checkbox = tk.Checkbutton(master=prefrences_table_frame)
tempo_checkbox.grid(row=8, column=0)
tempo_label = tk.Label(master=prefrences_table_frame, text="Speed (tempo)")
tempo_label.grid(row=8, column=1)
tempo_entry = tk.Entry(master=prefrences_table_frame)
tempo_entry.grid(row=8, column=2)
# Loudness
loudness_checkbox = tk.Checkbutton(master=prefrences_table_frame)
loudness_checkbox.grid(row=9, column=0)
loudness_label = tk.Label(master=prefrences_table_frame, text="Loudness")
loudness_label.grid(row=9, column=1)
loudness_entry = tk.Entry(master=prefrences_table_frame)
loudness_entry.grid(row=9, column=2)
loudness_example = tk.Label(master=prefrences_table_frame, text="0-100")
loudness_example.grid(row=9, column=3)
# Speechiness
speechiness_checkbox = tk.Checkbutton(master=prefrences_table_frame)
speechiness_checkbox.grid(row=10, column=0)
speechiness_label = tk.Label(master=prefrences_table_frame, text="Speechiness")
speechiness_label.grid(row=10, column=1)
speechiness_entry = tk.Entry(master=prefrences_table_frame)
speechiness_entry.grid(row=10, column=2)
speechiness_example = tk.Label(master=prefrences_table_frame, text="0-100")
speechiness_example.grid(row=10, column=3)
# Mode
mode_checkbox = tk.Checkbutton(master=prefrences_table_frame)
mode_checkbox.grid(row=11, column=0)
mode_label = tk.Label(master=prefrences_table_frame, text="Mode")
mode_label.grid(row=11, column=1)
mode_options = ["Major", "Minor"]
mode_dropdown = tk.OptionMenu(prefrences_table_frame, mode_selection, *mode_options)
mode_dropdown.grid(row=11, column=2)
# Key
key_checkbox = tk.Checkbutton(master=prefrences_table_frame)
key_checkbox.grid(row=12, column=0)
key_label = tk.Label(master=prefrences_table_frame, text="Key")
key_label.grid(row=12, column=1)
key_options = ["C", "C#", "D", "D#", "E", "E#", "F", "F#", "G", "G#", "A", "A#", "B"]
key_dropdown = tk.OptionMenu(prefrences_table_frame, key_selection, *key_options)
key_dropdown.grid(row=12, column=2)
# Genre
#TODO Put genres into dropdown
genre_checkbox = tk.Checkbutton(master=prefrences_table_frame)
genre_checkbox.grid(row=13, column=0)
genre_label = tk.Label(master=prefrences_table_frame, text="Genre")
genre_label.grid(row=13, column=1)
genre_options = ["Placeholder"]
genre_dropdown = tk.OptionMenu(prefrences_table_frame, genre_selection, *genre_options)
genre_dropdown.grid(row=13, column=2)
# Number of songs
num_of_songs_checkbox = tk.Checkbutton(master=prefrences_table_frame)
num_of_songs_checkbox.grid(row=14, column=0)
num_of_songs_label = tk.Label(master=prefrences_table_frame, text="Number of songs")
num_of_songs_label.grid(row=14, column=1)
num_of_songs_entry = tk.Entry(master=prefrences_table_frame)
num_of_songs_entry.grid(row=14, column=2)

# Pre-set audio features button
pre_set_audio_features_frame = tk.Frame(master=prefrences_frame)
pre_set_audio_features_frame.pack(anchor=tk.W)
save_features_label = tk.Button(master=pre_set_audio_features_frame, text="Save audio features")
save_features_label.grid(row=0, column=0)
load_features_label = tk.Button(master=pre_set_audio_features_frame, text="Load audio features")
load_features_label.grid(row=0, column=1, padx=15, pady=10)
features_saved_label = tk.Label(master=prefrences_frame, textvariable=features_saved, fg="green")
features_saved_label.pack(anchor=tk.W)

# Explict button
explict_frame = tk.Frame(master=prefrences_frame)
explict_frame.pack(anchor=tk.W)
explict_checkbox = tk.Checkbutton(master=explict_frame)
explict_checkbox.grid(row=0, column=0)
explict_label = tk.Label(master=explict_frame, text="Include explict songs")
explict_label.grid(row=0, column=1)

# Loop main window
root.mainloop()