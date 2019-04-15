#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from CometTools.GbtxMemParser import GbtxMemParser


class GbtxMemParserTester(unittest.TestCase):
    def test_dissect_str_to_dict(self):
        raw_data = ['800CFFD6FC11FD09FF07FE05FF030001',
                    '800CFFD8FF035902FF07FE05FF030001']
        self.assertEqual(
            GbtxMemParser.dissect_str_to_dict(raw_data),
            [
                {'elink0': 0x00,
                 'elink1': 0x01,
                 'elink2': 0xFF,
                 'elink3': 0x03,
                 'elink4': 0xFE,
                 'elink5': 0x05,
                 'elink6': 0xFF,
                 'elink7': 0x07,
                 'elink8': 0xFD,
                 'elink9': 0x09,
                 'elink10': 0xFC,
                 'elink11': 0x11},

                {'elink0': 0x00,
                 'elink1': 0x01,
                 'elink2': 0xFF,
                 'elink3': 0x03,
                 'elink4': 0xFE,
                 'elink5': 0x05,
                 'elink6': 0xFF,
                 'elink7': 0x07,
                 'elink8': 0x59,
                 'elink9': 0x02,
                 'elink10': 0xFF,
                 'elink11': 0x03}
            ]
        )


if __name__ == '__main__':
    unittest.main()
