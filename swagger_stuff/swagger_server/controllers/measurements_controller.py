import connexion
import six

from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2001_metricid import InlineResponse2001METRICID  # noqa: E501
from swagger_server.models.measurement import Measurement
from swagger_server.models.point import Point


from swagger_server import util

from mongoAccess import dbApi
from apiUtils import QueryResolver


def get_measurements(start, end=None, q=None):  # noqa: E501
    """Selected measurements

     # noqa: E501

    :param start: ISO 8601 datetime format with 1s accuracy.
    :type start: str
    :param end: ISO 8601 datetime format with 1s accuracy. Default value is current time.
    :type end: str
    :param q: Filters out used metrics and hosts according to provided keys. String needs to match the following schema: &#x60;KEY1:VAL1,KEY2:VAL2;KEY3:VAL4...&#x60;. Comma is used to indicate &#x60;AND&#x60; operation while semicolon relates to &#x60;OR&#x60;. When &#x60;VAL&#x60; paramater is wrapped into slashes then regex mode is activated. For example when we query for &#x60;metric_id:cpu,os:/.*nix.*/;metric_id:cpu,os:/.*win.*/&#x60; we should receive cpu metric measurements for hosts containing either nix or win as substring in &#x60;os&#x60; metadata. Note that &#x60;AND&#x60; operation has higher priority than &#x60;OR&#x60;. Allowed keys: &#x60;metric_id&#x60;, &#x60;description&#x60;, &#x60;complex&#x60; (metric parameters) and all available host metadata fields.
    :type q: str

    :rtype: InlineResponse2001
    """
    start = util.deserialize_datetime(start)
    end = util.deserialize_datetime(end)

    api = dbApi.dbApi()
    resolver = QueryResolver.QueryResolver(q)

    for filt in resolver.getFilters():
        metaFilter = filt[0]
        metric = filt[1]
        sessionIds = api.getSessionIds(metaFilter)
        for sessionId in sessionIds:
            dataPoints = api.getMeasurements(sessionId, metric, start, end)
            points = [Point(m[1], m[0]) for m in dataPoints]
            measurement = Measurement(metric, sessionId, points)
            inlineResponse = InlineResponse2001METRICID(measurement)
            inlineResponse2001 = InlineResponse2001(inlineResponse)

            return inlineResponse2001
