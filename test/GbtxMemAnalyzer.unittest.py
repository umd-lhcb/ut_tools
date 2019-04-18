#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from CometTools.GbtxMemAnalyzer import ref_cyclic_pattern
from CometTools.GbtxMemAnalyzer import check_match
from CometTools.GbtxMemAnalyzer import check_shift, check_shift_single_byte
from CometTools.GbtxMemAnalyzer import concatenate_bytes, find_slicing_idx
from CometTools.GbtxMemAnalyzer import slice_ref_patterns
from CometTools.GbtxMemAnalyzer import find_counting_direction
from CometTools.GbtxMemAnalyzer import check_time_evolution


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


class GbtxCheckShiftTester(unittest.TestCase):
    def test_check_shift_single_byte_none(self):
        self.assertEqual(
            check_shift_single_byte(0b00010001, 0b00010001),
            0
        )

    def test_check_shift_single_byte_match_case1(self):
        self.assertEqual(
            check_shift_single_byte(0b00010001, 0b01000100),
            2
        )

    def test_check_shift_single_byte_match_case2(self):
        self.assertEqual(
            check_shift_single_byte(0b00010001, 0b10001000),
            3
        )

    def test_check_shift_single_byte_mismatch(self):
        self.assertEqual(
            check_shift_single_byte(0b00010001, 0b10001001),
            9
        )

    def test_check_shift_match_case1(self):
        self.assertEqual(
            check_shift(0xFFFE, 0xFFFEFD, 16, 24),
            8
        )

    def test_check_shift_match_case2(self):
        self.assertEqual(
            check_shift(0xFDFC, 0xFFFDFC, 16, 24),
            0
        )

    def test_check_shift_mismatch(self):
        self.assertEqual(
            check_shift(0xFDFC, 0xFFFDFE, 16, 24),
            9
        )


class CheckMatchTester(unittest.TestCase):
    def test_check_match(self):
        ref_value = {
            'elink0': 0xF0,
            'elink4': 0xB4,
            'elink5': 0x01
        }
        parsed_data = [
            {'elink0': 0xF0,
             'elink4': 0xB4,
             'elink5': 0x01},

            {'elink0': 0xF0,
             'elink4': 0xB5,
             'elink5': 0x02},

            {'elink0': 0xF0,
             'elink4': 0xB4,
             'elink5': 0x02}
        ]
        self.assertEqual(
            check_match(ref_value, parsed_data),
            {'elink0': {'num_of_match': 3,
                        'num_of_mismatch': 0,
                        'num_of_shifts': 0,
                        'percent_match': 1.,
                        'percent_mismatch': 0.,
                        'badness': [0, 0, 0]},
             'elink4': {'num_of_match': 2,
                        'num_of_mismatch': 1,
                        'num_of_shifts': 0,
                        'percent_match': round(2/3, 5),
                        'percent_mismatch': round(1/3, 5),
                        'badness': [0, 9, 0]},
             'elink5': {'num_of_match': 3,
                        'num_of_mismatch': 0,
                        'num_of_shifts': 2,
                        'percent_match': 1.,
                        'percent_mismatch': 0.,
                        'badness': [0, 1, 1]}
             }
        )


class CheckTimeEvolutionTester(unittest.TestCase):
    def test_concatenate_bytes_case1(self):
        self.assertEqual(
            concatenate_bytes([0xFE, 0xFD]),
            0xFEFD
        )

    def test_concatenate_bytes_case2(self):
        self.assertEqual(
            concatenate_bytes([0xFE, 0xFD, 0x02, 0x3C]),
            0xFEFD023C
        )

    def test_concatenate_bytes_case3(self):
        self.assertEqual(
            concatenate_bytes([0x02, 0x3C], reverse=False),
            0x3C02
        )

    def test_find_slicing_idx_case1(self):
        self.assertEqual(
            find_slicing_idx(0, 10, slice_size=3),
            (0, 3)
        )

    def test_find_slicing_idx_case2(self):
        self.assertEqual(
            find_slicing_idx(2, 4, slice_size=3),
            (0, 4)
        )

    def test_find_slicing_idx_case3(self):
        self.assertEqual(
            find_slicing_idx(4, 11, slice_size=3),
            (1, 7)
        )

    def test_find_counting_direction_up_case1(self):
        data = 0xFDFEFF
        ref_patterns = {'elink0': [0xFD, 0xFE, 0xFF]}
        sliced = slice_ref_patterns(ref_patterns)['elink0']
        self.assertEqual(
            find_counting_direction(sliced, data, 24),
            (1, 8)
        )

    def test_find_counting_direction_up_case2(self):
        data = 0xFFFDFE
        ref_patterns = {'elink0': [0xFD, 0xFE, 0xFF]}
        sliced = slice_ref_patterns(ref_patterns)['elink0']
        self.assertEqual(
            find_counting_direction(sliced, data, 24),
            (1, 0)
        )

    def test_find_counting_direction_up_case3(self):
        data = 0xFEFEFF
        ref_patterns = {'elink0': [0xFD, 0xFE, 0xFF]}
        sliced = slice_ref_patterns(ref_patterns)['elink0']
        self.assertEqual(
            find_counting_direction(sliced, data, 24),
            (1, 0)
        )

    def test_find_counting_direction_down_case1(self):
        data = 0xFFFEFD
        ref_patterns = {'elink0': [0xFD, 0xFE, 0xFF]}
        sliced = slice_ref_patterns(ref_patterns)['elink0']
        self.assertEqual(
            find_counting_direction(sliced, data, 24),
            (-1, 8)
        )

    def test_find_counting_direction_down_case2(self):
        data = 0xFFFFFE
        ref_patterns = {'elink0': [0xFD, 0xFE, 0xFF]}
        sliced = slice_ref_patterns(ref_patterns)['elink0']
        self.assertEqual(
            find_counting_direction(sliced, data, 24),
            (-1, 0)
        )

    def test_find_counting_direction_none(self):
        data = 0x01033C
        ref_patterns = {'elink0': [0xFD, 0xFE, 0xFF]}
        sliced = slice_ref_patterns(ref_patterns)['elink0']
        self.assertEqual(
            find_counting_direction(sliced, data, 24),
            (0, 9)
        )

    def test_check_time_evolution_case1(self):
        parsed_data = [
            {'elink0': 0x03},
            {'elink0': 0x04},
            {'elink0': 0x05},
            {'elink0': 0x06},
            {'elink0': 0x07},
            {'elink0': 0x08},
            {'elink0': 0x09},
            {'elink0': 0x0A},
            {'elink0': 0x0B},
            {'elink0': 0x0C},
            {'elink0': 0x0D},
            {'elink0': 0x0E},
            {'elink0': 0x0F},
            {'elink0': 0x10},
            {'elink0': 0x11},
        ]
        ref_patterns = {
            'elink0': [i for i in range(0, 256)]
        }
        result = check_time_evolution(
            slice_ref_patterns(ref_patterns), parsed_data)
        self.assertEqual(result['elink0']['counting_direction'], 'up')
        self.assertEqual(result['elink0']['counting_length'], 13)
        self.assertEqual(result['elink0']['max_sequence'],
                         [0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B,
                          0x0C, 0x0D, 0x0E, 0x0F])

    def test_check_time_evolution_case2(self):
        parsed_data = [
            {'elink0': 0x09},
            {'elink0': 0x08},
            {'elink0': 0x07},
            {'elink0': 0x06},
            {'elink0': 0x05},
            {'elink0': 0x04},
            {'elink0': 0x03},
            {'elink0': 0x02},
            {'elink0': 0x01},
        ]
        ref_patterns = {
            'elink0': [i for i in range(0, 256)]
        }
        result = check_time_evolution(
            slice_ref_patterns(ref_patterns), parsed_data)
        self.assertEqual(result['elink0']['counting_direction'], 'down')
        self.assertEqual(result['elink0']['counting_length'], 7)
        self.assertEqual(result['elink0']['max_sequence'],
                         [0x09, 0x08, 0x07, 0x06, 0x05, 0x04, 0x03])

    def test_check_time_evolution_case3(self):
        parsed_data = [
            {'elink0': 0x09},
            {'elink0': 0x08},
            {'elink0': 0x07},
            {'elink0': 0x01},
            {'elink0': 0x01},
            {'elink0': 0x01},
            {'elink0': 0x02},
            {'elink0': 0x03},
            {'elink0': 0x04},
        ]
        ref_patterns = {
            'elink0': [i for i in range(0, 256)]
        }
        result = check_time_evolution(
            slice_ref_patterns(ref_patterns), parsed_data)
        self.assertEqual(result['elink0']['counting_direction'], 'up')
        self.assertEqual(result['elink0']['counting_length'], 2)
        self.assertEqual(result['elink0']['max_sequence'],
                         [0x01, 0x02])

    def test_check_time_evolution_case4(self):
        parsed_data = [
            {'elink0': 0x1A},
            {'elink0': 0x2C},
            {'elink0': 0x3C},
            {'elink0': 0x01},
            {'elink0': 0x04},
            {'elink0': 0xFE},
            {'elink0': 0xAA},
            {'elink0': 0xD2},
            {'elink0': 0x2B},
        ]
        ref_patterns = {
            'elink0': [i for i in range(0, 256)]
        }
        result = check_time_evolution(
            slice_ref_patterns(ref_patterns), parsed_data)
        self.assertEqual(result['elink0']['counting_direction'], 'none')
        self.assertEqual(result['elink0']['counting_length'], 0)
        self.assertEqual(result['elink0']['max_sequence'], [])

    def test_check_time_evolution_case5(self):
        parsed_data = [
            {'elink4': 0x1C},
            {'elink4': 0x2C},
            {'elink4': 0x3C},
            {'elink4': 0x4C},
            {'elink4': 0x5C},
            {'elink4': 0x6C},
            {'elink4': 0x7C},
            {'elink4': 0x8C},
            {'elink4': 0x9C},
        ]
        ref_patterns = {
            'elink4': [i for i in range(0, 256)]
        }
        result = check_time_evolution(
            slice_ref_patterns(ref_patterns), parsed_data)
        self.assertEqual(result['elink4']['counting_direction'], 'up')
        self.assertEqual(result['elink4']['counting_length'], 7)
        self.assertEqual(result['elink4']['max_sequence'],
                         [0x1C, 0x2C, 0x3C, 0x4C, 0x5C, 0x6C, 0x7C])
        self.assertEqual(result['elink4']['badness'],
                         [4, 4, 4, 4, 4, 4, 4])

    def test_check_time_evolution_case6(self):
        parsed_data = [
            {'elink4': 0x03},
            {'elink4': 0x04},
            {'elink4': 0x05},
            {'elink4': 0x06},
            {'elink4': 0x07},
            {'elink4': 0x08},
            {'elink4': 0x09},
            {'elink4': 0x0A},
            {'elink4': 0x0B},
            {'elink4': 0x0C},
            {'elink4': 0x0D},
            {'elink4': 0x0E},
            {'elink4': 0x0F},
            {'elink4': 0x10},
            {'elink4': 0x11},
            {'elink4': 0x12},
            {'elink4': 0x13},
            {'elink4': 0x14},
            {'elink4': 0x15},
            {'elink4': 0x16},
            {'elink4': 0x17},
            {'elink4': 0x18},
            {'elink4': 0x19},
            {'elink4': 0x0A},
            {'elink4': 0x1B},
            {'elink4': 0x0C},
            {'elink4': 0x0C},
            {'elink4': 0x0E},
            {'elink4': 0x0F},
            {'elink4': 0x10},
            {'elink4': 0x10},
            {'elink4': 0x91},
            {'elink4': 0x11},
            {'elink4': 0x92},
            {'elink4': 0x12},
        ]
        ref_patterns = {
            'elink4': [i for i in range(0, 256)]
        }
        result = check_time_evolution(
            slice_ref_patterns(ref_patterns), parsed_data)
        self.assertEqual(result['elink4']['counting_direction'], 'up')
        self.assertEqual(result['elink4']['counting_length'], 22)
        self.assertEqual(result['elink4']['max_sequence'],
                         [i for i in range(3, 0x19)])


if __name__ == '__main__':
    unittest.main()
