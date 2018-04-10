# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestResourcesController(BaseTestCase):
    """ResourcesController integration test stubs"""

    def test_get_hosts(self):
        """Test case for get_hosts

        Get list of hosts
        """
        response = self.client.open(
            '/resources',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
