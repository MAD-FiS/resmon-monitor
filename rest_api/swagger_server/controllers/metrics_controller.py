import connexion
import six
import json

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.metric import Metric  # noqa: E501
from swagger_server import util
from flask_jwt_extended import jwt_required
from mongoAccess import dbApi

@jwt_required
def get_metrics():  # noqa: E501
    """List of metrics

     # noqa: E501


    :rtype: List[Metric]
    """

    api = dbApi.dbApi()
    metrics = api.getAllMetrics()
    response = []

    for metric in metrics.keys():
        interval = None
        moving_window = None
        hosts = api.getHostnameByMetric(metric)

        cpxDefinitions = api.getCpxDefinitions({api.METRIC_ID_KEY: metric})
        for cpxDef in cpxDefinitions:
            hosts.append(cpxDef[api.HOSTNAME_KEY])
            interval = cpxDef[api.INTERVAL_KEY]
            moving_window = cpxDef[api.MOVING_WINDOW_KEY]

        metric_object = Metric(
            id=metric,
            interval=interval,
            moving_window_duration=moving_window,
            description=metrics[metric],
            unit="%",
            hosts=hosts,
        )
        response.append(metric_object.to_dict())

    return response
