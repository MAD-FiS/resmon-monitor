# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from rest_api.swagger_server.models.error import Error  # noqa: E501
from rest_api.swagger_server.models.metric import Metric  # noqa: E501
from rest_api.swagger_server.test import BaseTestCase

authorizationToken = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    "eyJpYXQiOjE1MjkzNTk4MDIsIm5iZiI6MTUyO"
    "TM1OTgwMiwianRpIjoiZTY4N2M5YzgtNDk3ZS"
    "00MzRhLWI0MDItYTdmMmRhYzc3ZGQ4IiwiaWR"
    "lbnRpdHkiOiJhc2QiLCJmcmVzaCI6ZmFsc2Us"
    "InR5cGUiOiJhY2Nlc3MifQ.Us_sjA7wc90ltl"
    "mlgEnz1FaotgMzVXoFAzkrJt56Tcw"
)


class TestMetricsController(BaseTestCase):
    """MetricsController integration test stubs"""

    def test_get_metrics(self):
        """Test case for get_metrics

        List of metrics
        """
        response = self.client.get(
            "/metrics",
            headers={"Authorization": "Bearer " + authorizationToken},
        )
        self.assert200(
            response, "Response body is : " + response.data.decode("utf-8")
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
