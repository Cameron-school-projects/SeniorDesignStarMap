import sqlite3
connection =  sqlite3.connect("stars.db")
cursor = connection.cursor()
constellationReferences = {
    'Aries':[9257,6888,6195,6147],
    'Taurus':[18796,15108,14714,14183,14373,14710,18021,13110,11284],
    }
def createDatabase():
    cursor.execute('''CREATE TABLE constellations(
               name STRING PRIMARY KEY,
                dec DOUBLE,
                RA DOUBLE
    );''')
    cursor.execute('''CREATE TABLE stars(
               id INTEGER PRIMARY KEY,
               hip INTEGER,
               HD INTEGER,
               HR INTEGER,
               Gliese STRING,
               properName STRING,
               bayerFlamesteed STRING,
               RA DOUBLE,
               dec DOUBLE,
               magnitude DOUBLE,
               constellation STRING,
               FOREIGN KEY (constellation) REFERENCES constellations(name) 
    );''')
    cursor.execute('''CREATE TABLE planets(
               id INTEGER PRIMARY KEY,
               planetName STRING,
               lScale DOUBLE,
               lProp DOUBLE,
               aScale DOUBLE,
               aConst DOUBLE,
               eScale DOUBLE,
               eProp DOUBLE,
               iScale DOUBLE,
               iProp DOUBLE,
               wScale DOUBLE,
               wProp DOUBLE,
               oScale DOUBLE,
               oProp DOUBLE,
               constellation STRING,
               FOREIGN KEY (constellation) REFERENCES constellations(name) 
    );''')


def parseCSVStars():
    with open('hyg.csv',encoding='utf-8') as f:
        next(f)
        for line in f:
            elements = line.split(",")
            floatMagnitude = float(elements[10])
            if(floatMagnitude<6.0):
                newStar = [elements[0],elements[1],elements[2],elements[3],elements[4],elements[5],elements[6],elements[7],elements[8],elements[10]]
                cursor.execute("INSERT INTO STARS VALUES(?,?,?,?,?,?,?,?,?,?)",newStar)
                #Check if star is known to be in a constellation
                connectedConst = constellationReferences.get(elements[0])
                if(connectedConst!=None):
                    cursor.execute("INSERT INTO CONSTELLATIONS(name) VALUES(?,?)",(connectedConst,elements[0]))
        connection.commit()


def addStar():
    #add in everything individually
    return


#closes database
def close(connectionName, cursorName = False):
    if cursorName:
        cursorName.close()
    if connectionName:
        connectionName.close()
        print("\nSQLite Connection closed")

#Returns all stars visible to specific latitude and longitude 
#Expects latitude/longitude to be in decimal        
#When returning, python only returns values
#the corresponding attributes are:
        #allStars[0] = id
        #allStars[1] = hip
        #allStars[2] = HD
        #allStars[3] = HR
        #allStars[4] = Gliese
        #allStars[5] = properName
        #allStars[6] = bayerflamesteed
        #allStars[7] = RA
        #allStars[8] = dec
        #allStars[9] = magnitude
def getAllVisibleStars(observerLat,observerLong):
    queryString=""
    visibleLat=0   
    visibleLong=0  
    #build query based on lat/long of observer
    if(observerLat<0):
        #any stars within 90 degrees of declination will be visible
        visibleLat = (90+observerLat-5)/360
        queryString = "SELECT * FROM stars WHERE RA BETWEEN 24 AND  ?"
    else:
        #any stars within 90 degrees of declination will be visible
        visibleLat = (90-observerLat+5)/360
        #dont need to filter on magnitude, as when inserting we only add if magnitude is less than 6.0
        queryString = "SELECT * FROM stars WHERE RA BETWEEN ? AND 24"
    if(observerLong<0):
        visibleLong=(90+observerLong)
        queryString = queryString+" AND dec < ?"
    else:
        visibleLong=(90-observerLong)
    #     queryString = queryString+" AND RA BETWEEN ? AND 24"
    allParams = (visibleLat,visibleLong)
    #dont need to filter on magnitude, as when inserting we only add if magnitude is less than 6.0
    allStars = cursor.execute(queryString,allParams)
    return allStars.fetchall()
