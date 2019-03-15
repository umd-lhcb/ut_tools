#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from GbtxMemAnalyzer import ref_fixed_pattern, ref_cyclic_pattern
from GbtxMemAnalyzer import check_match
from GbtxMemAnalyzer import check_shift_single_byte, check_shift


class GbtxRefPatternTester(unittest.TestCase):
    def test_ref_fixed_pattern(self):
        self.assertEqual(
            ref_fixed_pattern([0x01, 0x04], ['elink0-0', 'elink0-1'], 3),
            [
                {'elink0-0': 0xFF01,
                 'elink0-1': 0xFF04},

                {'elink0-0': 0xFF01,
                 'elink0-1': 0xFF04},

                {'elink0-0': 0xFF01,
                 'elink0-1': 0xFF04}
            ]
        )

    def test_ref_cyclic_pattern(self):
        self.assertEqual(
            ref_cyclic_pattern([0x01, 0x02, 0x04],
                               ['elink0-0', 'elink2-0', 'elink4-0'],
                               [2, 3, 7],
                               length=10),
            [
                {'elink0-0': 0xFF01,
                 'elink2-0': 0xFF02,
                 'elink4-0': 0xFF04},

                {'elink0-0': 0xFF02,
                 'elink2-0': 0xFF03,
                 'elink4-0': 0xFF05},

                {'elink0-0': 0xFF01,
                 'elink2-0': 0xFF04,
                 'elink4-0': 0xFF06},

                {'elink0-0': 0xFF02,
                 'elink2-0': 0xFF02,
                 'elink4-0': 0xFF07},

                {'elink0-0': 0xFF01,
                 'elink2-0': 0xFF03,
                 'elink4-0': 0xFF08},

                {'elink0-0': 0xFF02,
                 'elink2-0': 0xFF04,
                 'elink4-0': 0xFF09},

                {'elink0-0': 0xFF01,
                 'elink2-0': 0xFF02,
                 'elink4-0': 0xFF0A},

                {'elink0-0': 0xFF02,
                 'elink2-0': 0xFF03,
                 'elink4-0': 0xFF04},

                {'elink0-0': 0xFF01,
                 'elink2-0': 0xFF04,
                 'elink4-0': 0xFF05},

                {'elink0-0': 0xFF02,
                 'elink2-0': 0xFF02,
                 'elink4-0': 0xFF06},
            ]
        )


class GbtxCheckMatchTester(unittest.TestCase):
    def test_check_match(self):
        ref_data = ref_fixed_pattern(
            [0x01, 0x04], ['elink0-0', 'elink4-0'], 3)
        parsed_data = [
            {'elink0-0': 0x01,
             'elink4-0': 0x04},

            {'elink0-0': 0x01,
             'elink4-0': 0x05},

            {'elink0-0': 0x01,
             'elink4-0': 0x04}
        ]
        self.assertEqual(
            check_match(ref_data, parsed_data),
            {'elink0-0': {'num_match': 3, 'num_of_mismatch': 0,
                          'percent_match': 1., 'percent_mismatch': 0.},
             'elink4-0': {'num_match': 2, 'num_of_mismatch': 1,
                          'percent_match': 2/3, 'percent_mismatch': 1/3}}
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
            -1
        )

    def test_check_shift(self):
        ref_data = ref_cyclic_pattern(
            [0x01, 0x02, 0x04], ['elink0-0', 'elink2-0', 'elink4-0'],
            [2, 3, 7], length=10)
        parsed_data = [
            {'elink0-0': 0x01,
             'elink2-0': 0x02,
             'elink4-0': 0x04},

            {'elink0-0': 0x02,
             'elink2-0': 0x03,
             'elink4-0': 0x05},

            {'elink0-0': 0x01,
             'elink2-0': 0x04,
             'elink4-0': 0x06},

            {'elink0-0': 0x02,
             'elink2-0': 0x02,
             'elink4-0': 0x07},

            {'elink0-0': 0x01,
             'elink2-0': 0x03,
             'elink4-0': 0x08},

            {'elink0-0': 0x02,
             'elink2-0': 0x04,
             'elink4-0': 0x09},

            {'elink0-0': 0x08,
             'elink2-0': 0x02,
             'elink4-0': 0x0A},

            {'elink0-0': 0x02,
             'elink2-0': 0x03,
             'elink4-0': 0x04},

            {'elink0-0': 0x01,
             'elink2-0': 0x04,
             'elink4-0': 0x05},

            {'elink0-0': 0x04,
             'elink2-0': 0x02,
             'elink4-0': 0x0C},
        ]
        self.assertEqual(
            check_shift(ref_data, parsed_data),
            {'elink0-0': [0, 0, 0, 0, 0, 0, 3, 0, 0, 1],
             'elink2-0': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             'elink4-0': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}
        )


if __name__ == '__main__':
    unittest.main()
