#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from comet_tools.CsvParser import regulator_signal_id_for_comet_dcb_mapping
from comet_tools.CsvParser import CsvParser


class CsvParserTester(unittest.TestCase):
    def test_chain_replacement(self):
        reg_exps = [(r'TEST1', '1'), (r'TEST2', '2'), (r'TEST3', '3')]
        self.assertEqual(
            CsvParser.chain_replacement('TEST1_TEST2_TEST3', reg_exps),
            '1_2_3'
        )

    def test_regularize_row(self):
        reg_exps = {'Signal ID':
                    [(r'_1_[N,P]', ''), (r'GBTX_ELK_', ''), (r'_ELKS', '')]}
        regulators = {'Signal ID': regulator_signal_id_for_comet_dcb_mapping}
        self.assertEqual(
            CsvParser.regularize_row(
                {'Signal ID': 'DC0_ELKS.GBTX_ELK_CH0_1_N'},
                reg_exps, regulators
            ),
            {'Signal ID': '1-elink0'}
        )


if __name__ == '__main__':
    unittest.main()
