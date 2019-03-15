#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from GbtxMemParser import GbtxMemParser


class GbtxMemParserTester(unittest.TestCase):
    def test_dissect_str_to_dict(self):
        raw_data = ['800CFFD6FF03FF02FF01FF00FF060000',
                    '800CFF6DFF03FD02FF01FF00FF060000',
                    '800CFFD8FF035902FF01FF00FF060000']
        self.assertEqual(
            GbtxMemParser.dissect_str_to_dict(raw_data),
            [
                {'egroup0': 0xFF00,
                 'egroup1': 0xFF01,
                 'egroup2': 0xFF02,
                 'egroup3': 0xFF03,
                 'egroup4': 0xFFD6,
                 'egroup5': 0x0000,
                 'egroup6': 0xFF06},

                {'egroup0': 0xFF00,
                 'egroup1': 0xFF01,
                 'egroup2': 0xFD02,
                 'egroup3': 0xFF03,
                 'egroup4': 0xFF6D,
                 'egroup5': 0x0000,
                 'egroup6': 0xFF06},

                {'egroup0': 0xFF00,
                 'egroup1': 0xFF01,
                 'egroup2': 0x5902,
                 'egroup3': 0xFF03,
                 'egroup4': 0xFFD8,
                 'egroup5': 0x0000,
                 'egroup6': 0xFF06},
            ]
        )


if __name__ == '__main__':
    unittest.main()
