from common.database.mongoAccess.dbApi import dbApi
import datetime

if __name__ == '__main__':
    api = dbApi.dbApi()

    meas = api.getMeasurements(
            "349e126d3d13489dd3e797580195b3684f15779e", "RAM_USAGE",
            datetime.datetime(2010, 5, 10, 00, 00, 00),
            datetime.datetime(2018, 5, 23, 14, 8, 18))
    print(list(meas))

    sessionIds = api.getSessionIds()
    print(sessionIds)
