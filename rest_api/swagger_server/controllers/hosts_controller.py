import connexion
import six
import json

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.host import Host  # noqa: E501
from swagger_server.models.host import Metric  # noqa: E501
from swagger_server.models.host import Metadata  # noqa: E501
from swagger_server.models.payload import Payload  # noqa: E501
from swagger_server import util

from mongoAccess import dbApi
from .metrics_controller import get_metrics


def delete_metric(metric_id, hostname):  # noqa: E501
    """Delete complex metric

     # noqa: E501

    :param metric_id: Metric identyfier. It has the same form as &#x60;metric_id&#x60; field of &#x60;Metric&#x60; model
    :type metric_id: str
    :param hostname: Target host (domain name)
    :type hostname: str

    :rtype: object
    """
    return 'do some magic!'


def get_hosts(q=None):  # noqa: E501
    """Get list of hosts

     # noqa: E501

    :param q: Filters out used metrics and hosts according to provided keys. String needs to match the following schema: &#x60;KEY1:VAL1,KEY2:VAL2;KEY3:VAL4...&#x60;. Comma is used to indicate &#x60;AND&#x60; operation while semicolon relates to &#x60;OR&#x60;. When &#x60;VAL&#x60; paramater is wrapped into slashes then regex mode is activated. For example when we query for &#x60;metric_id:cpu,os:/.*nix.*/;metric_id:cpu,os:/.*win.*/&#x60; we should receive cpu metric measurements for hosts containing either nix or win as substring in &#x60;os&#x60; metadata. Note that &#x60;AND&#x60; operation has higher priority than &#x60;OR&#x60;. Allowed keys: &#x60;metric_id&#x60;, &#x60;description&#x60;, &#x60;complex&#x60; (metric parameters) and all available host metadata fields. When not provided: No filtering performed - all available metrics and hosts are taken
    :type q: str

    :rtype: List[Host]
    """

    api = dbApi.dbApi()
    if q:
        hosts = api.getHosts(query=q)
    else:
        hosts = api.getHosts(query="")

    response = []
    for host in hosts:
        metrics = get_metrics()
        metric_objects = []
        for metric in metrics:
            metric_objects.append(Metric.from_dict(metric))
        metrics = []
        metrics = [m for m in metric_objects if host in m.hosts]
        metadatas = [Metadata.from_dict(metadata)
                     for metadata in api.getMetadataByHost(host)]
        response.append((Host(hostname=host,
                              metrics=metrics, metadata=metadatas)).to_dict())

    return response


def post_metric(hostname, payload):  # noqa: E501
    """Add complex metric

     # noqa: E501

    :param hostname: Target host (domain name)
    :type hostname: str
    :param payload: Complex mertic payload
    :type payload: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        payload = Payload.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'