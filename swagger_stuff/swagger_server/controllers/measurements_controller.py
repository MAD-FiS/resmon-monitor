import connexion
import six

from swagger_server.models.measurement import Measurement  # noqa: E501
from swagger_server import util


def get_measurements(_from=None, to=None, q=None):  # noqa: E501
    """Selected measurements

     # noqa: E501

    :param _from: ISO 8601 datetime format with 1s accuracy
    :type _from: str
    :param to: ISO 8601 datetime format with 1s accuracy
    :type to: str
    :param q: Filters out used metrics and hosts according to provided keys. String needs to match the following schema: &#x60;KEY1:VAL1,KEY2:VAL2;KEY3:VAL4...&#x60;. Comma is used to indicate &#x60;AND&#x60; operation while semicolon relates to &#x60;OR&#x60;. When &#x60;VAL&#x60; paramater is wrapped into slashes then regex mode is activated. For example when we query for &#x60;metric_id:cpu,os:/.*nix.*/;metric_id:cpu,os:/.*win.*/&#x60; we should receive cpu metric measurements for hosts containing either nix or win as substring in &#x60;os&#x60; metadata. Note that &#x60;AND&#x60; operation has higher priority than &#x60;OR&#x60;. Allowed keys: &#x60;metric_id&#x60;, &#x60;description&#x60;, &#x60;complex&#x60; (metric parameters) and all available host metadata fields.
    :type q: str

    :rtype: List[Measurement]
    """
    _from = util.deserialize_datetime(_from)
    to = util.deserialize_datetime(to)
    return 'do some magic!'
