# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Value(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, time: datetime=None, value: float=None):  # noqa: E501
        """Value - a model defined in Swagger

        :param time: The time of this Value.  # noqa: E501
        :type time: datetime
        :param value: The value of this Value.  # noqa: E501
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
    def from_dict(cls, dikt) -> 'Value':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Value of this Value.  # noqa: E501
        :rtype: Value
        """
        return util.deserialize_model(dikt, cls)

    @property
    def time(self) -> datetime:
        """Gets the time of this Value.


        :return: The time of this Value.
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time: datetime):
        """Sets the time of this Value.


        :param time: The time of this Value.
        :type time: datetime
        """

        self._time = time

    @property
    def value(self) -> float:
        """Gets the value of this Value.


        :return: The value of this Value.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value: float):
        """Sets the value of this Value.


        :param value: The value of this Value.
        :type value: float
        """

        self._value = value
