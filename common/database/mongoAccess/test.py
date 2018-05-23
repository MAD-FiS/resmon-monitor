import dbApi
import datetime
import mongo3

api = dbApi.dbApi()

#db = mongo3.DB('', '', '172.17.0.2', 27017, "test", "myCollection")
#result = db.find({"TYPE":"META"})
#for metaEntries in result:
#    for entry in metaEntries["DATA"]:
#        if entry["TAG"] == "SESSION_ID":
#            print(entry["DATA"])

meas = api.getMeasurements("349e126d3d13489dd3e797580195b3684f15779e", "RAM_USAGE", datetime.datetime(2010,5,10,00,00,00), datetime.datetime(2018,5,23,14,8,18))
print(list(meas))

sessionIds = api.getSessionIds()
print(sessionIds)
