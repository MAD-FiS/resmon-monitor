import connexion
import six

from swagger_server.models.metric_list import MetricList  # noqa: E501
from swagger_server import util


def get_metrics():  # noqa: E501
    """Get available metrics

     # noqa: E501


    :rtype: List[MetricList]
    """
    return 'do some magic!'
