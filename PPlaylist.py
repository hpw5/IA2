import sqlite3
import os
import csv
import tkinter as tk
PATH = "./"
DB_FILE = PATH + "catalogue.db"

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

# initialise tkinter
root = tk.Tk()
root.title("Database")
root.geometry("400x400")

# Loop main window
root.mainloop()