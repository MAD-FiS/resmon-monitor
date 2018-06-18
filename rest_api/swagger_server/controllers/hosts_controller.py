import connexion

from rest_api.swagger_server.models.error import Error  # noqa: E501
from rest_api.swagger_server.models.host import Host  # noqa: E501
from rest_api.swagger_server.models.host import Metric  # noqa: E501
from rest_api.swagger_server.models.host import Metadata  # noqa: E501
from rest_api.swagger_server.models.inline_response201 import (
    InlineResponse201
)  # noqa: E501
from rest_api.swagger_server.models.payload import Payload  # noqa: E501
from rest_api.swagger_server import util

from common.database.mongoAccess import dbApi
from rest_api.swagger_server.controllers.metrics_controller import get_metrics
from rest_api.apiUtils.apiUtils import QueryResolver

from flask_jwt_extended import jwt_required


@jwt_required
def delete_metric(metric_id, hostname):  # noqa: E501
    """Delete complex metric

     # noqa: E501

    :param metric_id: Metric identyfier. It has the same form as &#x60;metric_id&#x60; field of &#x60;Metric&#x60; model
    :type metric_id: str
    :param hostname: Target host (domain name)
    :type hostname: str

    :rtype: object
    """
    api = dbApi.dbApi()

    ids = api.getSessionIds(
        {api.HOSTNAME_KEY: hostname, api.METRIC_PATH: metric_id}
    )
    if len(ids) <= 0:
        return "Uknown metric or hostname", 404

    api.deleteComplexMetric(hostname, metric_id)
    api.deleteMetric(hostname, metric_id)

    return "Success", 200


@jwt_required
def get_hosts(q=None):  # noqa: E501
    """Get list of hosts

     # noqa: E501

    :param q: Filters out used metrics and hosts according to provided keys. String needs to match the following schema: &#x60;KEY1:VAL1,KEY2:VAL2;KEY3:VAL4...&#x60;. Comma is used to indicate &#x60;AND&#x60; operation while semicolon relates to &#x60;OR&#x60;. When &#x60;VAL&#x60; paramater is wrapped into slashes then regex mode is activated. For example when we query for &#x60;metric_id:cpu,os:/.*nix.*/;metric_id:cpu,os:/.*win.*/&#x60; we should receive cpu metric measurements for hosts containing either nix or win as substring in &#x60;os&#x60; metadata. Note that &#x60;AND&#x60; operation has higher priority than &#x60;OR&#x60;. Allowed keys: &#x60;metric_id&#x60;, &#x60;description&#x60;, &#x60;complex&#x60; (metric parameters) and all available host metadata fields. When not provided: No filtering performed - all available metrics and hosts are taken
    :type q: str

    :rtype: List[Host]
    """

    api = dbApi.dbApi()
    if q:
        hosts = []
        filters = QueryResolver.QueryResolver(q).getFilters()
        for f in filters:
            hosts.extend(api.getHosts(query=f))
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
        metadatas = [
            Metadata.from_dict(metadata)
            for metadata in api.getMetadataByHost(host)
        ]
        response.append(
            (
                Host(hostname=host, metrics=metrics, metadata=metadatas)
            ).to_dict()
        )

    return response


@jwt_required
def post_metric(hostname, payload):  # noqa: E501
    """Add complex metric

     # noqa: E501

    :param hostname: Target host (domain name)
    :type hostname: str
    :param payload: Complex mertic payload
    :type payload: dict | bytes

    :rtype: InlineResponse201
    """
    api = dbApi.dbApi()
    if connexion.request.is_json:
        payload = Payload.from_dict(connexion.request.get_json())  # noqa: E501

    parent_id = payload.parent_id
    moving_window = payload.moving_window_duration
    interval = payload.interval

    if interval <= 0:
        return "Interval has to be greather than 0", 400

    if moving_window <= 0:
        return "Moving window has to be greater than 0", 400

    description = payload.description
    metric_id = (
        "cpx_"
        + str(parent_id)
        + "_"
        + str(moving_window)
        + "_"
        + str(interval)
    )

    metrics = api.getAllMetrics({dbApi.dbApi.HOSTNAME_KEY: hostname})
    if metric_id in metrics:
        return "Metric id already exists", 409

    print(metrics)
    if parent_id not in metrics:
        return "Unknown parent_id", 404

    hostnames = api.getHosts(None)
    if hostname not in hostnames:
        return "Unknown hostname", 404

    unit = api.updateMetricInMetadata(
        hostname, metric_id, parent_id, description
    )
    if unit == "":
        unit = "Unknown Unit"

    api.insertMeasDefinition(
        hostname, metric_id, parent_id, moving_window, interval, description
    )
    response = InlineResponse201(metric_id, unit)
    return response.to_dict(), 201
