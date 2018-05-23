#!/usr/bin/env python3

from mongoAccess import mongo3

class dbApi:
    '''Wrapper for mongoDB basic access. Used to provide higher level api.'''

    DATA_COLL="dataCollection"
    META_COLL="metaCollection"
    META2_COLL="meta2Collection"
    NAME="monitorDatabase"
    IP='172.17.0.2'
    PORT='27017'
    USER=''
    PASSW=''

    def __init__(self):
        self.db = mongo3.DB(self.USER, self.PASSW, self.IP, self.PORT, self.NAME)

    DATA_KEY="DATA"
    SESSION_KEY="SESSION_ID"
    TIME_KEY="DATE"
    SESSION_PATH=DATA_KEY+'.'+SESSION_KEY
    FROM="$gt"
    TO="$lt"
    TYPE_KEY="TYPE"

    def findInMeta(self, filtr):
        #filtr["TYPE"]="META"
        return self.db.find(filtr, META_COLL) 

    def findInMeta2(self, filtr):
        #filtr["TYPE"]="META2"
        return self.db.find(filtr, META2_COLL) 
    
    def findData(self, filtr):
        #filtr["TYPE"]="DATA"
        return self.db.find(filtr, DATA_COLL)

    def getSessionIds(self, dataFilter=None):
        sessionIds = []

        #metaEntries = self.db.find({"TYPE":"META"}, META_COLL);
        metaEntries = findInMeta2(dataFilter)
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
