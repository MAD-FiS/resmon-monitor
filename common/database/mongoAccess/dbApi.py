#!/usr/bin/env python3

import re
import json
from datetime import datetime
from mongoAccess import mongo3


class dbApi:
    """Wrapper for mongoDB basic access. Used to provide higher level api."""

    DATA_COLL = "dataCollection"
    META_COLL = "metaCollection"
    META2_COLL = "meta2Collection"
    COMPLEX_COLL = "complexMeasurements"
    NAME = "monitorDatabase"
    IP = "172.17.0.2"
    PORT = 27017
    USER = ""
    PASSW = ""

    def __init__(self):
        self.db = mongo3.DB(self.USER, self.PASSW,
                            self.IP, self.PORT, self.NAME)

    DATA_KEY = "DATA"
    SESSION_KEY = "SESSION_ID"
    TIME_KEY = "DATE"
    SESSION_PATH = DATA_KEY + "." + SESSION_KEY
    FROM = "$gt"
    TO = "$lt"
    TYPE_KEY = "TYPE"
    METRICS_KEY = "AVAILABLE_FIELDS"
    METRIC_ID_KEY = "TAG"
    METRIC_PATH = METRICS_KEY + "." + METRIC_ID_KEY
    METRIC_QUERY_KEY = "metric_id"
    NAME_KEY = "NAME"
    PARENT_ID_KEY = "PARENT_ID"
    MOVING_WINDOW_KEY = "WINDOW_WIDTH"
    INTERVAL_KEY = "INTERVAL"
    LAST_CALC_KEY = "LAST_CALCULATION"
    DESCRIPTION_KEY = "DESCRIPTION"

    STANDARD_FIELDS = [
        "METRICS",
        "SESSION_ID",
        "NAME",
        "AVAILABLE_FIELDS",
        "SESSION_START_DATE",
        "DESCRIPTIONS",
        "_id",
    ]

    def findInMeta(self, filtr):
        return self.db.find(filtr, self.META_COLL)

    def findInMeta2(self, filtr=None):
        return self.db.find(filtr, self.META2_COLL)

    def findData(self, filtr):
        return self.db.find(filtr, self.DATA_COLL)

    def getSessionIds(self, dataFilter=None):
        # TODO: delete once query metric_id
        #       is consitent with database metric_id
        if dataFilter:
            dbFilter = dataFilter.copy()
            if self.METRIC_QUERY_KEY in dbFilter:
                dbFilter[self.METRIC_PATH] = dbFilter[self.METRIC_QUERY_KEY]
                del dbFilter[self.METRIC_QUERY_KEY]

            metaEntries = self.findInMeta2(dbFilter)
            return [entry[self.SESSION_KEY] for entry in metaEntries]
        else:
            metaEntries = self.findInMeta2()
            return [entry[self.SESSION_KEY] for entry in metaEntries]

    def getMetrics(self, sessionId, metricMatcher=None):
        records = self.findInMeta2({self.SESSION_KEY: sessionId})
        metrics = [record[self.METRICS_KEY] for record in records][0]
        print(metrics)

        if not metricMatcher:
            return [metric[self.METRIC_ID_KEY] for metric in metrics]
        else:
            if isinstance(metricMatcher, re._pattern_type):
                matchedMetrics = list()

                for metric in metrics:
                    metricId = metric[self.METRIC_ID_KEY]
                    if metricMatcher.match(metricId):
                        matchedMetrics.append(metricId)

                return matchedMetrics
            else:
                return [metricMatcher]

    def getMeasurements(self, sessionId, metricName, startTime, endTime):
        dataEntries = self.db.find(
            {
                self.SESSION_KEY: sessionId,
                self.TIME_KEY: {self.FROM: startTime, self.TO: endTime},
            },
            self.DATA_COLL,
        )
        values = [[v[metricName], v[self.TIME_KEY]] for v in dataEntries if metricName in v]
        return values

    def getAll(self):
        return self.db.select(self.DATA_COLL)

    def getAllMetrics(self):
        dataEntries = self.db.find(None, self.META2_COLL)
        response = {}
        for entry in dataEntries:
            for metric in entry["AVAILABLE_FIELDS"]:
                response.update({metric["TAG"]: metric["DESCRIPTION"]})

        return response

    def getHostname(self, sessionId):
        return self.findInMeta2(
            {self.SESSION_KEY: sessionId})[0][self.NAME_KEY]

    def getHostnameByMetric(self, metric):
        dataEntries = self.db.find(None, self.META2_COLL)
        hostnames = []
        entries = {}
        for entry in dataEntries:
            for met in entry["AVAILABLE_FIELDS"]:
                if met["TAG"] == metric:
                    hostnames.append(entry["NAME"])

        return list(set(hostnames))

    def getHosts(self, query):
        dataEntries = self.db.find(None, self.META2_COLL)
        hostnames = []
        expression = re.compile(".*" + query + ".*")
        for entry in dataEntries:
            if expression.match(entry["NAME"]):
                hostnames.append(entry["NAME"])

        return list(set(hostnames))

    def getMetadataByHost(self, host):
        metadata = list()
        metaEntries = self.findInMeta2({self.NAME_KEY: host})
        for entry in metaEntries:
            for key in entry.keys():
                if key not in self.STANDARD_FIELDS:
                    metadata.append({"id": key,
                                     "name": key,
                                     "value": entry[key]})
        return metadata

    def getCpxDefinitions(self):
        return self.db.find(None, self.COMPLEX_COLL)

    #TODO:Delete all this ugly arguments and replace with MeasurementDefinition object
    def insertMeasDefinition(self, hostname, metric_id, parent_id, moving_window, interval, description):
        doc = dict()
        doc[self.NAME_KEY] = hostname
        doc[self.METRIC_ID_KEY] = metric_id
        doc[self.PARENT_ID_KEY] = parent_id
        doc[self.MOVING_WINDOW_KEY] = moving_window
        doc[self.INTERVAL_KEY] = interval
        doc[self.DESCRIPTION_KEY] = description
        doc[self.LAST_CALC_KEY] = datetime.now()
        self.db.insert(doc, self.COMPLEX_COLL)

    #TODO:Delete all this ugly arguments and replace with MeasurementDefinition object
    def updateMeasDefinition(self, hostname, metric_id, parent_id, moving_window, interval, description, lastCalcTime):
        doc = dict()
        doc[self.NAME_KEY] = hostname
        doc[self.METRIC_ID_KEY] = metric_id

        updateFilter = doc.copy()

        doc[self.PARENT_ID_KEY] = parent_id
        doc[self.MOVING_WINDOW_KEY] = moving_window
        doc[self.INTERVAL_KEY] = interval
        doc[self.DESCRIPTION_KEY] = description
        doc[self.LAST_CALC_KEY] = lastCalcTime
        
        self.db.update(updateFilter, doc, self.COMPLEX_COLL)
        
    def insertMeasurements(self, sessionId, metric_id, measurements):
        measurementsEntries = list()

        for measurement in measurements:
            dbEntry = {}
            dbEntry[self.SESSION_KEY] = sessionId
            dbEntry[metric_id] = measurement[0]
            dbEntry[self.TIME_KEY] = measurement[1]
            measurementsEntries.append(dbEntry)

        self.db.insert(measurementsEntries, self.DATA_COLL)
