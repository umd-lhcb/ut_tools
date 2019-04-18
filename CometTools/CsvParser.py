#!/usr/bin/env python3
'''
@author: Yipeng Sun
@license: BSD 2-clause
'''

import csv
import re

from collections import defaultdict


class CsvParser(object):
    def __init__(self, filename, keyname='Signal ID',
                 keyname_regularization=lambda x: x,
                 regularizations={
                     'Signal ID': [(r'_1_[N,P]', ''), (r'GBTX_ELK_', ''),
                                   (r'_ELKS', '')]
                 }):
        self.filename = filename
        self.keyname = keyname
        self.keyname_regularization = keyname_regularization
        self.regularizations = regularizations

    def parse(self):
        parsed_data = defaultdict(list)

        with open(self.filename) as f:  # open txt file
            reader = csv.DictReader(f)
            for row in reader:
                self.regularize_row(row)
                parsed_data.append(row)

        return parsed_data

    # NOTE: In-place modification
    def regularize_row(cls, row):
        pass

    @staticmethod
    def chain_replacement(name, reg_exps):
        for reg_exp, replacement in reg_exps:
            name = re.sub(reg_exp, replacement, name)
        return name
