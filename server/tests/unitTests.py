import unittest
import datetime
from starMath import *
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
