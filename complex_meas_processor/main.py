#!/usr/bin/env python3
from mongoAccess import dbApi
from datetime import datetime
from datetime import timedelta
from CpxCalculator import CpxCalculator
from MeasurementDef import MeasurementDef

import time


def timePoints(startTime, endTime, interval):
    intervals = int((endTime - startTime).total_seconds()/interval) + 1
    return (startTime + timedelta(seconds=(interval*x)) for x in range(intervals))

def run():
    api = dbApi.dbApi()
    while True:
        print("Calculating complex measurements, time: ", datetime.now())
        complexEntries = api.getCpxDefinitions()
        measDefs = [MeasurementDef.fromDict(v) for v in complexEntries]
        for measDef in measDefs:
            cpxCalculator = CpxCalculator(measDef)
            sessionIds = api.getSessionIds(measDef.getFilter())
            nowTime = datetime.now()
            for sessionId in sessionIds:
                simpleMeasurements = api.getMeasurements(
                    sessionId, measDef.parent_id, measDef.lastCalcTime, nowTime
                )
                cpxValues = cpxCalculator.calculate(simpleMeasurements, nowTime)
                print(sessionId, measDef.metric_id, cpxValues)
                api.insertMeasurements(sessionId, measDef.metric_id, cpxValues)
            measDef.lastCalcTime = nowTime
            api.updateMeasDefinition(measDef.hostname, measDef.metric_id, measDef.parent_id, measDef.movingWindow, measDef.interval, measDef.description, measDef.lastCalcTime)
        time.sleep(60)


if __name__ == "__main__":
    run()
