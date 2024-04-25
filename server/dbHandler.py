import sqlite3
from starMath import checkConstellationVisibility, checkStarVisibility
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
               color STRING,
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
            starToInsert = [(key),(idx+1),(item)]
            cursor.execute("UPDATE stars SET constellation=?, constellationNum=? WHERE id=?",starToInsert)
    connection.commit()


def addStar():
    #add in everything individually
    return

def addPlanets():
    connection =  sqlite3.connect("stars.db")
    cursor = connection.cursor()
    planetVals = {"Mercury": [252.25084,538101628.3,0.38709893,0.00000066,0.20563069,0.00002527,7.00487,23.51,77.45645,573.57,48.33167,446.3,'pink'],
                  "Venus":[181.97973,210664136.1,0.72333199,0.00000092,0.00677323,0.00004938,3.39471,2.86,131.53298,108.8,76.68069,996.89,'white'],
                  "Earth":[100.46435,129597740.6,1.00000011,0.00000005,0.01671022,0.00003804,0.00005,46.94,102.94719,1198.28,-11.26064,18228.25,'blue'],
                  "Mars":	[55.45332,68905103.78,1.52366231,0.00007221,0.09341233,0.00011902,1.85061,25.47,336.04084,1560.78,49.57854,1020.19,'red'],
                  "Jupiter":	[34.40438,10925078.35,5.20336301,0.00060737,0.04839266,0.0001288,1.3053,-4.15,14.75385,839.93,100.55615,1217.17,'whitesmoke'],
                  "Saturn":	[49.94432,4401052.95,9.53707032,0.0030153,0.0541506,0.00036762,2.48446,6.11,92.43194,1948.89,113.71504,1591.05,'gold'],
                   "Uranus":	[313.23218,1542547.79,19.19126393,0.00152025,0.04716771,0.0001915,0.76986,2.09,170.96424,1312.56,74.22988,1681.4,'lightblue'],
                   "Neptune":	[304.88003,786449.21,30.06896348,0.00125196,0.00858587,0.00125196,1.76917,3.64,44.97135,844.43,131.72169,151.25,'steelblue'],
                   "Pluto":	[238.92881,522747.9,39.48168677,0.00076912,0.24880766,0.00006465,17.14175,11.07,224.06676,132.25,110.30347,37.33,'powderblue'],
                   "Sun":[100.46435,129597740.6,1.00000011,0.00000005,0.01671022,0.00003804,0.00005,46.94,102.94719,1198.28,-11.26064,18228.25,'darkorange'],
                  }
    for idx,key in enumerate(planetVals):
        tempVals = [idx,key,planetVals[key][0],planetVals[key][1],planetVals[key][2],planetVals[key][3],planetVals[key][4],planetVals[key][5],planetVals[key][6],planetVals[key][7],planetVals[key][8],planetVals[key][9],planetVals[key][10],planetVals[key][11],None,planetVals[key][12]]
        cursor.execute("INSERT INTO planets(id,planetName,lScale,lProp,aScale,aConst,eScale,eProp,iScale,iProp,wScale,wProp,oScale,oProp,constellation,color) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",tempVals)

    connection.commit()




def getAllPlanetData():
    connection =  sqlite3.connect("stars.db")
    cursor = connection.cursor()
    planetDict = {}
    planets = cursor.execute("SELECT * FROM planets")
    planets = planets.fetchall()
    for planet in planets:
        planetDict[planet[1]] = [planet[2],planet[3],planet[4],planet[5],planet[6],planet[7],planet[8],planet[9],planet[10],planet[11],planet[12],planet[13],planet[15]]
    
    return planetDict


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
def getAllVisibleObjects(observerLat,observerLong,LST):
    connection =  sqlite3.connect("stars.db")
    cursor = connection.cursor()
    allStars = cursor.execute("SELECT * from stars WHERE properName!='Sol' ORDER BY constellationNum")
    allStars = allStars.fetchall()
    allConstellations = cursor.execute("SELECT * FROM constellations")
    allConstellations = allConstellations.fetchall()
    visibleConstellations = checkConstellationVisibility(allConstellations,observerLat,LST)
    visibleStars = checkStarVisibility(allStars,observerLat,LST)

    return visibleStars,visibleConstellations



