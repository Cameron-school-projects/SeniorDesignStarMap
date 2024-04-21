import sqlite3
from starMath import checkStarVisibility
constellationReferences = {
    'Aries':[9257,6147,6195,6888],
    'Taurus':[18796,15108,14714,14183,14373,14710,18021,13110,11284],
    'Gemini':[23453,22916,24803,25932,27698,86307,23358,21860,21289,27015,27636,22291,25784,25267,23969],
    'Cancer':[31816,31577,31661,32566,29788],
    'Leo':[35524,35934,37309,37506,36763,36830,40631,42525,40626,37506],
    'Virgo':[52290,49844,48306,47776,50455,50649,52116,46533,46201,46929,42598,44220,45451],
    'Libra':[56097,55578,55074,54037,52562,53308,55172,55262],
    'Scorpius':[61677,61845,62385,62676,62069,60538,59500,59345,59254,58437,58094,57640,56460,56747,57143,56345,56260],
    'Sagittarius':[67811,67014,66393,67523,65228,64997,63828,64804],
    'Capricornus':[72769,74379,74748,76950,77585,78188,77773,76670,75605],
    'Aquarius':[74474,74803,77257,79284,79976,79334,80250,80644,80999,83242,82014,81843,82126],
    'Pisces':[3909,4313,4011,4959,5731,6605,5510,4892,3437,2640,85716,84662,84008,83413,83938,84769]
    }
consetllationLocations=[(2,19),(4,25),(7,18),(8,14),(11,17),(13,-3),(15,-13),(17,-32),(19,-32),(21,-21),(23,-13),(1,12)]
# ,(4,25),(7,18),(8,14),(11,17),(13,-3),(15,-13),(17,-32),(19,-32),(21,-21),(23,-13),(1,12)
def createDatabase():
    connection =  sqlite3.connect("stars.db")
    cursor = connection.cursor()
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
               bayerFlamesteed STRING,
               properName STRING,
               RA DOUBLE,
               dec DOUBLE,
               magnitude DOUBLE,
               constellation STRING,
                constellationNum INTEGER,
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
    connection =  sqlite3.connect("stars.db")
    cursor = connection.cursor()
    for idx,key in enumerate(constellationReferences):
        params = [(key),(consetllationLocations[idx][0]),(consetllationLocations[idx][1])]
        cursor.execute("INSERT INTO CONSTELLATIONS(name,dec,RA) VALUES(?,?,?)",params)
    connection.commit()

    with open('hyg.csv',encoding='utf-8') as f:
        next(f)
        for line in f:
            elements = line.split(",")
            floatMagnitude = float(elements[10])
            if(floatMagnitude<6.0):
                newStar = [elements[0],elements[1],elements[2],elements[3],elements[4],elements[5],elements[6],elements[7],elements[8],elements[10],None,0]
                cursor.execute("INSERT INTO stars VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",newStar)       
        connection.commit()
    for key in constellationReferences:
        for idx,item in enumerate(constellationReferences.get(key)):
            print(idx+1)
            print(item)
            starToInsert = [(key),(idx+1),(item)]
            cursor.execute("UPDATE stars SET constellation=?, constellationNum=? WHERE id=?",starToInsert)
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
        #allStars[10] = constellation(if applicable)
def getAllVisibleStars(observerLat,observerLong,LST):
    connection =  sqlite3.connect("stars.db")
    cursor = connection.cursor()
    queryString=""
    observerDec = observerLat
    observerRA = LST    
    if(observerLat<0):
        queryString = "SELECT * FROM stars WHERE (dec + ? ) < -90"
    else:
        queryString = "SELECT * FROM stars WHERE (dec + ?) > 90"
    # build query based on lat/long of observer
    # if(observerLong<0):        
    #     queryString = "SELECT * FROM stars WHERE RA BETWEEN ? AND 0"
    # else:
    #     #dont need to filter on magnitude, as when inserting we only add if magnitude is less than 6.0
    #     queryString = "SELECT * FROM stars WHERE RA BETWEEN ? AND 24"
    # if(observerLat<0):        
    #     visibleLong2=(90+observerLat)
    #     visibleLong1 = (90-observerLat)
    #     tempLong =visibleLong2%180 
    #     if(-tempLong!=visibleLong2):
    #         visibleLong2=tempLong
    #     tempLong = visibleLong1%180
    #     if(-tempLong!=visibleLong1):
    #         visibleLong1=tempLong
    #     queryString = queryString+" AND dec BETWEEN ? AND ? ORDER BY constellationNum"
    # else:
        
    #     visibleLong1=(90-observerLat)
    #     visibleLong2 = (90+observerLat)
    #     tempLong =visibleLong1%180 
    #     if(tempLong!=visibleLong1 or -tempLong!=visibleLong1):
    #         visibleLong1=-tempLong
    #     tempLong = visibleLong2%180
    #     if(tempLong!=visibleLong2):
    #         visibleLong2=tempLong
    #     queryString = queryString+" AND dec BETWEEN ? AND ? ORDER BY constellationNum"
    allParams = [(observerLat)]
    #dont need to filter on magnitude, as when inserting we only add if magnitude is less than 6.0
    allStars = cursor.execute(queryString,allParams)
    allStars = allStars.fetchall()
    visibleStars = checkStarVisibility(allStars,observerLat,LST)
    return visibleStars


