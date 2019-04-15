#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from CometTools.GbtxMemAnalyzer import ref_cyclic_pattern
from CometTools.GbtxMemAnalyzer import check_match
from CometTools.GbtxMemAnalyzer import check_shift_single_byte


class GbtxRefPatternTester(unittest.TestCase):
    def test_ref_cyclic_pattern(self):
        self.assertEqual(
            ref_cyclic_pattern(['elink0', 'elink2', 'elink4'], [1, 3, 100]),
            {
                'elink0': [i for i in range(0, 256)],
                'elink2': [i for i in range(0, 256, 3)],
                'elink4': [0, 100, 200]
            }
        )


class GbtxCheckMatchTester(unittest.TestCase):
    def test_check_match(self):
        ref_value = {
            'elink0': 0xF0,
            'elink4': 0xB4
        }
        parsed_data = [
            {'elink0': 0xF0,
             'elink4': 0xB4},

            {'elink0': 0xF0,
             'elink4': 0xB5},

            {'elink0': 0xF0,
             'elink4': 0xB4}
        ]
        self.assertEqual(
            check_match(ref_value, parsed_data),
            {'elink0': {'num_of_match': 3,
                        'num_of_mismatch': 0,
                        'num_of_shifts': 0,
                        'percent_match': 1.,
                        'percent_mismatch': 0.},
             'elink4': {'num_of_match': 2,
                        'num_of_mismatch': 1,
                        'num_of_shifts': 0,
                        'percent_match': round(2/3, 5),
                        'percent_mismatch': round(1/3, 5)}}
        )


class GbtxCheckShiftTester(unittest.TestCase):
    def test_check_shift_single_byte_none(self):
        self.assertEqual(
            check_shift_single_byte(0b00010001, 0b00010001),
            0
        )

    def test_check_shift_single_byte_positive(self):
        self.assertEqual(
            check_shift_single_byte(0b00010001, 0b01000100),
            2
        )

    def test_check_shift_single_byte_negative(self):
        self.assertEqual(
            check_shift_single_byte(0b00010001, 0b10001000),
            3
        )

    def test_check_shift_single_byte_mismatch(self):
        self.assertEqual(
            check_shift_single_byte(0b00010001, 0b10001001),
            8
        )


if __name__ == '__main__':
    unittest.main()
