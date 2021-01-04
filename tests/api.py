#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from idmclient.api import find_by_name


class ApiTestCase(unittest.TestCase):

    def test_find(self):
        result = set(m.name for m in find_by_name("Tap Water*Temperature"))
        expected = {
            "Tap Water Temperature",
            "Tap Water Heater Top Temperature",
            "Tap Water Heater Bottom Temperature"
        }
        self.assertSetEqual(expected, result)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(ApiTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
