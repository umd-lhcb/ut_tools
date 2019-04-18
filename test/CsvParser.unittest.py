#!/usr/bin/env python

import unittest

import sys
sys.path.insert(0, '..')

from CometTools.CsvParser import CsvParser


class CsvParserTester(unittest.TestCase):
    def test_chain_replacement(self):
        reg_exps = [(r'TEST1', '1'), (r'TEST2', '2'), (r'TEST3', '3')]
        self.assertEqual(
            CsvParser.chain_replacement('TEST1_TEST2_TEST3', reg_exps),
            '1_2_3'
        )


if __name__ == '__main__':
    unittest.main()
