import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.measurement import Measurement  # noqa: E501
from swagger_server.models.value import Value  # noqa: E501
from swagger_server import util

from mongoAccess import mongo3


def get_measurements():  # noqa: E501
    db = mongo3.DB('', '', '172.17.0.2', 27017, "test", "myCollection")
    dbContent = db.select() 

    """Get measurements from all hosts

     # noqa: E501

    :rtype: List[InlineResponse200]
    """
    return str(dbContent)


def get_measurements_host(hostname):  # noqa: E501
    """Get measurements from particular host

     # noqa: E501

    :param hostname: 
    :type hostname: str

    :rtype: List[Measurement]
    """
    return 'do some magic!'


def get_measurements_host_metric(hostname, metric_id):  # noqa: E501
    """Get measurements from particular host of particular metric

     # noqa: E501

    :param hostname: 
    :type hostname: str
    :param metric_id: 
    :type metric_id: str

    :rtype: List[Value]
    """
    return 'do some magic!'
