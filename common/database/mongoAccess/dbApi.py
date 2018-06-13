#!/usr/bin/env python3

import re
import json
from mongoAccess import mongo3

# import mongo3


class dbApi:
    """Wrapper for mongoDB basic access. Used to provide higher level api."""

    DATA_COLL = "dataCollection"
    META_COLL = "metaCollection"
    NAME = "monitorDatabase"
    IP = "172.17.0.2"
    PORT = 27017
    USER = ""
    PASSW = ""

    def __init__(self):
        self.db = mongo3.DB(
            self.USER, self.PASSW, self.IP, self.PORT, self.NAME
        )

    DATA_KEY = "data"
    SESSION_KEY = "session_id"
    TIME_KEY = "date"
    SESSION_PATH = DATA_KEY + "." + SESSION_KEY
    FROM = "$gt"
    TO = "$lt"
    TYPE_KEY = "type"
    METRICS_KEY = "metrics"
    METRIC_ID_KEY = "metric_id"
    METRIC_PATH = METRICS_KEY + "." + METRIC_ID_KEY
    METRIC_QUERY_KEY = "metric_id"
    HOSTNAME_KEY = "hostname"
    DESCRIPTION_KEY = "description"

    STANDARD_FIELDS = [
        "metrics",
        "session_id",
        "meta_descriptions",
        "hostname",
        "session_start_date",
        "descriptions",
        "_id",
    ]

    def findInMeta(self, filtr=None):
        return self.db.find(filtr, self.META_COLL)

    def findData(self, filtr):
        return self.db.find(filtr, self.DATA_COLL)

    def getSessionIds(self, dataFilter=None):
        if dataFilter:
            metaEntries = self.findInMeta(dataFilter)
            return [entry[self.SESSION_KEY] for entry in metaEntries]
        else:
            metaEntries = self.findInMeta()
            return [entry[self.SESSION_KEY] for entry in metaEntries]

    def getMetrics(self, sessionId, metricMatcher=None):
        records = self.findInMeta({self.SESSION_KEY: sessionId})
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
        dataEntries = self.findInMeta()
        response = {}
        for entry in dataEntries:
            for metric in entry[self.METRICS_KEY]:
                response.update(
                    {metric[self.METRIC_ID_KEY]: metric[self.DESCRIPTION_KEY]}
                )

        return response

    def getHostname(self, sessionId):
        return self.findInMeta({self.SESSION_KEY: sessionId})[0][
            self.HOSTNAME_KEY
        ]

    def getHostnameByMetric(self, metric):
        dataEntries = self.findInMeta()
        hostnames = []
        entries = {}
        for entry in dataEntries:
            for met in entry[self.METRICS_KEY]:
                if met[self.METRIC_ID_KEY] == metric:
                    hostnames.append(entry[self.HOSTNAME_KEY])

        return list(set(hostnames))

    def getHosts(self, query):
        dataEntries = self.findInMeta()
        hostnames = []
        for entry in dataEntries:
            hostnames.append(entry[self.HOSTNAME_KEY])
        return list(set(hostnames))

    def getMetadataByHost(self, host):
        metadata = list()
        metaEntries = self.findInMeta({self.HOSTNAME_KEY: host})
        for entry in metaEntries:
            for key in entry.keys():
                if key not in self.STANDARD_FIELDS:
                    metadata.append(
                        {"id": key, "name": key, "value": entry[key]}
                    )

        return metadata
