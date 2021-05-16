import sqlite3
import os
import csv
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
                            valance NUMERIC,
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
                            artist TEXT,
                            song_id TEXT,
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
                artist_values = artists.replace('"','')
                artist_list.append((artist_values,))
                
                
                # Import Genres
                genres = row[0]
                genre_values_no_bracket = genres.replace('[', '').replace(']', '')
                if genre_values_no_bracket != '':
                    genres = genre_values_no_bracket.split(',')
                    for genre_raw in genres:
                        genre_list.append((genre_raw.strip()[1:-1],))
        #print(genre_list)           

        #print(genre_list)
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
                duartion_values = row[3]
                song_list.append((id_values,name_values,acousticness_values,danceability_values,energy_values,duartion_values))
        sqlmanycommand("INSERT OR IGNORE INTO Songs (id, name, acousticness, danceability, energy, duration_ms) VALUES (?,?,?,?,?,?)",song_list)

## MAIN PROGRAM ##
# Create tables if no exist
if os.path.isfile("catalogue.db") == False:
    create_database()
    print("Created database")
else:
    print("Database already exist")

# import csv files
import_csv("data_by_artist_o.csv")
import_csv("tracks.csv")