import sqlite3
connection =  sqlite3.connect("stars.db")
cursor = connection.cursor()
def createDatabase():
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
               magnitude DOUBLE
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
               oProp DOUBLE
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
def getAllStars():
    #dont need to filter on magnitude, as when inserting we only add if magnitude is less than 6.0
    allStars = cursor.execute("SELECT * FROM stars")
    return allStars.fetchall()
