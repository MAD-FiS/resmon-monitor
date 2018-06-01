#!/usr/bin/env python3

import re
from mongoAccess import mongo3

# import mongo3


class dbApi:
    """Wrapper for mongoDB basic access. Used to provide higher level api."""

    DATA_COLL = "dataCollection"
    META_COLL = "metaCollection"
    META2_COLL = "meta2Collection"
    NAME = "monitorDatabase"
    IP = "172.17.0.2"
    PORT = 27017
    USER = ""
    PASSW = ""

    def __init__(self):
        self.db = mongo3.DB(self.USER, self.PASSW, self.IP, self.PORT, self.NAME)

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
        # TODO: delete once query metric_id is consitent with database metric_id
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
        values = [[v[metricName], str(v[self.TIME_KEY])] for v in dataEntries]
        return values

    def getAll(self):
        return self.db.select(self.DATA_COLL)

    def getAllMetrics(self):
        dataEntries = self.db.find({self.TYPE_KEY: "META"}, self.META_COLL)
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

    def getHostname(self, sessionId):
        return self.findInMeta2({self.SESSION_KEY: sessionId})[0][self.NAME_KEY]

    def getHostnameByMetric(self, metric):
        dataEntries = self.db.find({self.TYPE_KEY: "META"}, self.META_COLL)
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

    def getHosts(self, query):
        dataEntries = self.db.find({self.TYPE_KEY: "META"}, self.META_COLL)
        hostnames = []
        expression = re.compile(".*" + query + ".*")
        for entry in dataEntries:
            for value in entry["DATA"]:
                if value["TAG"] == "NAME" and expression.match(value["DATA"]):
                    hostnames.append(value["DATA"])

        return list(set(hostnames))

    def getMetadataByHost(self, host):
        metadata = list()
        metaEntries = self.findInMeta2({self.NAME_KEY: host})
        for entry in metaEntries:
            for key in entry.keys():
                if not key in self.STANDARD_FIELDS:
                    metadata.append({"id": key, "name": key, "value": entry[key]})

        return metadata