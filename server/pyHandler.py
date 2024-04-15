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
    prev=0
    constellations = {'Aries':[]}
    dateAndTime = str(date+" "+time)
    currentDate = datetime.strptime(dateAndTime,'%m/%d/%Y %I:%M%p')
    latDec = convertLatAndLong(lat)
    lonDec = convertLatAndLong(lon)
    GSTime = GST(currentDate,latDec,lonDec)
    siderealTime = testLST(currentDate,GSTime,lonDec)
    allStarData = getAllVisibleStars(latDec,lonDec)
    tarAz,tarEl = getStarAzEl(4,25,siderealTime,latDec,lonDec)
    constellations['Aries'].append((tarAz,tarEl))
    for star in allStarData:
        #pass in RA and Dec
        tempAz,tempEl = getStarAzEl(star[7],star[8],siderealTime,latDec,lonDec)
        #suns magnitude is so big we need to diminish it 
        allStars['x'].append(tempAz)
        allStars['y'].append(tempEl)
        if(star[6]=='Sol'):
            allStars['mag'].append((3 ** ( star[9]/ -2.5)))
        else:
            allStars['mag'].append((100*10**(star[9]/-2.5))+10)
        if(star[6]!=''):
            allStars['label'].append(star[6])
        # if(star[10]=='Aries'):
        #     if(star[11]!=1):
        #         allStars['x'].append(tempAz)
        #         allStars['y'].append(tempEl)
                # constellations[star[10]].append([prev,(tempAz,tempEl)])
                # prev=(tempAz,tempEl)
            # else:
            #     allStars['x'].append(tempAz)
            #     allStars['y'].append(tempEl)
            #     constellations[star[10]].append([(tempAz,tempEl)])
            #     prev=(tempAz,tempEl)
            
            # allStars['label'].append(str(star[0]))
        # if(star[10] in constellations):
        #     constellations[star[10]][0].append((tempAz,tempEl))
        # elif(star[10]!=None):
        #     constellations[star[10]]=[[]]
        #     constellations[star[10]][0].append((tempAz,tempEl))
    # print(constellations)
    # for key in constellations:
    #     constellations[key][0] = sorted(constellations[key][0],key=lambda tup: tup[1])
    map = drawMap(allStars,constellations)
    #pass in time, date, and location
    #run math commands
    #run map creation function
    #save map
    #return map
    return map

