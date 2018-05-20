#!/usr/bin/env python3

from mongoAccess import mongo3

class dbApi:
    '''Wrapper for mongoDB basic access. Used to provide higher level api.'''
    def __init__(self):
        self.db = mongo3.DB('', '', '172.17.0.2', 27017, "test", "myCollection")

    DATA_KEY="DATA"
    SESSION_KEY="SESSION_ID"
    TIME_KEY="DATE"
    SESSION_PATH=DATA_KEY+'.'+SESSION_KEY
    FROM="$gt"
    TO="$lt"
    TYPE_KEY="TYPE"

    def getSessionIds(self, dataFilter=None):
        sessionIds = []

        metaEntries = self.db.find({"TYPE":"META"});
        for meta in metaEntries:
            for entry in meta["DATA"]:
                if entry["TAG"] == "SESSION_ID":
                    sessionIds.append(entry["DATA"])

        return sessionIds

    def getMeasurements(self, sessionId, metricName, startTime, endTime):
        dataEntries = self.db.find({self.SESSION_KEY:sessionId, self.TIME_KEY:{self.FROM:startTime, self.TO:endTime}})
        values = [[v[metricName], str(v[self.TIME_KEY])] for v in dataEntries]
        return values

    def getAll(self):
        return self.db.select()

    def getAllMetrics(self):
        dataEntries = self.db.find({self.TYPE_KEY : "META"})
        entries = {}
        metrics = []
        descriptions = {}
        for entry in dataEntries:
            for value in entry["DATA"]:
                if value["TAG"] == "AVAILABLE_FIELDS":
                    for metric in value:
                        entries[metric] = value[metric]
            for metric in entries["DATA"]:
                if metric["TAG"] == "DATE" or metric["TAG"] == "SESSION_ID":
                    continue
                metrics.append(metric["TAG"])
                descriptions[metric["TAG"]] = metric["DESCRIPTION"]

        return set(metrics), descriptions

    def getHostnameByMetric(self, metric):
        dataEntries = self.db.find({self.TYPE_KEY : "META"})
        hostnames = []
        entries = {}
        for entry in dataEntries:
            for value in entry["DATA"]:
                if value["TAG"] == "NAME":
                    hostname = value["DATA"]
                if value["TAG"] == "AVAILABLE_FIELDS":
                    for met in value:
                        entries[met] = value[met]
            for met in entries["DATA"]:
                if met["TAG"] == metric:
                    hostnames.append(hostname)

        return list(set(hostnames))


