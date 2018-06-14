#!/usr/bin/env python3

import re
import json
from datetime import datetime
from mongoAccess import mongo3


class dbApi:
    """Wrapper for mongoDB basic access. Used to provide higher level api."""

    DATA_COLL = "dataCollection"
    META_COLL = "metaCollection"
    COMPLEX_COLL = "complexMeasurements"
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
    PARENT_ID_KEY = "parent_id"
    MOVING_WINDOW_KEY = "moving_window"
    INTERVAL_KEY = "interval"
    LAST_CALC_KEY = "last_calculation"
    DESCRIPTION_KEY = "description"
    UNIT_KEY = "unit"

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
        """Find filter in meta collection"""
        return self.db.find(filtr, self.META_COLL)

    def findData(self, filtr):
        """Find in data collection using filter"""
        return self.db.find(filtr, self.DATA_COLL)

    def getSessionIds(self, dataFilter=None):
        """Get session id from meta using filter"""
        if dataFilter:
            metaEntries = self.findInMeta(dataFilter)
            return [entry[self.SESSION_KEY] for entry in metaEntries]
        else:
            metaEntries = self.findInMeta()
            return [entry[self.SESSION_KEY] for entry in metaEntries]

    def getMetrics(self, sessionId, metricMatcher=None):
        """ Get metrics from meta collection using session id"""
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
        """Get measurements from data collection precisize by session id,
         metric name and time interval"""
        dataEntries = self.db.find(
            {
                self.SESSION_KEY: sessionId,
                self.TIME_KEY: {self.FROM: startTime, self.TO: endTime},
            },
            self.DATA_COLL,
        )
        values = [
            [v[metricName], v[self.TIME_KEY]]
            for v in dataEntries
            if metricName in v
        ]
        return values

    def getAll(self):
        """Get all record from database"""
        return self.db.select(self.DATA_COLL)

    def getAllMetrics(self):
        """Get all metrics from meta collection"""
        dataEntries = self.findInMeta()
        response = {}
        for entry in dataEntries:
            for metric in entry[self.METRICS_KEY]:
                response.update(
                    {metric[self.METRIC_ID_KEY]: metric[self.DESCRIPTION_KEY]}
                )

        return response

    def getHostname(self, sessionId):
        """Get name of host specified by session id"""
        return self.findInMeta({self.SESSION_KEY: sessionId})[0][
            self.HOSTNAME_KEY
        ]


    def getHostnameByMetric(self, metric):
        """Get name of host specified by metric"""
        dataEntries = self.findInMeta()
        hostnames = []
        entries = {}
        for entry in dataEntries:
            for met in entry[self.METRICS_KEY]:
                if met[self.METRIC_ID_KEY] == metric:
                    hostnames.append(entry[self.HOSTNAME_KEY])

        return list(set(hostnames))

    def getHosts(self, query):
        """Get list of hosts from meta collection using query"""
        dataEntries = self.findInMeta()
        hostnames = []
        for entry in dataEntries:
            hostnames.append(entry[self.HOSTNAME_KEY])
        return list(set(hostnames))

    def getMetadataByHost(self, host):
        """Get metadata from meta colleciton specified by host"""
        metadata = list()
        metaEntries = self.findInMeta({self.HOSTNAME_KEY: host})
        for entry in metaEntries:
            for key in entry.keys():
                if key not in self.STANDARD_FIELDS:
                    metadata.append(
                        {"id": key, "name": key, "value": entry[key]}
                    )
        return metadata

    def getCpxDefinitions(self):
        return self.db.find(None, self.COMPLEX_COLL)

    # TODO:Delete all this ugly arguments and
    # replace with MeasurementDefinition object
    def insertMeasDefinition(
        self,
        hostname,
        metric_id,
        parent_id,
        moving_window,
        interval,
        description,
    ):
        doc = dict()
        doc[self.HOSTNAME_KEY] = hostname
        doc[self.METRIC_ID_KEY] = metric_id
        doc[self.PARENT_ID_KEY] = parent_id
        doc[self.MOVING_WINDOW_KEY] = moving_window
        doc[self.INTERVAL_KEY] = interval
        doc[self.DESCRIPTION_KEY] = description
        doc[self.LAST_CALC_KEY] = datetime.now()
        self.db.insert(doc, self.COMPLEX_COLL)

    def updateMetricInMetadata(
        self, hostname, metric_id, parent_id, description
    ):
        record = self.findInMeta(
            {self.HOSTNAME_KEY: hostname, self.METRIC_PATH: parent_id}
        )
        metrics = record[0][self.METRICS_KEY]
        unit = ""
        for metric in metrics:
            if metric[self.METRIC_ID_KEY] == parent_id:
                unit = metric[self.UNIT_KEY]

        metricRecord = dict()
        metricRecord[self.DESCRIPTION_KEY] = description
        metricRecord[self.METRIC_ID_KEY] = metric_id
        metricRecord[self.UNIT_KEY] = unit

        metrics.append(metricRecord)

        self.db.update(
            {self.HOSTNAME_KEY: hostname, self.METRIC_PATH: parent_id},
            {self.METRICS_KEY: metrics},
            self.META_COLL,
        )

    # TODO:Delete all this ugly arguments and
    # replace with MeasurementDefinition object
    def updateMeasDefinition(
        self,
        hostname,
        metric_id,
        parent_id,
        moving_window,
        interval,
        description,
        lastCalcTime,
    ):
        doc = dict()
        doc[self.HOSTNAME_KEY] = hostname
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
