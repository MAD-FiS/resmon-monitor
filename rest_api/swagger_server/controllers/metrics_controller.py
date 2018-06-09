import connexion
import six
import json

from swagger_server.models.metric import Metric  # noqa: E501
from swagger_server import util

from mongoAccess import dbApi


def get_metrics():  # noqa: E501
    """List of metrics

     # noqa: E501


    :rtype: List[Metric]
    """

    api = dbApi.dbApi()
    metrics = api.getAllMetrics()
    response = []

    for metric in metrics.keys():
        hosts = api.getHostnameByMetric(metric)
        metric_object = Metric(id = metric, description = metrics[metric],
                               unit = "%", hosts = hosts)
        response.append(metric_object.to_dict())

    return response
