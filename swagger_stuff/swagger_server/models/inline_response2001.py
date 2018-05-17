# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.inline_response2001_metricid import InlineResponse2001METRICID  # noqa: F401,E501
from swagger_server import util


class InlineResponse2001(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, metric_id: InlineResponse2001METRICID=None):  # noqa: E501
        """InlineResponse2001 - a model defined in Swagger

        :param metric_id: The metric_id of this InlineResponse2001.  # noqa: E501
        :type metric_id: InlineResponse2001METRICID
        """
        self.swagger_types = {
            'metric_id': InlineResponse2001METRICID
        }

        self.attribute_map = {
            'metric_id': '[METRIC_ID]'
        }

        self._metric_id = metric_id

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2001':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_1 of this InlineResponse2001.  # noqa: E501
        :rtype: InlineResponse2001
        """
        return util.deserialize_model(dikt, cls)

    @property
    def metric_id(self) -> InlineResponse2001METRICID:
        """Gets the metric_id of this InlineResponse2001.


        :return: The metric_id of this InlineResponse2001.
        :rtype: InlineResponse2001METRICID
        """
        return self._metric_id

    @metric_id.setter
    def metric_id(self, metric_id: InlineResponse2001METRICID):
        """Sets the metric_id of this InlineResponse2001.


        :param metric_id: The metric_id of this InlineResponse2001.
        :type metric_id: InlineResponse2001METRICID
        """

        self._metric_id = metric_id
