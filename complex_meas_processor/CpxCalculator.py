#!/usr/bin/env python3
from datetime import datetime
from datetime import timedelta


def timePoints(startTime, endTime, interval):
    intervals = int((endTime - startTime).total_seconds() / interval) + 1
    return (startTime + timedelta(seconds=(interval * x)) for x in range(intervals))


class CpxCalculator:
    def __init__(self, measDef):
        self.measDef = measDef

    def calculate(self, simpleMeasurements, nowTime):
        return self.getCpxValues(
            self.measDef.lastCalcTime,
            nowTime,
            self.measDef.interval,
            self.measDef.movingWindow,
            simpleMeasurements,
        )

    def getCpxValues(self, startTime, endTime, interval, movingWindow, measurements):
        cpxValues = []
        endTime = endTime - timedelta(seconds=movingWindow)
        for timePoint in timePoints(startTime, endTime, interval):
            print(timePoint)
            windowStartTime = timePoint
            windowEndTime = timePoint + timedelta(seconds=movingWindow)
            simpleValues = self.getSimpleValues(
                windowStartTime, windowEndTime, measurements
            )
            complexValue = self.calcCpx(simpleValues)
            cpxValues.append(
                [complexValue, timePoint + timedelta(seconds=movingWindow)]
            )
        return cpxValues

    def getSimpleValues(self, startTime, endTime, measurements):
        return list(filter(lambda x: startTime < x[1] < endTime, measurements))

    def calcCpx(self, simpleMeasurements):
        if len(simpleMeasurements) == 0:
            return 0.0
        totalSum = 0.0
        for simpleMeas in simpleMeasurements:
            totalSum += simpleMeas[0]
        cpx = totalSum / len(simpleMeasurements)
        return cpx
