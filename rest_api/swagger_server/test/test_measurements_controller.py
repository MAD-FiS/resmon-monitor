# coding: utf-8

from __future__ import absolute_import

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


class TestMeasurementsController(BaseTestCase):
    """MeasurementsController integration test stubs"""

    def test_get_measurements(self):
        """Test case for get_measurements

        Selected measurements
        """
        query_string = [
            ("start", "2013-10-20T19:20:30+01:00"),
            ("end", "2013-10-20T19:20:30+01:00"),
            ("q", "os:q_example"),
            ("limit", 8.14),
            ("last", True),
        ]
        response = self.client.get(
            "/measurements",
            headers={"Authorization": "Bearer " + authorizationToken},
            query_string=query_string,
        )
        self.assert200(
            response, "Response body is : " + response.data.decode("utf-8")
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
