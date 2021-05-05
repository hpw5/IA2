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
                            name TEXT NOT NULL,
                            acousticness NUMERIC NOT NULL,
                            danceability NUMERIC NOT NULL,
                            energy NUMERIC NOT NULL,
                            duration_ms NUMERIC NOT NULL,
                            instrumentals NUMERIC NOT NULL,
                            valance NUMERIC NOT NULL,
                            popularity NUMERIC NOT NULL,
                            tempo NUMERIC NOT NULL,
                            liveness NUMERIC NOT NULL,
                            loudness NUMERIC NOT NULL,
                            speechiness NUMERIC NOT NULL,
                            mode INTEGER NOT NULL,
                            key INTEGER NOT NULL,
                            explict INTERGER NOT NULL,
                            release_date TEXT NOT NULL
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
    with open(file_name, encoding = "utf8") as csv_file:
        #csv_reader = csv.reader(csv_file, delimiter = ",")
        for line in csv.DictReader(csv_file):
            artists_dict = line
            values = artists_dict["artists"].replace('"','')
            sql = f"""
                INSERT INTO Artists
                VALUES ("{values}")
                """
            sqlcommand(sql)

## MAIN PROGRAM ##
# Create tables if no exist
if os.path.isfile("catalogue.db") == False:
    create_database()
    print("Created database")
else:
    print("Database already exist")

# import csv files
import_csv("data_by_artist_o.csv")