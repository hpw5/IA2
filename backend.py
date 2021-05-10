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
        with open(file_name, encoding = "utf8") as csv_file:
            #csv_reader = csv.reader(csv_file, delimiter = ",")
            for line in csv.DictReader(csv_file):
                # Import artists
                artist_values = line["artists"].replace('"','')
                artist_sql = f"""
                    INSERT OR IGNORE INTO Artists
                    VALUES ("{artist_values}")
                    """
                sqlcommand(artist_sql)
                
                # Import Genres
                genre_values_no_left_bracket = line["genres"].replace('[', '')
                genre_values_no_right_bracket = genre_values_no_left_bracket.replace(']', '"')
                if genre_values_no_right_bracket != '"':
                    genre_values_raw = genre_values_no_right_bracket.replace('"', "")
                    genre_list = genre_values_raw.split(', ')
                    genre_list = [i.replace("'", '') for i in genre_list]
                    for i in range(len(genre_list)):
                        genre_values = (genre_list[i])
                        genre_sql = f"""
                            INSERT OR IGNORE INTO Genres
                            VALUES ("{genre_values}")
                            """
                        sqlcommand(genre_sql)
    # Import Songs
    else:
        with open(file_name, encoding = "utf8") as csv_file:
            for line in csv.DictReader(csv_file):
                # Import id
                id_values = line["id"]
                song_sql = f"""
                    INSERT OR IGNORE INTO Songs (id)
                    VALUES ("{id_values}")
                    """
                sqlcommand(song_sql)
                print(song_sql)

## MAIN PROGRAM ##
# Create tables if no exist
if os.path.isfile("catalogue.db") == False:
    create_database()
    print("Created database")
else:
    print("Database already exist")

# import csv files
#import_csv("data_by_artist_o.csv")
import_csv("tracks.csv")