import sqlite3
from dbHandler import *
import os
from datetime import datetime
import datetime
from dbHandler import  *
from starMath import *
from mapPlot import *
import numpy as np
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
    
def makeMap(time, date, lat,lon):
    allStars = {'x':[],'y':[],'mag':[],'label':[]}
    dateAndTime = str(date+" "+time)
    currentDate = datetime.strptime(dateAndTime,'%m/%d/%Y %I:%M%p')
    latDec = convertLatAndLong(lat)
    lonDec = convertLatAndLong(lon)
    GSTime = getGST(currentDate)
    GMTime = getUTC(latDec,lonDec,currentDate.hour,currentDate.minute,currentDate.second,currentDate.day,currentDate.month,currentDate.year)
    siderealTime = getLST(GSTime,lonDec)
    allStarData = getAllStars()
    for star in allStarData:
        #pass in RA and Dec
        tempRA,tempDec = getStarAzEl(star[7],star[8],siderealTime,latDec,lonDec)
        allStars['x'].append(tempRA)
        allStars['y'].append(tempDec)
        #suns magnitude is so big we need to diminish it 
        if(star[5]=='Sol'):
            allStars['mag'].append((3 ** ( star[9]/ -2.5)))
        else:
            allStars['mag'].append(100*10**(star[9]/-2.5))
        if(star[5]!=''):
            allStars['label'].append(star[5])

    map = drawMap(allStars)
    #pass in time, date, and location
    #run math commands
    #run map creation function
    #save map
    #return map
    return map

