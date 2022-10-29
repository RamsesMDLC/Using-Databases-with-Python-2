# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 21:10:52 2020

@author: USUARIO
"""

#PART 1.1: I wil use "ElemenyTree" because I need to parse XML text.
import xml.etree.ElementTree as ET

#PART 1.2: Import the library of SQL lite Browser
import sqlite3

#PART 2: Making the connection between the Python File and...
#...the SQL Database. 
#The "Week3_Test1.sqlite" is the name of the SQL DataBase
conn = sqlite3.connect("Week3_Test1.sqlite")

#PART 3: This code allow me to handle the transmission of... 
#...information. Specificalley, it Open and Send SQL...
#...Commands  through the Cursor and then we get resopnse...
#...through the same Cursor.
cur = conn.cursor()

#PART 4.1: This code juste check if alredy exists any Table...
#... in SQLite3, called "Artist", "Album", "Track" and "Genre"...
#...and if exist, it will be deleted. This is eith the code "DROP TABLE"

#PART 4.2: This code create Tables in SQLite3 called...
#..."Artist", "Album", "Track" and "Genre" with the code "CREATE TABLE".
#It will also establish the "id", "name", "title" and "len" of...
#...every object per Table.
# Also Make some fresh tables using "executescript()"

cur.executescript("""
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);


CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
""")

#PART 5: In this part, the Python File will prompt for the...
#...the name of File in format XML
fname = input("Enter file name: ")

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found: return child.text
        if child.tag == "key" and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall("dict/dict/dict")
print("Dict count:", len(all))

#PART: In this part we will apply a Loop through every line...
#... of the file to find the "Artist", "Album", "Play Count" and "Genre"...
#..., "Name", "Total Time" and "Rating".
for entry in all:
    if ( lookup(entry, "Track ID") is None ): continue

    name = lookup(entry, "Name")
    artist = lookup(entry, "Artist")
    genre = lookup(entry, "Genre")
    album = lookup(entry, "Album")
    count = lookup(entry, "Play Count")
    rating = lookup(entry, "Rating")
    length = lookup(entry, "Total Time")

    if name is None or artist is None or genre is None or album is None: 
        continue

    print(name, artist, genre, album, count, rating, length)

#PART: In this part we will select every piece of data that we found...
# in the File in format XML through the Python Code and then...
#...introduce them in the SQL Database. Specifically, this...
#...code is opening the record set in the SQL Database
#PART 8.2: Also it is important to say that the "question mark?" in the...
#...code is too avoid "SQL Injection"
#PART 8.3: (artist, 1) is a Tuple, as happen with others.
    cur.execute("""INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )""", (artist, ) )
    cur.execute("SELECT id FROM Artist WHERE name = ? ", (artist, ))

#PART: Grab the first information (i.e. the artist) and put it...
#...in the SQL Database, as happen with others.
    artist_id = cur.fetchone()[0]

    cur.execute("""INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )""", (genre, ) )
    cur.execute("SELECT id FROM Genre WHERE name = ? ", (genre, ))
    genre_id = cur.fetchone()[0]
    
    cur.execute("""INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )""", (album, artist_id) )
    cur.execute("SELECT id FROM Album WHERE title = ? ", (album, ))
    album_id = cur.fetchone()[0]

    cur.execute("""INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )""", 
        (name, album_id, genre_id, length, rating, count) )

#PART: It allow us to extract the info from the disk. It...
#...affect the process and make it slow if it is inside the...
#loop.
conn.commit()


