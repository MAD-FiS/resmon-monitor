# coding: utf-8

from __future__ import absolute_import

from rest_api.swagger_server.test import BaseTestCase


class TestMetadataController(BaseTestCase):
    """MetadataController integration test stubs"""

    def test_get_metadata(self):
        """Test case for get_metadata

        List of all available hosts metadata
        """
        response = self.client.open(
            '/metadata',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
