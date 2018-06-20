from common.database.mongoAccess import dbApi


class MeasurementDef:
    def __init__(
        self,
        hostname,
        metric_id,
        parent_id,
        movingWindow,
        interval,
        lastCalc,
        description,
        owner,
    ):
        self.hostname = hostname
        self.metric_id = metric_id
        self.parent_id = parent_id
        self.movingWindow = movingWindow
        self.interval = interval
        self.lastCalcTime = lastCalc
        self.description = description
        self.owner = owner

    def getFilter(self):
        measFilter = dict()
        measFilter[dbApi.dbApi.HOSTNAME_KEY] = self.hostname
        measFilter[dbApi.dbApi.METRIC_PATH] = self.parent_id
        return measFilter

    @classmethod
    def fromDict(cls, cpx):
        hostname = cpx[dbApi.dbApi.HOSTNAME_KEY]
        metric_id = cpx[dbApi.dbApi.METRIC_ID_KEY]
        parent_id = cpx[dbApi.dbApi.PARENT_ID_KEY]
        movingWindow = cpx[dbApi.dbApi.MOVING_WINDOW_KEY]
        interval = cpx[dbApi.dbApi.INTERVAL_KEY]
        lastCalcTime = cpx[dbApi.dbApi.LAST_CALC_KEY]
        description = cpx[dbApi.dbApi.DESCRIPTION_KEY]
        owner = "-"
        if dbApi.dbApi.OWNER_KEY in cpx:
            owner = cpx[dbApi.dbApi.OWNER_KEY]

        return cls(
            hostname,
            metric_id,
            parent_id,
            movingWindow,
            interval,
            lastCalcTime,
            description,
            owner,
        )
