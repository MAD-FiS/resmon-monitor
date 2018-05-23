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
    metrics, descriptions = api.getAllMetrics()
    response = []
    for metric in metrics:
        hosts = api.getHostnameByMetric(metric)
        metric_object = Metric(id = metric, description = descriptions[metric], parent_id = "null", unit = "%", hosts = hosts)
        response.append(metric_object.to_dict())

    return response
