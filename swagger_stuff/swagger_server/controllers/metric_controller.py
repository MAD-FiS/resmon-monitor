import connexion
import six

from swagger_server.models.dummy import Dummy  # noqa: E501
from swagger_server import util


def delete_metric(metric_id):  # noqa: E501
    """Delete complex metric

     # noqa: E501

    :param metric_id: 
    :type metric_id: int

    :rtype: None
    """
    return 'do some magic!'


def post_metric(dummy=None):  # noqa: E501
    """Add complex metric

     # noqa: E501

    :param dummy: 
    :type dummy: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        dummy = Dummy.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
