import sqlite3
import os
import csv
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
import random
import json
PATH = "./"
DB_FILE = PATH + "catalogue.db"

## BACKEND ##
# Run sql command
def sqlcommand(sql_command):
    with sqlite3.connect(DB_FILE) as database:
        cursor = database.cursor()
        cursor.execute(sql_command)
        return cursor.fetchall()

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
                            explicit INTERGER,
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
    try:
        sqlcommand(artists_table)
        sqlcommand(genres_table)
        sqlcommand(artistsgenres_table)
        sqlcommand(songs_table)
        sqlcommand(artistssongs_table)
    except:
        pass

# Put csv values into database
def import_csv(file_name):
    # Create tables if they don't exist
    create_database()
    # Import artists and genres
    if "data_by_artist_o.csv" in file_name:
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
                # import valence values
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
                # import explicit values
                explicit_values = row[4]
                # import mode values
                release_dates = row[7]
                song_list.append((id_values,name_values,acousticness_values,danceability_values,energy_values,duration_values,instrumentals_values,valence_values,popularity_values,tempo_values,liveness_values,loudness_values,speechiness_values,mode_values,key_values,explicit_values,release_dates))
        sqlmanycommand("INSERT OR IGNORE INTO Songs (id, name, acousticness, danceability, energy, duration_ms, instrumentals, valence, popularity, tempo, liveness, loudness, speechiness, mode, key, explicit, release_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",song_list)

# Create linking table
def linking_table(csv_id, file_name):
    # Check which csv is being loaded
    if csv_id == 1:
        # ArtistsGenre table
        artistgenre = []
        with open(file_name, encoding = "utf8") as csv_file:
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
    else:
        artistsong = []
        with open(file_name, encoding = "utf8") as csv_file:
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

# Tkinter functions
# Select and import songs csv file
def import_songs():
    # Checks whether the songs list has been imported or not
    if songs_status.get() == ("Status: Not loaded!"):
        file = tk.filedialog.askopenfilename(filetype=(('CSV files', "tracks.csv"),))
        # Checks if the user actually selected a file or not
        if file != "":
            # Create temp window to let user know that file is importing
            temp = tk.Toplevel(master=root)
            temp.geometry("300x100")
            temp_label_top = tk.Label(master=temp, text="Importing", font="Helvetica, 25")
            temp_label_bot = tk.Label(master=temp, text="Please be patient...", font="Helvetica, 14")
            temp_label_top.pack(expand=1)
            temp_label_bot.pack(expand=1)
            root.update()
            import_csv(file)
            linking_table(0, file)
            messagebox.showinfo("PPlaylist", "Spotify songlist successfully imported.")
            songs_status.set("Status: Loaded!")
            import_songs_status.configure(fg="green")
            # Destroy temp window
            temp.destroy()
            fill_genres()
    else:
        #TODO Let users "reset" the catalogue. (Actually just delete it)
        messagebox.showerror("PPlaylist", "Error: Songlist has already been imported!")

def import_artists():
    # Checks whether the artist list has been imported or not
    if artists_status.get() == ("Status: Not loaded!"):
        file = tk.filedialog.askopenfilename(filetype=(('CSV files', "data_by_artist_o.csv"),))
        # Checks if the user actually selected a file or not
        if file != "":
            # Create temp window to let user know that file is importing
            temp = tk.Toplevel(master=root)
            temp.geometry("300x100")
            temp_label_top = tk.Label(master=temp, text="Importing", font="Helvetica, 25")
            temp_label_bot = tk.Label(master=temp, text="Please be patient...", font="Helvetica, 14")
            temp_label_top.pack(expand=1)
            temp_label_bot.pack(expand=1)
            root.update()
            import_csv(file)
            linking_table(1, file)
            messagebox.showinfo("PPlaylist", "Artist list successfully imported.")
            artists_status.set("Status: Loaded!")
            import_artists_status.configure(fg="green")
            # Destroy temp window
            temp.destroy()
            fill_genres()
    else:
        #TODO Let users "reset" the catalogue. (Actually just delete it)
        messagebox.showerror("PPlaylist", "Error: Artist list has already been imported!")

def fill_genres():
    # Check if both csv files have been imported, then put all genres into the genre dropdown box
    if songs_status.get() == "Status: Loaded!" and artists_status.get() == "Status: Loaded!":
        # Fetch all genres from database
        genres_for_dropdown = sqlcommand("SELECT genre FROM Genres ORDER BY genre ASC")
        # Convert list to string, remove symbols, then turn back into list
        genre_options = str(genres_for_dropdown).replace(",)", "").replace("(", "").replace("',", ",").replace(", '", ", ").replace("['", "").replace("']", "").replace('"', "").split(", ")
        genre_dropdown = ttk.Combobox(master=preferences_table_frame, width=20, textvariable=genre_value)
        genre_dropdown['values'] = genre_options
        genre_dropdown.grid(row=14, column=2)

def generate_playlist():
    # Stop users from trying to create playlist if files aren't imported
    if songs_status.get() != "Status: Loaded!" or artists_status.get() != "Status: Loaded!":
        messagebox.showerror("PPlaylist", "Error: Spotify songlist and/or artist list not loaded!")
        return

    # Stop users from entering an unwanted value for number of songs
    try:
        isinstance(int(num_of_songs_value.get()), (int))
        if int(num_of_songs_value.get()) <=0:
            messagebox.showerror("PPlaylist", "Error: Please specify the number of songs you want")
            return
    except ValueError:
        messagebox.showerror("PPlaylist", "Error: Please specify the number of songs you want")
        return

    # Put genre into query if user selects one
    if genre_value.get() != "Any":
        genre_sql = 'ArtistsGenre.genre = "' + genre_value.get() + '" AND '
    else:
        genre_sql = ""

    # Include explicit songs if user chooses to
    if explicit_check.get() == True:
        explicit_value = 1
    else:
        explicit_value = 0

    # Include explicit songs if user chooses to
    if mode_check.get() == True:
        if mode_value.get() == "Minor":
            mode_sql = 0
        elif mode_value.get() == "Major":
            mode_sql = 1
        else:
            mode_sql = random.randint(0, 1)
    else:
        mode_sql = random.randint(0, 1)

    # Create list to be put into sql query
    sql_preferences = []
    
    # Put values into sql_preferences or randomise if empty
    # Acousticness
    if acousticness_check.get() == True:
        sql_preferences.append("CAST(ABS(songs.acousticness - " + acousticness_value.get() + "*0.01) AS REAL)")
    else:
        sql_preferences.append("CAST(ABS(songs.acousticness - " + str(random.uniform(0, 1)) + "*0.01) AS REAL)")

        ### Since all the other preferences would contain an
        ### AND statement, this needs to be first to start off"""
    
    # Danceability
    if danceability_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.danceability - " + danceability_value.get() + "*0.01) AS REAL)")
    
    # Energy
    if energy_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.energy - " + energy_value.get() + "*0.01) AS REAL)")
    
    # Duration_ms
    if duration_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.duration_ms - " + duration_value.get() + "*1000) AS REAL)")
    
    # Instrumentalness
    if instrumentalness_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.instrumentals - " + instrumentalness_value.get() + "*0.01) AS REAL)")
    
    # Valence
    if valence_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.valence - " + valence_value.get() + "*0.01) AS REAL)")
    
    # Popularity
    if popularity_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.popularity - " + popularity_value.get() + "*0.01) AS REAL)")
    
    # Tempo
    if tempo_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.tempo - " + tempo_value.get() + ") AS REAL)")
    
    # Liveness
    if liveness_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.liveness - " + liveness_value.get() + ") AS REAL)")
    
    # Loudness
    if loudness_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.loudness - " + loudness_value.get() + "*0.01) AS REAL)")
    
    # Speechiness
    if speechiness_check.get() == True:
        sql_preferences.append(" AND CAST(ABS(songs.speechiness - " + speechiness_value.get() + ") AS REAL)")
    
    # Create temp window to let user know that the playlist is being created
    temp = tk.Toplevel(master=root)
    temp.geometry("300x100")
    temp_label_top = tk.Label(master=temp, text="Creating playlist", font="Helvetica, 25")
    temp_label_bot = tk.Label(master=temp, text="Please be patient...", font="Helvetica, 14")
    temp_label_top.pack(expand=1)
    temp_label_bot.pack(expand=1)
    root.update()
    # Turn list into string
    sql_preferences = ''.join(sql_preferences)
    print(sql_preferences)
    query = f"""SELECT DISTINCT songs.id, songs.name, ArtistsSongs.artist
                FROM songs
                JOIN ArtistsSongs ON songs.id = ArtistsSongs.song_id
                JOIN artistsGenre ON ArtistsSongs.artist = artistsGenre.artist
                WHERE {genre_sql}songs.explicit = {explicit_value} AND songs.mode = {mode_sql}
                ORDER BY {sql_preferences}
                ASC
                LIMIT {num_of_songs_value.get()}
            """
    # Query the database and store the result
    global result
    result = sqlcommand(query)

    # Create listboxes to display playlist
    song_result_label = tk.Label(master=result_listbox_frame, text="Song name")
    song_result_label.grid(row=0, column=0)
    song_result_listbox = tk.Listbox(master=result_listbox_frame, width=25, height=28, selectmode=tk.BROWSE)
    song_result_listbox.grid(row=1, column=0)
    artist_result_label = tk.Label(master=result_listbox_frame, text="Artist")
    artist_result_label.grid(row=0, column=1)
    artist_result_listbox = tk.Listbox(master=result_listbox_frame, width=25, height=28, selectmode=tk.BROWSE)
    artist_result_listbox.grid(row=1, column=1)
    for song in ([x[1] for x in result]):
        song_result_listbox.insert(tk.END, song)
    for artist in ([x[2] for x in result]):
        artist_result_listbox.insert(tk.END, artist)
    if export_button_exist.get() == False:
        export_label = tk.Label(master=results_frame, text="If you're happy with this playlist,\nclick the button below to export it.", justify="left")
        export_label.pack(anchor=tk.W,pady=10)
        export_button = tk.Button(master=results_frame, text="Export")
        export_button.pack(anchor=tk.SW)
        export_button_exist.set(True)
    print(query)
    temp.destroy()

def update_entry_state():
    # Acousticness
    if acousticness_check.get() == True:
        acousticness_entry.configure(state='normal')
    else:
        acousticness_entry.configure(state='disabled')
    # Danceability
    if danceability_check.get() == True:
        danceability_entry.configure(state='normal')
    else:
        danceability_entry.configure(state='disabled')
    # Energy
    if energy_check.get() == True:
        energy_entry.configure(state='normal')
    else:
        energy_entry.configure(state='disabled')
    # Duration_ms
    if duration_check.get() == True:
        duration_entry.configure(state='normal')
    else:
        duration_entry.configure(state='disabled')
    # Instrumentalness
    if instrumentalness_check.get() == True:
        instrumentalness_entry.configure(state='normal')
    else:
        instrumentalness_entry.configure(state='disabled')
    # Valence
    if valence_check.get() == True:
        valence_entry.configure(state='normal')
    else:
        valence_entry.configure(state='disabled')
    # Popularity
    if popularity_check.get() == True:
        popularity_entry.configure(state='normal')
    else:
        popularity_entry.configure(state='disabled')
    # Tempo
    if tempo_check.get() == True:
        tempo_entry.configure(state='normal')
    else:
        tempo_entry.configure(state='disabled')
    # Liveness
    if liveness_check.get() == True:
        liveness_entry.configure(state='normal')
    else:
        liveness_entry.configure(state='disabled')
    # Loudness
    if loudness_check.get() == True:
        loudness_entry.configure(state='normal')
    else:
        loudness_entry.configure(state='disabled')
    # Speechiness
    if speechiness_check.get() == True:
        speechiness_entry.configure(state='normal')
    else:
        speechiness_entry.configure(state='disabled')
    # Mode
    if mode_check.get() == True:
        mode_dropdown.configure(state='normal')
    else:
        mode_dropdown.configure(state='disabled')
    # Key
    if key_check.get() == True:
        key_dropdown.configure(state='normal')
    else:
        key_dropdown.configure(state='disabled')

# Save preferences when button is clicked
def save_file():
    savefile = filedialog.asksaveasfile(initialfile="preferences", defaultextension=".json", mode="w")
    preferences = {}
    preferences["preferences"] = []
    preferences["preferences"].append({
        "acousticness": acousticness_value.get(),
        "danceability": danceability_value.get(),
        "energy": energy_value.get(),
        "duration": duration_value.get(),
        "instrumentalness": instrumentalness_value.get(),
        "valence": valence_value.get(),
        "popularity": popularity_value.get(),
        "tempo": tempo_value.get(),
        "liveness": liveness_value.get(),
        "loudness": loudness_value.get(),
        "speechiness": speechiness_value.get(),
        "mode": mode_value.get(),
        "key": key_value.get(),
        "genre": genre_value.get(),
        "num_of_songs": num_of_songs_value.get()
    })
    json.dump(preferences, savefile)

# Load preferences when button is clicked
def load_file():
    # Prevent user from trying to load invaild files
    try:
        loadfile = filedialog.askopenfile()
        preferences = json.load(loadfile)
        for value in preferences["preferences"]:
            acousticness_value.set(value["acousticness"])
            danceability_value.set(value["danceability"])
            energy_value.set(value["energy"])
            duration_value.set(value["duration"])
            instrumentalness_value.set(value["instrumentalness"])
            valence_value.set(value["valence"])
            popularity_value.set(value["popularity"])
            tempo_value.set(value["tempo"])
            liveness_value.set(value["liveness"])
            loudness_value.set(value["loudness"])
            speechiness_value.set(value["speechiness"])
            mode_value.set(value["mode"])
            key_value.set(value["key"])
            genre_value.set(value["genre"])
            num_of_songs_value.set(value["num_of_songs"])
    except:
            messagebox.showerror("PPlaylist", "Error: Cannot load audio features. Is it the right file?")
            
# Create tkinter variables
songs_status = tk.StringVar(value="Status: Not loaded!")
artists_status = tk.StringVar(value="Status: Not loaded!")
acousticness_value = tk.StringVar()
acousticness_check = tk.BooleanVar()
danceability_value = tk.StringVar()
danceability_check = tk.BooleanVar()
energy_value = tk.StringVar()
energy_check = tk.BooleanVar()
duration_value = tk.StringVar()
duration_check = tk.BooleanVar()
instrumentalness_value = tk.StringVar()
instrumentalness_check = tk.BooleanVar()
valence_value = tk.StringVar()
valence_check = tk.BooleanVar()
popularity_value = tk.StringVar()
popularity_check = tk.BooleanVar()
tempo_value = tk.StringVar()
tempo_check = tk.BooleanVar()
liveness_value = tk.StringVar()
liveness_check = tk.BooleanVar()
loudness_value = tk.StringVar()
loudness_check = tk.BooleanVar()
speechiness_value = tk.StringVar()
speechiness_check = tk.BooleanVar()
mode_value = tk.StringVar(value="-")
mode_check = tk.BooleanVar()
key_value = tk.StringVar(value="-")
key_check = tk.BooleanVar()
genre_value = tk.StringVar(value="Any")
num_of_songs_value = tk.StringVar()
explicit_check = tk.BooleanVar()
features_saved = tk.StringVar()
export_button_exist = tk.BooleanVar()

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
import_songs_button = tk.Button(master=import_songs_frame, text="Import songs", command=import_songs)
import_songs_button.pack(anchor=tk.W)
import_songs_status = tk.Label(master=import_songs_frame, textvariable=songs_status, fg="red")
import_songs_status.pack(anchor=tk.W)

import_artists_frame = tk.Frame(master=import_tab)
import_artists_frame.pack(anchor=tk.W, padx=15)
blank_2 = tk.Label(master=import_artists_frame)
blank_2.pack()
artists_label = tk.Label(master=import_artists_frame, text="Import the spotify artist catalogue.", font="Helvetica, 15")
artists_label.pack(anchor=tk.W)
artists_link = tk.Label(master=import_artists_frame, text = "It can be found at https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks/?select=data_by_artist_o.csv")
artists_link.pack()
import_artists_button = tk.Button(master=import_artists_frame, text="Import artists", command=import_artists)
import_artists_button.pack(anchor=tk.W)
import_artists_status = tk.Label(master=import_artists_frame, textvariable=artists_status, fg="red")
import_artists_status.pack(anchor=tk.W)

# Create preferences side
preferences_frame = tk.Frame(master=create_playlist_tab)
preferences_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=15)
create_preferences_label = tk.Label(master=preferences_frame, text="Create playlist", font="Helvetica, 35")
create_preferences_label.pack()
preferences_guide_label = tk.Label(master=preferences_frame, text="Fill out the fields with what audio features you want your\nmusic to have.", font="Helvetica, 15", justify="left")
preferences_guide_label.pack()

# Create preferences table
preferences_table_frame = tk.Frame(master=preferences_frame)
preferences_table_frame.pack(anchor=tk.W)
audio_feature_label = tk.Label(master=preferences_table_frame, text="Audio Feature")
audio_feature_label.grid(row=0, column=1)
audio_feature_value_label = tk.Label(master=preferences_table_frame, text="Value")
audio_feature_value_label.grid(row=0, column=2)
# Acousticness
acousticness_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=acousticness_check, command=update_entry_state)
acousticness_checkbox.grid(row=1, column=0)
acousticness_label = tk.Label(master=preferences_table_frame, text="Acousticness")
acousticness_label.grid(row=1, column=1)
acousticness_entry = tk.Entry(master=preferences_table_frame, textvariable=acousticness_value, state="disabled")
acousticness_entry.grid(row=1, column=2)
acousticness_example = tk.Label(master=preferences_table_frame, text="0-100")
acousticness_example.grid(row=1, column=3)
# Danceability
danceability_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=danceability_check, command=update_entry_state)
danceability_checkbox.grid(row=2, column=0)
danceability_label = tk.Label(master=preferences_table_frame, text="Danceability")
danceability_label.grid(row=2, column=1)
danceability_entry = tk.Entry(master=preferences_table_frame, textvariable=danceability_value, state="disabled")
danceability_entry.grid(row=2, column=2)
danceability_example = tk.Label(master=preferences_table_frame, text="0-100")
danceability_example.grid(row=2, column=3)
# Energy
energy_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=energy_check, command=update_entry_state)
energy_checkbox.grid(row=3, column=0)
energy_label = tk.Label(master=preferences_table_frame, text="Energy")
energy_label.grid(row=3, column=1)
energy_entry = tk.Entry(master=preferences_table_frame, textvariable=energy_value, state="disabled")
energy_entry.grid(row=3, column=2)
energy_example = tk.Label(master=preferences_table_frame, text="0-100")
energy_example.grid(row=3, column=3)
# Duration_ms
duration_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=duration_check, command=update_entry_state)
duration_checkbox.grid(row=4, column=0)
duration_label = tk.Label(master=preferences_table_frame, text="Duration in seconds")
duration_label.grid(row=4, column=1)
duration_entry = tk.Entry(master=preferences_table_frame, textvariable=duration_value, state="disabled")
duration_entry.grid(row=4, column=2)
duration_example = tk.Label(master=preferences_table_frame, text="")
# Instrumentalness
instrumentalness_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=instrumentalness_check, command=update_entry_state)
instrumentalness_checkbox.grid(row=5, column=0)
instrumentalness_label = tk.Label(master=preferences_table_frame, text="Instrumentalness")
instrumentalness_label.grid(row=5, column=1)
instrumentalness_entry = tk.Entry(master=preferences_table_frame, textvariable=instrumentalness_value, state="disabled")
instrumentalness_entry.grid(row=5, column=2)
instrumentalness_example = tk.Label(master=preferences_table_frame, text="0-100")
instrumentalness_example.grid(row=5, column=3)
# Valence
valence_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=valence_check, command=update_entry_state)
valence_checkbox.grid(row=6, column=0)
valence_label = tk.Label(master=preferences_table_frame, text="Valence (Happiness)")
valence_label.grid(row=6, column=1)
valence_entry = tk.Entry(master=preferences_table_frame, textvariable=valence_value, state="disabled")
valence_entry.grid(row=6, column=2)
valence_example = tk.Label(master=preferences_table_frame, text="0-100")
valence_example.grid(row=6, column=3)
# Popularity
popularity_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=popularity_check, command=update_entry_state)
popularity_checkbox.grid(row=7, column=0)
popularity_label = tk.Label(master=preferences_table_frame, text="Popularity")
popularity_label.grid(row=7, column=1)
popularity_entry = tk.Entry(master=preferences_table_frame, textvariable=popularity_value, state="disabled")
popularity_entry.grid(row=7, column=2)
popularity_example = tk.Label(master=preferences_table_frame, text="0-100")
popularity_example.grid(row=7, column=3)
# Tempo
tempo_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=tempo_check, command=update_entry_state)
tempo_checkbox.grid(row=8, column=0)
tempo_label = tk.Label(master=preferences_table_frame, text="Speed (tempo)")
tempo_label.grid(row=8, column=1)
tempo_entry = tk.Entry(master=preferences_table_frame, textvariable=tempo_value, state="disabled")
tempo_entry.grid(row=8, column=2)
# Liveness
liveness_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=liveness_check, command=update_entry_state)
liveness_checkbox.grid(row=9, column=0)
liveness_label = tk.Label(master=preferences_table_frame, text="Audience background\nnoise")
liveness_label.grid(row=9, column=1)
liveness_entry = tk.Entry(master=preferences_table_frame, textvariable=liveness_value, state="disabled")
liveness_entry.grid(row=9, column=2)
liveness_example = tk.Label(master=preferences_table_frame, text="0-100")
liveness_example.grid(row=9, column=3)
# Loudness
loudness_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=loudness_check, command=update_entry_state)
loudness_checkbox.grid(row=10, column=0)
loudness_label = tk.Label(master=preferences_table_frame, text="Loudness")
loudness_label.grid(row=10, column=1)
loudness_entry = tk.Entry(master=preferences_table_frame, textvariable=loudness_value, state="disabled")
loudness_entry.grid(row=10, column=2)
loudness_example = tk.Label(master=preferences_table_frame, text="0-100")
loudness_example.grid(row=10, column=3)
# Speechiness
speechiness_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=speechiness_check, command=update_entry_state)
speechiness_checkbox.grid(row=11, column=0)
speechiness_label = tk.Label(master=preferences_table_frame, text="Speechiness")
speechiness_label.grid(row=11, column=1)
speechiness_entry = tk.Entry(master=preferences_table_frame, textvariable=speechiness_value, state="disabled")
speechiness_entry.grid(row=11, column=2)
speechiness_example = tk.Label(master=preferences_table_frame, text="0-100")
speechiness_example.grid(row=11, column=3)
# Mode
mode_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=mode_check, command=update_entry_state)
mode_checkbox.grid(row=12, column=0)
mode_label = tk.Label(master=preferences_table_frame, text="Mode")
mode_label.grid(row=12, column=1)
mode_options = ["Major", "Minor"]
mode_dropdown = ttk.Combobox(master=preferences_table_frame, width=20, textvariable=mode_value, state="disabled")
mode_dropdown['values'] = mode_options
mode_dropdown.grid(row=12, column=2)
# Key
key_checkbox = tk.Checkbutton(master=preferences_table_frame, variable=key_check, command=update_entry_state)
key_checkbox.grid(row=13, column=0)
key_label = tk.Label(master=preferences_table_frame, text="Key")
key_label.grid(row=13, column=1)
key_options = ["C", "C#", "D", "D#", "E", "E#", "F", "F#", "G", "G#", "A", "A#", "B"]
key_dropdown = ttk.Combobox(master=preferences_table_frame, width=20, textvariable=key_value, state="disabled")
key_dropdown['values'] = key_options
key_dropdown.grid(row=13, column=2)
# Genre
genre_label = tk.Label(master=preferences_table_frame, text="Genre")
genre_label.grid(row=14, column=1)
genre_options = ["-"]
genre_dropdown = ttk.Combobox(master=preferences_table_frame, width=20, textvariable=genre_value)
genre_dropdown['values'] = genre_options
genre_dropdown.grid(row=14, column=2)
# Number of songs
num_of_songs_label = tk.Label(master=preferences_table_frame, text="Number of songs")
num_of_songs_label.grid(row=15, column=1)
num_of_songs_entry = tk.Entry(master=preferences_table_frame, textvariable=num_of_songs_value)
num_of_songs_entry.grid(row=15, column=2)
num_of_songs_required_label = tk.Label(master=preferences_table_frame, text="REQUIRED", fg="red")
num_of_songs_required_label.grid(row=15, column=3)

# Pre-set audio features button
pre_set_audio_features_frame = tk.Frame(master=preferences_frame)
pre_set_audio_features_frame.pack(anchor=tk.W)
save_features_label = tk.Button(master=pre_set_audio_features_frame, text="Save audio features", command=save_file)
save_features_label.grid(row=0, column=0)
load_features_label = tk.Button(master=pre_set_audio_features_frame, text="Load audio features", command=load_file)
load_features_label.grid(row=0, column=1, padx=15, pady=10)
features_saved_label = tk.Label(master=preferences_frame, textvariable=features_saved, fg="green")
features_saved_label.pack(anchor=tk.W)

# explicit button
explicit_frame = tk.Frame(master=preferences_frame)
explicit_frame.pack(anchor=tk.W)
explicit_checkbox = tk.Checkbutton(master=explicit_frame, variable=explicit_check)
explicit_checkbox.grid(row=0, column=0)
explicit_label = tk.Label(master=explicit_frame, text="Include explicit songs")
explicit_label.grid(row=0, column=1)

# Create generate button
generate_frame = tk.Frame(master=preferences_frame)
generate_frame.pack(anchor=tk.W)
generate_label = tk.Label(master=generate_frame, text="Once the above table has the desired song values,\nclick the button below to create a unique playlist.")
generate_label.pack()
generate_button = tk.Button(master=generate_frame, text="Create playlist!", command=generate_playlist)
generate_button.pack(anchor=tk.W)

# Create results frame
results_frame = tk.Frame(master=create_playlist_tab)
results_frame.pack(side=tk.RIGHT, padx=15, anchor=tk.N)
results_label = tk.Label(master=results_frame, text="Your playlist", font="Helvetica, 35")
results_label.pack()
results_guide_label = tk.Label(master=results_frame, text="After filling in the table on the left, your playlist\nwill be automatically made and displayed below.", font="Helvetica, 15", justify="left")
results_guide_label.pack()

# Create frame to list results
result_listbox_frame = tk.Frame(master=results_frame)
result_listbox_frame.pack()

# Inital checks
# Check if files are imported
try:
    # Songs
    count = str(sqlcommand("SELECT COUNT(id) FROM Songs"))
    if int(count.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "")) >= 1:
        songs_status.set("Status: Loaded!")
        import_songs_status.configure(fg="green")
    # Artists
    count = str(sqlcommand("SELECT COUNT(artist) FROM Artists"))
    if int(count.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "")) >= 1:
        artists_status.set("Status: Loaded!")
        import_artists_status.configure(fg="green")
except:
    pass

fill_genres()

# Loop main window
root.mainloop()