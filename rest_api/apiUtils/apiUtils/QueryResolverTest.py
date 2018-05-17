import unittest
from unittest.mock import MagicMock

import QueryResolver
import re


class TestResolver(unittest.TestCase):
    def test_resolverShouldReturnProperValues(self):
        query="metric_id:cpu,os:/.*nix.*/;metric_id:cpu,os:/.*win.*/"

        resolver = QueryResolver.QueryResolver(query)
        filters = resolver.getFilters()

        self.assertEqual(len(filters), 2)
        self.assertEqual(filters[0][0], {"metric_id":"cpu", "os":re.compile(".*nix.*")})
        self.assertEqual(filters[0][1], "cpu")

        self.assertEqual(filters[1][0], {"metric_id":"cpu", "os":re.compile(".*win.*")})
        self.assertEqual(filters[1][1], "cpu")


if __name__ == '__main__':
    unittest.main()

