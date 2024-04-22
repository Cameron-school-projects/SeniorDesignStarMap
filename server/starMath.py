import math
import datetime
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from datetime import timedelta
from pytz import utc
from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy import units as u
from datetime import timezone
from astropy.coordinates import get_body
#constants :/
RADS = math.pi / 180
DEGS = 180 / math.pi

def mod2Pi(degree):
    #takes in angle in radians
    #keeps angles under 360 degrees
    B = degree/(2*math.pi)
    if B>=0:
        B = math.floor(B)
    else:
        B = math.ceil(B)
    A = (2*math.pi) * B
    if A<0:
        A = 2*math.pi + A
    return A

#converts julian date to normal date
#assumes JD is a string representation of a julian date
#returns string
def getDate(JD):
    #split to get year and day of year separably 
    dateParts = JD.split("-")
    dateYear = dateParts[0]
    dayOfYear = dateParts[1]
    #date will be time different between jan 1st of that year to passed in day of year
    return (datetime(dateYear, 1, 1) + datetime.timedelta(dayOfYear - 1))

#converts date to julian time
#assumes that date is a string representing current date in mm/dd/yy or mm/dd/yyyy format 
#returns string
def getJD(date):
    months = float(date.month)
    days = float(date.day)
    years = float(date.year)
    hours = float(date.hour)
    mins = float(date.minute)
    mins = mins/60
    UT = hours+mins
    JD = (367*years) - int((7*(years+int((months+9)/12)))/4) + int((275*months)/9) + days + 1721013.5 + (UT/24)
    return JD
#returns GST for current time,
#expects localTime to be a datetime object
def getGST(localTime):
    epoch = datetime(2004,1,1)
    timeDelta = localTime-epoch
    secondsToDeduct = timeDelta.days* 236
    #integer division
    hours = timeDelta.seconds//3600
    secondsToDeduct = secondsToDeduct + (hours-10*(hours))
    return (localTime - timedelta(seconds=secondsToDeduct))

def convertLatAndLong(location):
    multiplier = 1 if location[-1] in ['N', 'E'] else -1
    return multiplier * sum(float(x) / 60 ** n for n, x in enumerate(location[:-1].split('-')))

#returns UTC
#returns datetime object    
def getUTC(lat, lon,date):
    timeZoneConverter = TimezoneFinder()  
    timezone_str = timeZoneConverter.timezone_at(lng=lon, lat=lat)
    oldTimeZone = pytz.timezone(timezone_str)
    return oldTimeZone.localize(date).astimezone( utc )

#return local sidereal time 
#expects time to be in GST
def getLST(time,lon):
    dividedLon = lon/15
    hours = int(dividedLon)
    minutes = (dividedLon*60) % 60
    seconds = (dividedLon*3600) % 60
    #check if print(currentDate)long is west
    if(lon<0):
        LST = time - timedelta(hours=hours,minutes=minutes,seconds=seconds)
    else:
        LST = time + timedelta(hours=hours,minutes=minutes,seconds=seconds)
    lstNumeric = int(LST.hour)
    lstNumeric = lstNumeric+ (int(LST.minute)/10)
    lstNumeric = lstNumeric+ (int(LST.second)/100)
    return lstNumeric

#returns mean sidereal time
#converts from UTC/GMT
def getMST(time):
    observing_location = EarthLocation(lat=46.57*u.deg, lon=7.65*u.deg)
    observing_time = Time(time, scale='utc', location=observing_location)
    MST = observing_time.sidereal_time('mean')
    return MST

def getStarAzEl(ra, dec, time, lat, long):
    #ra, dec, and sidereal time passed in
    #return azimuth and elevation
    h = time-ra
    az = math.atan(-(math.sin(h) * math.cos(dec))/(math.cos(lat)*math.sin(dec) - math.sin(lat)*math.cos(dec)*math.cos(h)))
    el = math.asin(math.sin(lat)*math.sin(dec) + math.cos(lat)*math.cos(dec)*math.cos(h))
    # az = 2*math.cos(az)
    # el = 2*math.sin(el)
    return az, el

def getOrbitalElements(planetData, JD):
    #uses planet data to ccaulate orbital elements and 
    cy = JD/36525
    L = mod2Pi((planetData[0]+planetData[1]*cy/3600)*RADS)
    a = planetData[2] + planetData[3]*cy
    e = planetData[4] + planetData[5]*cy
    i = (planetData[6] - planetData[7] * cy / 3600) * RADS
    w = (planetData[8] + planetData[9] * cy / 3600) * RADS
    o = (planetData[9] - planetData[10] * cy / 3600) * RADS

    #returns all 6 elements
    return L, a, e, i, w, o

def trueAnomaly(m, e):
    #m and e in radians
    E = m + e*math.sin(m) * (1.0 + e*math.cos(m))
    E1 = E
    while(abs(E-E1) > (1.0 ** -12)):
        E1 = E
        E = E1 - (E1 - e * math.sin(E1) - m) / (1 - e * math.cos(E1))
    V = 2 * math.atan(math.sqrt((1+e)/(1-e)) * math.tan(0.5 * E))
    if (V<0):
        V = V+(1*math.pi)
    return V

def getPlanetRADec(planetData, earthData, JD):
    #planet math. Can be run individually for each planet
    #cy = JD / 36525 where JD is julian date counted from 2000
    #returns RA and Dec of the planet

    planet = getOrbitalElements(planetData, JD)
    earth = getOrbitalElements(earthData, JD)

    me = mod2Pi(earth[0] - earth[4])
    ve = trueAnomaly(me, earth[2])
    re = earth[1] * (1-earth[2]**2) / (1 + earth[2] * math.cos(ve))
    xe = re * math.cos(ve + earth[4])
    ye = re * math.sin(ve + earth[4])
    ze = 0.0

    mp = mod2Pi(planet[0] - planet[4])
    vp = trueAnomaly(mp, planet[2])
    rp = planet[1] * (1-planet[2]**2) / (1 + planet[2] * math.cos(vp))
    xh = rp * math.cos(planet[5]) * math.cos(vp + planet[4] - planet[5]) - math.sin(planet[5]) * math.sin(vp + planet[4] - planet[5]) * math.cos(planet[3])
    yh = rp * math.sin(planet[5]) * math.cos(vp + planet[4] - planet[5]) + math.cos(planet[5]) * math.sin(vp + planet[4] - planet[5]) * math.cos(planet[3])
    zh = rp * (math.sin(vp + planet[4] - planet[5]) * math.sin(planet[3]))

    xg = xh - xe
    yg = yh - ye
    zg = zh - ze

    ecl = 23.439281 * RADS
    xeq = xg
    yeq = yg * math.cos(ecl) - zg*math.sin(ecl)
    zeq = yg * math.sin(ecl) + zg*math.cos(ecl)

    ra = mod2Pi(math.atan2(yeq, xeq)) * DEGS
    dec = math.atan(zeq/math.sqrt(xeq**2 + yeq**2)) * DEGS
    
    return ra, dec

def getPlanetAzEl(lat, lon, ra, dec,LST):
    #not sure if this is different from star RA and Dec but we'll see I guess
    #takes in latitude, longitude, and ra and dec in degrees
    #returns planet azimuth and elevation
    if (lat<0):
        lat *= -1
    if lon < 0:
        lon *= -1
    A = LST - ra   #this is a vague time object. We'll figure it out later
    if A<0:
        A += 360
    decRad = dec * RADS
    latRad = lat * RADS
    hRad = lat*RADS

    #find altitude in radians, which I'm assuming is also elevation
    sinEl = (math.sin(decRad) * math.sin(latRad)) + (math.cos(decRad) * math.cos(latRad) * math.cos(hRad))
    el = math.asin(sinEl)

    #calculate azimuth in radians
    try:
        cosAz = (math.sin(decRad) - math.sin(el) * math.sin(latRad)) / (math.cos(el) * math.cos(latRad))
        az = math.acos(cosAz)
    except:
        az = 0
    
    # el *= DEGS
    # az *= DEGS
    
    if(math.sin(hRad>0)):
        az = 360-az 

    return az, el

def raDegToHMS(degree):
    #converts RA from degrees to hours:minutes:seconds
    #returns hour, minute, second
    h = int(degree / 15.0)
    m = int(((degree/15.0) - h) * 60.0)
    s = ((((degree/15.0) - h) * 60.0)-m) * 60
    return h, m, s

def decDegToDMS(degree):
    #converts declination from degrees to degree:minutes:seconds
    #returns degree, minute, second
    d = int(degree)
    m = int((degree - d)* 60.0)
    s = (((degree - d)*60.0)-m)*60.0 
    return d, m, s

def getMoonPhase(time, julianDate, location):
    #gets moon phase
    #takes the date as a float, where Feb 1, 2009 is 2009.087
    k = (year-1900.0)*12.3685
    #T = k / 1236.85
    #i have no idea what the math says so I guess this is happening now
    #124.2322 is a full moon --> 0.566
    #124.1913 is a new moon --> 0.060

    phase = k%1
    if phase <= 0.1 or phase>.93:     #new moon
        return 0
    elif phase <= 0.19:   #waxing crescent
        return 1
    elif phase <= .32:   #waxing quarter
        return 2
    elif phase <= .45:  #waxing gibbous
        return 3
    elif phase <= .57:   #full moon
        return 4
    elif phase <= .69:  #waning gibbous
        return 5
    elif phase <= .81:   #waning quarter
        return 6
    elif phase <= .93:    #waning crescent
        return 7

    #return the phase based on a threshold
    #if 8, something went wrong
    return 8

def getMoonLocation(T):
    #gets moon's location
    #input date
    #those are some ugly formulas :((
    T = (getJD(date)-2415020.0) / 36525

    moonL = 270.434164 + 481267.8831*T
    sunM = 358.475833 + 35999.0498*T
    moonM = 296.104608 + 477198.8491*T
    moonD = 350.737486 + 445267.1142*T
    F = 11.250889 + 483202.0251*T

    e = 1 - 0.002495*T - 0.00000752*T*T

    moonLon = moonL + (6.288750 * math.sin(moonM*RADS)) + (1.274018 * math.sin((2*moonD - moonM)*RADS)) + (0.658309 * math.sin((2*moonD)*RADS)) + (0.213616 * math.sin((2*moonM)*RADS)) - (0.185596 * math.sin((sunM)*RADS) * e) - (0.114336 * math.sin(2*F*RADS)) + (0.058793 * math.sin((2*moonD - 2*moonM)*RADS)) + (0.057212 * math.sin((2*moonD - sunM - moonM)*RADS) * e) + (0.053320 * math.sin((2*moonD + moonM)*RADS)) + (0.045874 * math.sin((2*moonD - sunM) * RADS) * e)
    moonLat = (5.128189 * math.sin(F*RADS)) + 0.280606 * math.sin((moonM + F)*RADS) + (0.277693 * math.sin((moonM - F)*RADS)) + (0.173238 * math.sin((2*moonD - F)*RADS)) + (0.055413 * math.sin((2*moonD + F - moonM)*RADS)) + (0.046272 * math.sin((2*moonD - F - moonM)*RADS)) + (0.032573 * math.sin((2*moonD + F)*RADS)) + (0.017198 * math.sin((2*moonM + F)*RADS)) + (0.009267 * math.sin((2*moonD + moonM - F)*RADS)) + (0.008823 * math.sin((2*moonM - F)*RADS))

    #return moon's geocentric longitude and latitude
    return moonLon, moonLat

def GST(date,lat,lon):
    dateUTC = getUTC(lat,lon,date)
    #calculate the Julian date:
    JD = getJD(dateUTC)
    #calculate the Greenwhich mean sidereal time:
    GMST = 18.697374558 + 24.06570982441908*(JD - 2451545)
    GMST = GMST % 24    #use modulo operator to convert to 24 hours
    GMSTmm = (GMST - int(GMST))*60          #convert fraction hours to minutes
    GMSTss = (GMSTmm - int(GMSTmm))*60      #convert fractional minutes to seconds
    GMSThh = int(GMST)
    GMSTmm = int(GMSTmm)
    GMSTss = int(GMSTss)
    # print ('\nLocal G Time %s:%s:%s \n\n' %(GMSThh, GMSTmm, GMSTss))
    return GMST

def testLST(date,GMST,Long):
    #Convert to the local sidereal time by adding the longitude (in hours) from the GMST.
    #(Hours = Degrees/15, Degrees = Hours*15)
    Long = Long/15      #Convert longitude to hours
    LST = GMST+Long     #Fraction LST. If negative we want to add 24...
    if LST < 0:
        LST = LST +24
    LST = LST %24
    LSTmm = (LST - int(LST))*60          #convert fraction hours to minutes
    LSTss = (LSTmm - int(LSTmm))*60      #convert fractional minutes to seconds
    LSThh = int(LST)
    LSTmm = int(LSTmm)
    LSTss = int(LSTss)    
    # print ('\nLocal Sidereal Time %s:%s:%s \n\n' %(LSThh, LSTmm, LSTss))

    return LST

def checkStarVisibility(allStars,lat,LST):
    visibleStars=[]
    for star in allStars:
        tempAlt = math.asin((math.sin(lat)*math.sin(star[8])+math.cos(lat)*math.cos(star[8])*math.cos(LST)))
        if(tempAlt>0):
            visibleStars.append(star)
    return visibleStars
