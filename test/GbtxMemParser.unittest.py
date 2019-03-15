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
                {'elink0-0': 0xFF,
                 'elink0-1': 0x00,
                 'elink1-0': 0xFF,
                 'elink1-1': 0x01,
                 'elink2-0': 0xFF,
                 'elink2-1': 0x02,
                 'elink3-0': 0xFF,
                 'elink3-1': 0x03,
                 'elink4-0': 0xFF,
                 'elink4-1': 0xD6,
                 'elink5-0': 0x00,
                 'elink5-1': 0x00,
                 'elink6-0': 0xFF,
                 'elink6-1': 0x06},

                {'elink0-0': 0xFF,
                 'elink0-1': 0x00,
                 'elink1-0': 0xFF,
                 'elink1-1': 0x01,
                 'elink2-0': 0x59,
                 'elink2-1': 0x02,
                 'elink3-0': 0xFF,
                 'elink3-1': 0x03,
                 'elink4-0': 0xFF,
                 'elink4-1': 0xD8,
                 'elink5-0': 0x00,
                 'elink5-1': 0x00,
                 'elink6-0': 0xFF,
                 'elink6-1': 0x06},
            ]
        )


if __name__ == '__main__':
    unittest.main()
