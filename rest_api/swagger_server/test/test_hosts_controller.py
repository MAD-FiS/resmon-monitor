# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.host import Host  # noqa: E501
from swagger_server.models.payload import Payload  # noqa: E501
from swagger_server.test import BaseTestCase


class TestHostsController(BaseTestCase):
    """HostsController integration test stubs"""

    def test_delete_metric(self):
        """Test case for delete_metric

        Delete complex metric
        """
        response = self.client.open(
            '/hosts/{hostname}/metrics/{metric_id}'.format(metric_id='metric_id_example', hostname='hostname_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_hosts(self):
        """Test case for get_hosts

        Get list of hosts
        """
        query_string = [('q', 'No filtering performed - all available metrics and hosts are taken')]
        response = self.client.open(
            '/hosts',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_metric(self):
        """Test case for post_metric

        Add complex metric
        """
        payload = Payload()
        response = self.client.open(
            '/hosts/{hostname}/metrics'.format(hostname='hostname_example'),
            method='POST',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
