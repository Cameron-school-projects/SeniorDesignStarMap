import unittest
import datetime
from starMath import *
from datetime import datetime
class TestStarMath(unittest.TestCase):
    def test_UTC(self):
        #testing conversion of April 20th, 2024 at 7:30 Huntsville AL time
        baseTime = datetime(2024,4,20,7,30)
        lat = 34.7304
        long = 86.5861
        UTCDate = datetime(2024,4,21,12,30)
        calculatedDate = getUTC(lat,long,baseTime)
        self.assertEqual(abs(calculatedDate-UTCDate) < datetime.timedelta(seconds=1))
    
    def test_JD(self):
        baseDate = datetime(2008,1,5,20)
        JD = getJD(baseDate)
        self.assertAlmostEqual(JD,2454471)

    def test_LST(self):
        lat = 34.7304
        long = 86.5861
        baseTime = datetime(2024,4,20,7,30)
        gst = GST(baseTime,lat,long)
        LST = calcLST(baseTime,gst,long)
        print(LST)
        self.assertAlmostEqual(LST,19.17)

    def test_getStarAzEl(self):
        lat = 34.7304
        long = 86.5861
        baseTime = datetime(2024,4,20,7,30)
        gst = GST(baseTime,lat,long)
        LST = calcLST(baseTime,gst,long)
        az,el=getStarAzEl(10,10,LST,lat,long)
        self.assertAlmostEqual(az,.444)
        self.assertAlmostEqual(el,1.117)

    def test_raDegToHMS(self):
        #90 degrees is 6 hours exactly
        degs = 90
        hours,min,sec= raDegToHMS(degs)
        self.assertEqual(hours,6)
        self.assertEqual(min,0)
        self.assertEqual(sec,0.0)


    def test_decDegToDMS(self):
        deg,min,sec=decDegToDMS(90)
        self.assertEqual(deg,90)
        self.assertEqual(min,0)
        self.assertEqual(sec,0.0)
    
    def test_getMoonPhase(self):
        baseTime = datetime(2024,4,20,7,30)
        moonPhase = getMoonPhase(baseTime)
        self.assertAlmostEqual(moonPhase,.39)

