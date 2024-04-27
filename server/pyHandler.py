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
            connection.commit()
                
        
        # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)
        close(connection)
        return
    
def getMoonAzEL(obsLat,obsLong,JD,siderealTime):
    moonLat,moonLong = getMoonLocation(JD)
    changeInLon = moonLong - obsLong
    y = math.sin(changeInLon) * math.cos(moonLat)
    x = math.cos(obsLat)*math.sin(moonLat) - math.sin(obsLat)*math.cos(moonLat)*math.cos(changeInLon)
    az = math.atan2(y,x)
    el = math.acos((math.sin(obsLat)*math.sin(moonLong))+(math.cos(obsLat)*math.cos(moonLong)*math.cos(siderealTime)))
    return az,el

    
def makeMap(time, date, lat,lon):
    allStars = {'x':[],'y':[],'mag':[],'label':[],'color':[]}
    constellations = {}
    dateAndTime = str(date+" "+time)
    currentDate = datetime.strptime(dateAndTime,'%m/%d/%Y %I:%M%p')
    latDec = convertLatAndLong(lat)
    lonDec = convertLatAndLong(lon)
    GSTime = GST(currentDate,latDec,lonDec)
    siderealTime = testLST(currentDate,GSTime,lonDec)
    allStarData,allConstellations = getAllVisibleObjects(latDec,lonDec,siderealTime)
    allPlanets = getAllPlanetData()
    jd = getJD(getUTC(latDec,lonDec,currentDate))
    for planet in allPlanets:
        if(planet !='Earth'):
            tempra,tempdec = getPlanetRADec(allPlanets[planet],allPlanets['Earth'],jd)
            tempVisibility = math.asin((math.sin(latDec)*math.sin(tempdec)+math.cos(latDec)*math.cos(tempdec)*math.cos(siderealTime)))
            if(tempVisibility>0):
                tempaz,tempel = getPlanetAzEl(latDec,lonDec,tempra,tempdec,siderealTime)
                # print(tempaz)
                # print(tempel)
                allStars['x'].append(tempaz)
                allStars['y'].append(tempel)
                allStars['color'].append(allPlanets[planet][12])
                if(planet=="Sun"):
                    allStars['mag'].append(10000)
                else:
                    allStars['mag'].append(10)

                allStars['label'].append(planet)
    for star in allStarData:
        #pass in RA and Dec
        tempAz,tempEl = getStarAzEl(star[7],star[8],siderealTime,latDec,lonDec)
        #suns magnitude is so big we need to diminish it 
        allStars['x'].append(tempAz)
        allStars['y'].append(tempEl)
        # if(star[6]=='Sol'):
        #     print("hello")
        #     allStars['mag'].append((3 ** ( star[9]/ -2.5)))
        #     allStars['color'].append('darkorange')
        #     allStars['label'].append("Sun")
        # else:
        allStars['mag'].append((100*10**(star[9]/-2.5)))
        allStars['color'].append('white')

        if(star[6]!=''):
            allStars['label'].append(star[6])
        
    
    for constellation in allConstellations:
        tempAz,tempEl = getStarAzEl(constellation[1],constellation[2],siderealTime,latDec,lonDec)
        constellations[constellation[0]] = (tempAz,tempEl)

    moonAz,moonEl = getMoonAzEL(latDec,lonDec,jd,siderealTime)
    moonPhase = getMoonPhase(currentDate)
    map = drawMap(allStars,constellations,moonPhase,moonAz,moonEl)
    return map

