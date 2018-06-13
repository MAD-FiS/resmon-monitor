import connexion
import six
import datetime

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.measurement import Measurement  # noqa: E501
from swagger_server.models.point import Point
from swagger_server import util

from mongoAccess import dbApi
from apiUtils import QueryResolver

TIME_IND = 0
VALUE_IND = 1


def get_measurements(start=None, end=None, q=None, limit=None, last=None):  # noqa: E501
    """Selected measurements

     # noqa: E501

    :param start: ISO 8601 datetime format with 1s accuracy. Default value is current time subtracted by 1 day
    :type start: str
    :param end: ISO 8601 datetime format with 1s accuracy. Default value is current time.
    :type end: str
    :param q: Filters out used metrics and hosts according to provided keys. String needs to match the following schema: &#x60;KEY1:VAL1,KEY2:VAL2;KEY3:VAL4...&#x60;. Comma is used to indicate &#x60;AND&#x60; operation while semicolon relates to &#x60;OR&#x60;. When &#x60;VAL&#x60; paramater is wrapped into slashes then regex mode is activated. For example when we query for &#x60;metric_id:cpu,os:/.*nix.*/;metric_id:cpu,os:/.*win.*/&#x60; we should receive cpu metric measurements for hosts containing either nix or win as substring in &#x60;os&#x60; metadata. Note that &#x60;AND&#x60; operation has higher priority than &#x60;OR&#x60;. Allowed keys: &#x60;metric_id&#x60;, &#x60;description&#x60;, &#x60;complex&#x60; (metric parameters) and all available host metadata fields. When not provided: No filtering performed - all available metrics and hosts are taken
    :type q: str
    :param limit: Number of maximal amount of measurements given as a result of the query
    :type limit: 
    :param last: If it is set as &#x60;TRUE&#x60; then the only last measurement meeting the criteria from &#x60;q&#x60; parameter is returned
    :type last: bool

    :rtype: List[Measurement]
    """
    api = dbApi.dbApi()

    if not end:
        end = datetime.datetime.now()
    else:
        end = util.deserialize_datetime(end)

    if not start:
        start = datetime.datetime.now() - datetime.timedelta(days=1)
    else:
        start = util.deserialize_datetime(start)

    filters = []
    if not q:
        filters.append(None)
    else:
        resolver = QueryResolver.QueryResolver(q)
        if resolver.validateQuery() == 0:
            return "Bad request", 400
        else:
            filters = resolver.getFilters()

    print("start: " + str(start))
    print("end: " + str(end))
    print("q: " + str(q))

    measurements = []
    for metaFilter in filters:
        print("metaFilter: " + str(metaFilter))
        for sessionId in api.getSessionIds(metaFilter):
            print("sessionId: " + str(sessionId))
            metrics = list()

            if metaFilter and "metric_id" in metaFilter:
                metricFilter = metaFilter["metric_id"]
                print("Metrics filtering with filter: " + str(metricFilter))
                metrics = api.getMetrics(sessionId, metricFilter)
            else:
                print("No metrics filtering, take all metrics")
                metrics = api.getMetrics(sessionId)

            for metric in metrics:
                print(sessionId)
                print(metric)
                print(start)
                print(end)
                dataPoints = api.getMeasurements(sessionId, metric, start, end)
                points = [Point(point[VALUE_IND],
                          point[TIME_IND]) for point in dataPoints]

                measurement = Measurement(metric, api.getHostname(sessionId),
                                          points)
                measurements.append(measurement.to_dict())

    return measurements
