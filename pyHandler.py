import sqlite3
from dbHandler import *
import os
from dbHandler import  *
def checkDB():
    try:
        # Connect to DB and create a cursor
        connection = sqlite3.connect('stars.db')
        cursor = connection.cursor()
        print('Database connection established.')

        #only run if file is empty
        if os.path.getsize("stars.db") == 0:
            createDatabase()
            print ("Table created.")
            parseCSVStars()

            #test lines
            #query = '''INSERT INTO music(name, game, location, theme, instrument, vibe) VALUES(?, ?, ?, ?, ?, ?)'''
            #cursor.execute(query, ("Song of Time", "Ocarina of Time, Majora's Mask", "temple, anywhere", "time, playable, magic", "ocarina", "magic, solo, divine"))

            connection.commit()
                
        
        # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)
        close(connection)
        return
    
def makeMap(time, date, location):
    #pass in time, date, and location
    #run math commands
    #run map creation function
    #save map
    #return map
    return
