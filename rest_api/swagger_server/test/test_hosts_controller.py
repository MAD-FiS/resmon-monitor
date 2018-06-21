# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from rest_api.swagger_server.models.error import Error  # noqa: E501
from rest_api.swagger_server.models.host import Host  # noqa: E501
from rest_api.swagger_server.models.inline_response201 import (
    InlineResponse201
)  # noqa: E501
from rest_api.swagger_server.models.payload import Payload  # noqa: E501
from rest_api.swagger_server.test import BaseTestCase

from unittest.mock import patch


authorizationToken = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    "eyJpYXQiOjE1MjkzNTk4MDIsIm5iZiI6MTUyO"
    "TM1OTgwMiwianRpIjoiZTY4N2M5YzgtNDk3ZS"
    "00MzRhLWI0MDItYTdmMmRhYzc3ZGQ4IiwiaWR"
    "lbnRpdHkiOiJhc2QiLCJmcmVzaCI6ZmFsc2Us"
    "InR5cGUiOiJhY2Nlc3MifQ.Us_sjA7wc90ltl"
    "mlgEnz1FaotgMzVXoFAzkrJt56Tcw"
)
dbModulePath = (
    "rest_api.swagger_server.controllers.hosts_controller.dbApi.dbApi."
)


class TestHostsController(BaseTestCase):
    """HostsController integration test stubs"""

    @patch(dbModulePath + "getCpxDefinitions")
    @patch(dbModulePath + "getSessionIds")
    def test_delete_metric(self, mock_getSessionIds, mock_getCpxDefinitions):
        """Test case for delete_metric

        Delete complex metric
        """
        mock_getSessionIds.return_value = [1314042]
        mock_getCpxDefinitions.return_value = {"owner": "asd"}
        response = self.client.delete(
            "/hosts/{hostname}/metrics/{metric_id}".format(
                metric_id="metric_id_example", hostname="hostname_example"
            ),
            headers={"Authorization": "Bearer " + authorizationToken},
        )
        self.assert200(
            response, "Response body is : " + response.data.decode("utf-8")
        )

    @patch(dbModulePath + "getCpxDefinitions")
    def test_get_hosts(self, mock_getCpxDefinitions):
        """Test case for get_hosts

        Get list of hosts
        """
        mock_getCpxDefinitions = {"owner": "asd"}
        query_string = [("q", "os:q_example")]
        response = self.client.get(
            "/hosts",
            query_string=query_string,
            headers={"Authorization": "Bearer " + authorizationToken},
        )
        self.assert200(
            response, "Response body is : " + response.data.decode("utf-8")
        )

    @patch(dbModulePath + "updateMetricInMetadata")
    @patch(dbModulePath + "getHosts")
    @patch(dbModulePath + "getAllMetrics")
    def test_post_metric(
        self, mock_getAllMetrics, mock_getHosts, mock_updateMetricInMetadata
    ):
        """Test case for post_metric

        Add complex metric
        """
        hostExistingInDb = "dummyHostname"
        metricExistingInDb = "dummyMetric"
        mock_getAllMetrics.return_value = [metricExistingInDb]
        mock_getHosts.return_value = [hostExistingInDb]
        mock_updateMetricInMetadata.return_value = "meters"
        interval_value = 10
        moving_window_value = 20
        payload = Payload(
            description="dummyDesc",
            interval=interval_value,
            moving_window_duration=moving_window_value,
            parent_id=metricExistingInDb,
        )
        response = self.client.post(
            "/hosts/{hostname}/metrics".format(hostname=hostExistingInDb),
            headers={"Authorization": "Bearer " + authorizationToken},
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertStatus(
            response,
            201,
            "Response body is : " + response.data.decode("utf-8"),
        )
        self.assertEqual(
            json.loads(response.data),
            {
                "id": "cpx_"
                + metricExistingInDb
                + "_"
                + str(moving_window_value)
                + "_"
                + str(interval_value),
                "unit": "meters",
            },
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
