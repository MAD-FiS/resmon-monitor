import unittest
from unittest.mock import MagicMock

import QueryResolver
import re


class TestResolver(unittest.TestCase):
    """Class for unittest of QueryResolver"""
    def test_resolverShouldReturnProperValues(self):
        """Method for testing if resolver returns proper value"""
        query = "metric_id:cpu,os:/.*nix.*/;metric_id:cpu,os:/.*win.*/"

        resolver = QueryResolver.QueryResolver(query)
        filters = resolver.getFilters()

        self.assertEqual(len(filters), 2)
        self.assertEqual(filters[0],
                         {"metric_id": "cpu", "os": re.compile(".*nix.*")})

        self.assertEqual(filters[1],
                         {"metric_id": "cpu", "os": re.compile(".*win.*")})

    def test_queryContent(self):
        """Method for testing query validation"""
        query1 = "metric_id:cpu,os:/.*nix.*/;metric_id:cpu,os:/.*win.*/"
        resolver1 = QueryResolver.QueryResolver(query1)
        self.assertEqual(resolver1.validateQuery(), 1)

        query2 = "metric_id:cpu,os://;metric_id:cpu,os:/.*win.*/"
        resolver2 = QueryResolver.QueryResolver(query2)
        self.assertEqual(resolver2.validateQuery(), 0)

        query3 = ":cpu,os:/.*nix.*/;metric_id:cpu,os:/.*win.*/"
        resolver3 = QueryResolver.QueryResolver(query3)
        self.assertEqual(resolver3.validateQuery(), 0)

        query4 = "metric_id:cpu,os:/.*nix.*/;metric_id:cpu,os:/"
        resolver4 = QueryResolver.QueryResolver(query4)
        self.assertEqual(resolver4.validateQuery(), 0)

        query5 = "metric_id:cpu,os:/.*nix.*/;lotr:cpu,os:/.*win.*/"
        resolver5 = QueryResolver.QueryResolver(query5)
        self.assertEqual(resolver5.validateQuery(), 0)

        query6 = "metric_id,os:/.*nix.*/;lotr:cpu,os:/.*win.*/"
        resolver6 = QueryResolver.QueryResolver(query6)
        self.assertEqual(resolver6.validateQuery(), 0)

        query7 = "metric_id,os:/.*nix.*/,metric_id:cpu,os:/.*win.*/"
        resolver7 = QueryResolver.QueryResolver(query7)
        self.assertEqual(resolver7.validateQuery(), 0)

        query8 = "os:/.*nix.*/;metric_id,cpu,os:/.*win.*/"
        resolver8 = QueryResolver.QueryResolver(query8)
        self.assertEqual(resolver8.validateQuery(), 0)

        query9 = ".*"
        resolver9 = QueryResolver.QueryResolver(query9)
        self.assertEqual(resolver9.validateQuery(), 0)

        query10 = "metric_id:dummy"
        resolver10 = QueryResolver.QueryResolver(query10)
        self.assertEqual(resolver10.validateQuery(), 1)


if __name__ == '__main__':
    unittest.main()
