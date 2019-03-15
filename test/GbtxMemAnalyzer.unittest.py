#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from GbtxMemAnalyzer import ref_fixed_pattern, ref_cyclic_pattern
from GbtxMemAnalyzer import check_match


class GbtxRefPatternTester(unittest.TestCase):
    def test_ref_fixed_pattern(self):
        self.assertEqual(
            ref_fixed_pattern([0xFF01, 0xFF04], ['egroup0', 'egroup4'], 3),
            [
                {'egroup0': 0xFF01,
                 'egroup4': 0xFF04},

                {'egroup0': 0xFF01,
                 'egroup4': 0xFF04},

                {'egroup0': 0xFF01,
                 'egroup4': 0xFF04}
            ]
        )

    def test_ref_cyclic_pattern(self):
        self.assertEqual(
            ref_cyclic_pattern([0xFF01, 0xFF02, 0xFF04],
                               ['egroup0', 'egroup2', 'egroup4'],
                               [2, 3, 7],
                               length=10),
            [
                {'egroup0': 0xFF01,
                 'egroup2': 0xFF02,
                 'egroup4': 0xFF04},

                {'egroup0': 0xFF02,
                 'egroup2': 0xFF03,
                 'egroup4': 0xFF05},

                {'egroup0': 0xFF01,
                 'egroup2': 0xFF04,
                 'egroup4': 0xFF06},

                {'egroup0': 0xFF02,
                 'egroup2': 0xFF02,
                 'egroup4': 0xFF07},

                {'egroup0': 0xFF01,
                 'egroup2': 0xFF03,
                 'egroup4': 0xFF08},

                {'egroup0': 0xFF02,
                 'egroup2': 0xFF04,
                 'egroup4': 0xFF09},

                {'egroup0': 0xFF01,
                 'egroup2': 0xFF02,
                 'egroup4': 0xFF0A},

                {'egroup0': 0xFF02,
                 'egroup2': 0xFF03,
                 'egroup4': 0xFF04},

                {'egroup0': 0xFF01,
                 'egroup2': 0xFF04,
                 'egroup4': 0xFF05},

                {'egroup0': 0xFF02,
                 'egroup2': 0xFF02,
                 'egroup4': 0xFF06},
            ]
        )


class GbtxCheckMatchTester(unittest.TestCase):
    def test_check_match(self):
        ref_data = ref_fixed_pattern(
            [0xFF01, 0xFF04], ['egroup0', 'egroup4'], 3)
        parsed_data = [
            {'egroup0': 0xFF01,
             'egroup4': 0xFF04},

            {'egroup0': 0xFF01,
             'egroup4': 0xFF05},

            {'egroup0': 0xFF01,
             'egroup4': 0xFF04}
        ]
        self.assertEqual(
            check_match(ref_data, parsed_data),
            {'egroup0': {'num_match': 3, 'num_of_mismatch': 0,
                         'percent_match': 1., 'percent_mismatch': 0.},
             'egroup4': {'num_match': 2, 'num_of_mismatch': 1,
                         'percent_match': 2/3, 'percent_mismatch': 1/3}}
        )


class GbtxCheckShiftTester(unittest.TestCase):
    def test_check_match(self):
        ref_data = ref_cyclic_pattern(
            [0xFF01, 0xFF02, 0xFF04], ['egroup0', 'egroup2', 'egroup4'],
            [2, 3, 7], length=10)
        parsed_data = [
            {'egroup0': 0xFF01,
             'egroup2': 0xFF02,
             'egroup4': 0xFF04},

            {'egroup0': 0xFF02,
             'egroup2': 0xFF03,
             'egroup4': 0xFF05},

            {'egroup0': 0xFF01,
             'egroup2': 0xFF04,
             'egroup4': 0xFF06},

            {'egroup0': 0xFF02,
             'egroup2': 0xFF02,
             'egroup4': 0xFF07},

            {'egroup0': 0xFF01,
             'egroup2': 0xFF03,
             'egroup4': 0xFF08},

            {'egroup0': 0xFF02,
             'egroup2': 0xFF04,
             'egroup4': 0xFF09},

            {'egroup0': 0xFF00,
             'egroup2': 0xFF02,
             'egroup4': 0xFF0A},

            {'egroup0': 0xFF02,
             'egroup2': 0xFF03,
             'egroup4': 0xFF04},

            {'egroup0': 0xFF01,
             'egroup2': 0xFF04,
             'egroup4': 0xFF05},

            {'egroup0': 0xFF03,
             'egroup2': 0xFF02,
             'egroup4': 0xFF04},
        ]
        self.assertEqual(
            check_shift(ref_data, parsed_data),
            {'egroup0': [0, 0, 0, 0, 0, 0, -1, 0, 0, 1],
             'egroup2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             'egroup4': [0, 0, 0, 0, 0, 0, 0, 0, 0, -2]}
        )


if __name__ == '__main__':
    unittest.main()
