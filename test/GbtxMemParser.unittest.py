#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from ut_tools.GbtxMemParser import GbtxMemParser


class GbtxMemParserTester(unittest.TestCase):
    def test_dissect_str_to_dict_case1(self):
        raw_line = '800CFFD6FC11FD09FF07FE05FF030001'
        self.assertEqual(
            GbtxMemParser.dissect_str_to_dict(raw_line),
            {'elink0': 0x01,
             'elink1': 0x00,
             'elink2': 0x03,
             'elink3': 0xFF,
             'elink4': 0x05,
             'elink5': 0xFE,
             'elink6': 0x07,
             'elink7': 0xFF,
             'elink8': 0x09,
             'elink9': 0xFD,
             'elink10': 0x11,
             'elink11': 0xFC},
        )

    def test_dissect_str_to_dict_case2(self):
        raw_line = '800CFFD8FF035902FF07FE05FF030001'
        self.assertEqual(
            GbtxMemParser.dissect_str_to_dict(raw_line),
            {'elink0': 0x01,
             'elink1': 0x00,
             'elink2': 0x03,
             'elink3': 0xFF,
             'elink4': 0x05,
             'elink5': 0xFE,
             'elink6': 0x07,
             'elink7': 0xFF,
             'elink8': 0x02,
             'elink9': 0x59,
             'elink10': 0x03,
             'elink11': 0xFF}
        )


if __name__ == '__main__':
    unittest.main()
