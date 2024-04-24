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
    
def getMoonAzEL(obsLat,obsLong,JD,siderealTime):
    moonLat,moonLong = getMoonLocation(JD)
    # print(moonLat)
    # print(moonLong)
    changeInLon = moonLong - obsLong
    y = math.sin(changeInLon) * math.cos(moonLat)
    x = math.cos(obsLat)*math.sin(moonLat) - math.sin(obsLat)*math.cos(moonLat)*math.cos(changeInLon)
    az = math.atan2(y,x)
    print(az)
    el = math.acos((math.sin(obsLat)*math.sin(moonLong))+(math.cos(obsLat)*math.cos(moonLong)*math.cos(siderealTime)))
    print(el)
    return az,el

    
def makeMap(time, date, lat,lon):
    prev=0
    allStars = {'x':[],'y':[],'mag':[],'label':[],'color':[]}
    planetLocations={'x':[],'y':[]}
    constellations = {'Taurus':[]}
    dateAndTime = str(date+" "+time)
    currentDate = datetime.strptime(dateAndTime,'%m/%d/%Y %I:%M%p')
    latDec = convertLatAndLong(lat)
    lonDec = convertLatAndLong(lon)
    GSTime = GST(currentDate,latDec,lonDec)
    siderealTime = testLST(currentDate,GSTime,lonDec)
    allStarData = getAllVisibleStars(latDec,lonDec,siderealTime)
    allPlanets = getAllPlanetData()
    jd = getJD(currentDate)
    moonAz,moonEl = getMoonAzEL(latDec,lonDec,jd,siderealTime)
    moonPhase = getMoonPhase(currentDate)
    for planet in allPlanets:
        if(planet !='Earth' and planet!='Sun'):
            tempra,tempdec = getPlanetRADec(allPlanets[planet],allPlanets['Earth'],jd)
            tempaz,tempel = getStarAzEl(tempra,tempdec,siderealTime,latDec,lonDec)
            allStars['x'].append(tempaz)
            allStars['y'].append(tempel)
            # print(tempel)
            # print(tempaz)
            allStars['color'].append(allPlanets[planet][12])
            allStars['mag'].append(10)
            allStars['label'].append(planet)
    for star in allStarData:
        #pass in RA and Dec
        tempAz,tempEl = getStarAzEl(star[7],star[8],siderealTime,latDec,lonDec)
        #suns magnitude is so big we need to diminish it 
        allStars['x'].append(tempAz)
        allStars['y'].append(tempEl)
        print(tempEl)
        allStars['color'].append('white')
        if(star[6]=='Sol'):
            allStars['mag'].append((3 ** ( star[9]/ -2.5)))
        else:
            allStars['mag'].append((100*10**(star[9]/-2.5))+10)
            print((100*10**(star[9]/-2.5))+10)
        if(star[6]!=''):
            allStars['label'].append(star[6])
        # if(star[10]=='Taurus'):
        #     if(star[11]!=1):
        #         allStars['x'].append(tempAz)
        #         allStars['y'].append(tempEl)
        #         allStars['color'].append('white')

        #         constellations[star[10]].append([prev,(tempAz,tempEl)])
        #     else:
        #         allStars['x'].append(tempAz)
        #         allStars['y'].append(tempEl)
        #         constellations[star[10]].append([(tempAz,tempEl)])
        #         prev=(tempAz,tempEl)
        #         allStars['color'].append('white')
            
            # allStars['label'].append(str(star[0]))
        # if(star[10] in constellations):
        #     constellations[star[10]][0].append((tempAz,tempEl))
        # elif(star[10]!=None):
        #     constellations[star[10]]=[[]]
        #     constellations[star[10]][0].append((tempAz,tempEl))
    map = drawMap(allStars,constellations,moonPhase,moonAz,moonEl)
    #pass in time, date, and location
    #run math commands
    #run map creation function
    #save map
    #return map
    return map

