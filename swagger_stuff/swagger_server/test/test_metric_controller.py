# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.dummy import Dummy  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMetricController(BaseTestCase):
    """MetricController integration test stubs"""

    def test_delete_metric(self):
        """Test case for delete_metric

        Delete complex metric
        """
        response = self.client.open(
            '/metric/{metric_id}'.format(metric_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_metric(self):
        """Test case for post_metric

        Add complex metric
        """
        dummy = Dummy()
        response = self.client.open(
            '/metric',
            method='POST',
            data=json.dumps(dummy),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
