# coding: utf-8

from __future__ import absolute_import

from rest_api.swagger_server.test import BaseTestCase


class TestMeasurementsController(BaseTestCase):
    """MeasurementsController integration test stubs"""

    def test_get_measurements(self):
        """Test case for get_measurements

        Selected measurements
        """
        query_string = [('start', '2010-05-10'),
                        ('end', '2018-08-10'),
                        ('q', 'os:/.*a.*/')]
        response = self.client.open('/measurements', method='GET', query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
