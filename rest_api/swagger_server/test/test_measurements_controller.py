# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.measurement import Measurement  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMeasurementsController(BaseTestCase):
    """MeasurementsController integration test stubs"""

    def test_get_measurements(self):
        """Test case for get_measurements

        Selected measurements
        """
        query_string = [('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00'),
                        ('q', 'q_example'),
                        ('limit', 8.14),
                        ('last', true)]
        response = self.client.open(
            '/measurements',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()