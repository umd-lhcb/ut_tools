#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from GbtxMemParser import GbtxMemParser


class GbtxMemParserTester(unittest.TestCase):
    def test_dissect_str_to_dict(self):
        raw_data = ['800CFFD6FF03FF02FF01FF00FF060000',
                    '800CFFD8FF035902FF01FF00FF060000']
        self.assertEqual(
            GbtxMemParser.dissect_str_to_dict(raw_data),
            [
                {'elink0': 0x00,
                 'elink1': 0x00,
                 'elink2': 0xFF,
                 'elink3': 0x06,
                 'elink4': 0xFF,
                 'elink5': 0x00,
                 'elink6': 0xFF,
                 'elink7': 0x01,
                 'elink8': 0xFF,
                 'elink9': 0x02,
                 'elink10': 0xFF,
                 'elink11': 0x03},

                {'elink0': 0x00,
                 'elink1': 0x00,
                 'elink2': 0xFF,
                 'elink3': 0x06,
                 'elink4': 0xFF,
                 'elink5': 0x00,
                 'elink6': 0xFF,
                 'elink7': 0x01,
                 'elink8': 0x59,
                 'elink9': 0x02,
                 'elink10': 0xFF,
                 'elink11': 0x03}
            ]
        )


if __name__ == '__main__':
    unittest.main()
