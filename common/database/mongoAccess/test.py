import dbApi
import datetime
import mongo3

#db = mongo3.DB('', '', '172.17.0.2', 27017, "test", "myCollection")
#result = db.find({"TYPE":"META"})
#for metaEntries in result:
#    for entry in metaEntries["DATA"]:
#        if entry["TAG"] == "SESSION_ID":
#            print(entry["DATA"])

#meas = api.getMeasurements("7a387076627b691cba4f7f54b255f70bef0aea68", "RAM_USAGE", datetime.datetime(2018,5,16,13,10,26), datetime.datetime(2018,5,16,13,30,26))
#print(list(meas))

api = dbApi.dbApi()
sessionIds = api.getSessionIds()
print(sessionIds)
