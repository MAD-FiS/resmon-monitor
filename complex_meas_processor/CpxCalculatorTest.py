import unittest
from unittest.mock import MagicMock

import datetime
from CpxCalculator import CpxCalculator
from MeasurementDef import MeasurementDef

class TestCpxCalculatorTest(unittest.TestCase):
    def test_Calculator(self):
        Y = 2018
        M = 6
        D = 13
        MS = 0
        startMinute = 0
        endMinute = 6
        lastCalcTime = datetime.datetime(Y, M, D, 17, startMinute, 0, MS)
        window = 61*2
        interval = 20
        measDef = MeasurementDef("boring_cabbage", "myMetricId", "CPU_USAGE", window, interval, lastCalcTime, "dummy description")
        cpxCalculator = CpxCalculator(measDef)
        
        sensorInterval = 30
        numOfMeasures = 10
        simpleMeasurements = [[i, lastCalcTime + datetime.timedelta(seconds=i*sensorInterval)] for i in range(numOfMeasures)]
        calculationTime = datetime.datetime(Y, M, D, 17, endMinute, 0, MS) 
        cpxMeasurements = cpxCalculator.calculate(simpleMeasurements, calculationTime)

        self.assertEqual(len(cpxMeasurements), ((endMinute-startMinute)*60-window)//measDef.interval + 1)

        self.assertAlmostEqual(cpxMeasurements[0][0], 2.5) 
        self.assertAlmostEqual(cpxMeasurements[1][0], 2.5) 
        self.assertAlmostEqual(cpxMeasurements[2][0], 3.5) 
        self.assertAlmostEqual(cpxMeasurements[3][0], 4.5) 
if __name__ == '__main__':
    unittest.main()
