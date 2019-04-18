#!/usr/bin/env python3
'''
@author: Yipeng Sun
@license: BSD 2-clause
'''

import csv
import re


#############################################
# Regulators for entries in the parsed dict #
#############################################

def regulator_signal_id(signal_id):
    gbtx, elink = signal_id.split('.')
    gbtx = str(int(gbtx[2:]) + 1)
    elink = 'elink' + elink[2:]
    return gbtx + '-' + elink


##########
# Parser #
##########

class CsvParser(object):
    def __init__(self, filename,
                 reg_exps={
                     'Signal ID':
                     [(r'_1_[N,P]', ''), (r'GBTX_ELK_', ''), (r'_ELKS', '')],
                     'COMET FPGA pin':
                     [(r'_1_[N,P]', ''), (r'COMET_', ''), (r'-IC3', '')]},
                 regulators={
                     'Signal ID': regulator_signal_id,
                     'COMET FPGA pin': lambda x: x
                 }
                 ):
        self.filename = filename
        self.reg_exps = reg_exps

    def parse(self):
        parsed_data = []

        with open(self.filename) as f:  # open txt file
            reader = csv.DictReader(f)
            for row in reader:
                self.regularize_row(row, self.reg_exps)
                parsed_data.append(row)

        return parsed_data

    # NOTE: In-place modification
    @classmethod
    def regularize_row(cls, row, reg_exps, regulators):
        for k, v in row.items():
            row[k] = cls.chain_replacement(v, reg_exps[k])
        for k, v in row.items():
            row[k] = regulators[k](v)
        return row

    @staticmethod
    def chain_replacement(name, reg_exps):
        for reg_exp, replacement in reg_exps:
            name = re.sub(reg_exp, replacement, name)
        return name
