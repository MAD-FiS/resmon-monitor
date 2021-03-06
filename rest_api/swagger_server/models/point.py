# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from rest_api.swagger_server.models.base_model_ import Model
from rest_api.swagger_server import util


class Point(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, time: datetime=None, value: float=None):  # noqa: E501
        """Point - a model defined in Swagger

        :param time: The time of this Point.  # noqa: E501
        :type time: datetime
        :param value: The value of this Point.  # noqa: E501
        :type value: float
        """
        self.swagger_types = {
            'time': datetime,
            'value': float
        }

        self.attribute_map = {
            'time': 'time',
            'value': 'value'
        }

        self._time = time
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'Point':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Point of this Point.  # noqa: E501
        :rtype: Point
        """
        return util.deserialize_model(dikt, cls)

    @property
    def time(self) -> datetime:
        """Gets the time of this Point.

        ISO 8601 datetime format with 1s accuracy  # noqa: E501

        :return: The time of this Point.
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time: datetime):
        """Sets the time of this Point.

        ISO 8601 datetime format with 1s accuracy  # noqa: E501

        :param time: The time of this Point.
        :type time: datetime
        """

        self._time = time

    @property
    def value(self) -> float:
        """Gets the value of this Point.

        Numerical value corresponding to the metric unit  # noqa: E501

        :return: The value of this Point.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value: float):
        """Sets the value of this Point.

        Numerical value corresponding to the metric unit  # noqa: E501

        :param value: The value of this Point.
        :type value: float
        """

        self._value = value
