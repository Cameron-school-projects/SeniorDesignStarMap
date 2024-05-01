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
import ephem
from PyAstronomy import pyasl
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
    return az,el

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

    ra = math.atan2(yeq, xeq)
    dec = math.atan(zeq/math.sqrt(xeq**2 + yeq**2)) 

    return ra, dec

def getPlanetAzEl(lat, lon, ra, dec,LST):
    #not sure if this is different from star RA and Dec but we'll see I guess
    #takes in latitude, longitude, and ra and dec in degrees
    #returns planet azimuth and elevation
    # if (lat<0):
    #     lat *= -1
    # if lon < 0:
    #     lon *= -1
    A = LST - ra   #this is a vague time object. We'll figure it out later
    # if A<0:
    #     A += 360
    decRad = dec 
    latRad = lat 
    hRad = lat

    #find altitude in radians, which I'm assuming is also elevation
    sinEl = (math.sin(decRad) * math.sin(latRad)) + (math.cos(decRad) * math.cos(latRad) * math.cos(hRad))
    el = math.asin(sinEl)

    #calculate azimuth in radians
    try:
        cosAz = (math.sin(decRad) - math.sin(el) * math.sin(latRad)) / (math.cos(el) * math.cos(latRad))
        az = cosAz
        # az = math.acos(cosAz)
    except:
        az = 0

    # print((az,el))
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

def getMoonPhase(currentDate):
    ephemDate = ephem.Date(currentDate)
    nnm = ephem.next_new_moon(ephemDate)
    pnm = ephem.previous_new_moon(ephemDate)

    phase = (ephemDate-pnm)/(nnm-pnm)
    return phase
  #Note that there is a ephem.Moon().phase() command, but this returns the
  #percentage of the moon which is illuminated. This is not really what we want.


    #gets moon phase
    #takes the date as a float, where Feb 1, 2009 is 2009.087
    # k = (year-1900.0)*12.3685
    #T = k / 1236.85
    #i have no idea what the math says so I guess this is happening now
    #124.2322 is a full moon --> 0.566
    #124.1913 is a new moon --> 0.060

    # phase = k%1
    # if phase <= 0.1 or phase>.93:     #new moon
    #     return 0
    # elif phase <= 0.19:   #waxing crescent
    #     return 1
    # elif phase <= .32:   #waxing quarter
    #     return 2
    # elif phase <= .45:  #waxing gibbous
    #     return 3
    # elif phase <= .57:   #full moon
    #     return 4
    # elif phase <= .69:  #waning gibbous
    #     return 5
    # elif phase <= .81:   #waning quarter
    #     return 6
    # elif phase <= .93:    #waning crescent
    #     return 7

    #return the phase based on a threshold
    #if 8, something went wrong
    # return 8

def getMoonLocation(JD):
    #gets moon's location
    res = pyasl.moonpos(JD,radian=True) 
    T = (JD-2415020.0) / 36525

    moonL = 270.434164 + 481267.8831*T
    sunM = 358.475833 + 35999.0498*T
    moonM = 296.104608 + 477198.8491*T
    moonD = 350.737486 + 445267.1142*T
    F = 11.250889 + 483202.0251*T

    e = 1 - 0.002495*T - 0.00000752*T*T

    moonLon = moonL + (6.288750 * math.sin(math.radians(moonM))) + (1.274018 * math.sin(math.radians(2*moonD - moonM))) + (0.658309 * math.sin(math.radians(2*moonD))) + (0.213616 * math.sin(math.radians(2*moonM))) - (0.185596 * math.sin(math.radians(sunM)) * e) - (0.114336 * math.sin(math.radians(2*F))) + (0.058793 * math.sin(math.radians(2*moonD - 2*moonM))) + (0.057212 * math.sin(math.radians(2*moonD - sunM - moonM)) * e) + (0.053320 * math.sin(math.radians(2*moonD + moonM))) + (0.045874 * math.sin(math.radians(2*moonD - sunM)) * e)
    moonLat = (5.128189 * math.sin(math.radians(F))) + 0.280606 * math.sin(math.radians(moonM + F)) + (0.277693 * math.sin(math.radians(moonM - F))) + (0.173238 * math.sin(math.radians(2*moonD - F))) + (0.055413 * math.sin(math.radians(2*moonD + F - moonM))) + (0.046272 * math.sin(math.radians(2*moonD - F - moonM))) + (0.032573 * math.sin(math.radians(2*moonD + F))) + (0.017198 * math.sin(math.radians(2*moonM + F))) + (0.009267 * math.sin(math.radians(2*moonD + moonM - F))) + (0.008823 * math.sin(math.radians(2*moonM - F)))

    #return moon's geocentric longitude and latitude
    return res[3], res[4]

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

def calcLST(date,GMST,Long):
    #Convert to the local sidereal time by adding the longitude (in hours) from the GMST.
    #(Hours = Degrees/15, Degrees = Hours*15)
    Long = Long/15      #Convert longitude to hours
    LST = GMST+Long     #Fraction LST. 
    if LST < 0:
        LST = LST +24
    LST = LST %24
    LSTmm = (LST - int(LST))*60          #convert fraction hours to minutes
    LSTss = (LSTmm - int(LSTmm))*60      #convert fractional minutes to seconds
    LSThh = int(LST)
    LSTmm = int(LSTmm)
    LSTss = int(LSTss)    
    #print for testing
    # print ('\nLocal Sidereal Time %s:%s:%s \n\n' %(LSThh, LSTmm, LSTss))

    return LST

def checkStarVisibility(allStars,lat,LST):
    visibleStars=[]
    for star in allStars:
        tempAlt = math.asin((math.sin(lat)*math.sin(star[8])+math.cos(lat)*math.cos(star[8])*math.cos(LST)))
        if(tempAlt>0):
            visibleStars.append(star)
    return visibleStars


def checkConstellationVisibility(allConstellations,lat,LST):
    visibleConstellations=[]
    for constellation in allConstellations:
        tempAlt = (math.sin(lat)*math.sin(constellation[2])+math.cos(lat)*math.cos(constellation[2])*math.cos(LST))
        tempAlt = math.asin(tempAlt)
        if(tempAlt>0):
            visibleConstellations.append(constellation)
    return visibleConstellations