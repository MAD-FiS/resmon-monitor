# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.measurement import Measurement  # noqa: E501
from swagger_server.models.value import Value  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMeasurementsController(BaseTestCase):
    """MeasurementsController integration test stubs"""

    def test_get_measurements(self):
        """Test case for get_measurements

        Get measurements from all hosts
        """
        response = self.client.open(
            '/measurements',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_measurements_host(self):
        """Test case for get_measurements_host

        Get measurements from particular host
        """
        response = self.client.open(
            '/measurements/{hostname}'.format(hostname='hostname_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_measurements_host_metric(self):
        """Test case for get_measurements_host_metric

        Get measurements from particular host of particular metric
        """
        response = self.client.open(
            '/measurements/{hostname}/{metric_id}'.format(hostname='hostname_example', metric_id='metric_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
