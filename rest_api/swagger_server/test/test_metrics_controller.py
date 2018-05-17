# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.metric import Metric  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMetricsController(BaseTestCase):
    """MetricsController integration test stubs"""

    def test_get_metrics(self):
        """Test case for get_metrics

        List of metrics
        """
        response = self.client.open(
            '/metrics',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
