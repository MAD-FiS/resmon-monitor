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
    responses = []
    for metric in metrics:
        response = {}
        hosts = api.getHostnameByMetric(metric)
        response["id"] = metric
        response["DESCRIPTION"] = descriptions[metric]
        response["hosts"] = hosts
        #Removable field should be changed when authorization will be implemented
        response["removable"] = "true"
        response["unit"] = "%"
        responses.append(response)

    return responses
