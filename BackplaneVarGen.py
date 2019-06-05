#!/usr/bin/env python
'''
@author: Yipeng Sun
@license: BSD 2-clause
'''

import sys
import re

from pathlib import Path


input_dir = Path('input')
output_dir = Path('output')

spec_dir = Path('backplane_{}-{}'.format(sys.argv[1], sys.argv[2]))

bom_files = list((input_dir / spec_dir).glob('*bom.asc'))
pnp_files = list((input_dir / spec_dir).glob('*mounter*.asc'))


###########
# Helpers #
###########

class CompRepDel(object):
    def __init__(self, input_file, output_dir,
                 replacement_rules=None,
                 depopulation_rules=None, deletion_rules=None,
                 suffix='.asc'):
        self.input_file = input_file
        self.output_dir = output_dir
        self.create_dir(output_dir)

        self.output_file = self.output_dir / (self.input_file.stem+suffix)

        self.replacement_rules = replacement_rules
        self.depopulation_rules = depopulation_rules
        self.deletion_rules = deletion_rules

    def do(self):
        with open(self.input_file, 'r') as src, \
                open(self.output_file, 'w') as dst:
            for line in src:
                for f in (self.depopulate, self.replace, self.delete):
                    line = f(line)
                dst.write(line)

    def replace(self, line):
        if self.replacement_rules is not None:
            for bom_id, man_id in self.replacement_rules:
                line = re.sub(bom_id, man_id, line)
        return line

    def depopulate(self, line):
        if self.depopulation_rules is not None:
            for comp, bom_id, man_id in self.depopulation_rules:
                if bool(re.match(comp, line)):
                    line = re.sub(bom_id, man_id, line)
        return line

    def delete(self, line):
        if self.deletion_rules is not None:
            for pattern in self.deletion_rules:
                if bool(re.match(pattern, line)):
                    line =  ''
        return line

    @staticmethod
    def create_dir(path):
        if not path.exists():
            path.mkdir(parents=True)


################
# Handle Alpha #
################

for f in bom_files:
    handler = CompRepDel(
        f, output_dir / Path(sys.argv[1]) / Path('alpha'),
        replacement_rules=(
            ('R0805_5R6_1%_0.125W_200PPM', 'RC0805FR-075R6L'),
            ('R0402_100R_1%_0.1W_100PPM_50V', 'RK73H1ETTP1000F'),
            ('CC0402_47NF_16V_10%_X7R', 'CC0402KRX7R7BB473'),
            ('CC0402_100NF_16V_10%_X7R', 'EMK105B7104KV-F'),
            ('CC0402_10NF_25V_10%_X7R', 'TMK105B7103KV-F')
        ),
        depopulation_rules=(
            (r'^CxRB_', 'CC0402_47NF_16V_10%_X7R', 'CC0402KRX7R7BB473'),
            (r'^RB_', 'R0402_100R_1%_0.1W_100PPM_50V', 'DNI'),
            (r'^RBSP_', 'R0402_100R_1%_0.1W_100PPM_50V', 'DNI'),
        )
    )
    handler.do()

for f in pnp_files:
    handler = CompRepDel(
        f, output_dir / Path(sys.argv[1]) / Path('alpha'),
        deletion_rules=(r'^RBSP_', r'^RB_')
    )
    handler.do()


###############
# Handle Beta #
###############

for f in bom_files:
    handler = CompRepDel(
        f, output_dir / Path(sys.argv[1]) / Path('beta'),
        replacement_rules=(
            ('R0805_5R6_1%_0.125W_200PPM', 'RC0805FR-075R6L'),
            ('R0402_100R_1%_0.1W_100PPM_50V', 'RK73H1ETTP1000F'),
            ('CC0402_47NF_16V_10%_X7R', 'CC0402KRX7R7BB473'),
            ('CC0402_100NF_16V_10%_X7R', 'EMK105B7104KV-F'),
            ('CC0402_10NF_25V_10%_X7R', 'TMK105B7103KV-F')
        ),
        depopulation_rules=(
            (r'^CxRB_', 'CC0402_47NF_16V_10%_X7R', 'RK73H1ETTP1000F'),
            # Replace the capacitance with resistance. Same for Gamma.
            (r'^CxRB_', 'CAPC1005X55N', 'RESC1005X40N'),
            (r'^CxRB_', '47nF', '100'),
            (r'^RB_', 'R0402_100R_1%_0.1W_100PPM_50V', 'RK73H1ETTP1000F'),
            (r'^RBSP_', 'R0402_100R_1%_0.1W_100PPM_50V', 'DNI'),
        )
    )
    handler.do()

for f in pnp_files:
    handler = CompRepDel(
        f, output_dir / Path(sys.argv[1]) / Path('beta'),
        deletion_rules=(r'^RBSP_', )
    )
    handler.do()


##########################
# Handle Beta SP (Gamma) #
##########################

for f in bom_files:
    handler = CompRepDel(
        f, output_dir / Path(sys.argv[1]) / Path('gamma'),
        replacement_rules=(
            ('R0805_5R6_1%_0.125W_200PPM', 'RC0805FR-075R6L'),
            ('R0402_100R_1%_0.1W_100PPM_50V', 'RK73H1ETTP1000F'),
            ('CC0402_47NF_16V_10%_X7R', 'CC0402KRX7R7BB473'),
            ('CC0402_100NF_16V_10%_X7R', 'EMK105B7104KV-F'),
            ('CC0402_10NF_25V_10%_X7R', 'TMK105B7103KV-F')
        ),
        depopulation_rules=(
            (r'^CxRB_', 'CC0402_47NF_16V_10%_X7R', 'RK73H1ETTP1000F'),
            (r'^CxRB_', 'CAPC1005X55N', 'RESC1005X40N'),
            (r'^CxRB_', '47nF', '100'),
            (r'^RB_', 'R0402_100R_1%_0.1W_100PPM_50V', 'RK73H1ETTP1000F'),
            (r'^RBSP_', 'R0402_100R_1%_0.1W_100PPM_50V', 'RK73H1ETTP1000F'),
        )
    )
    handler.do()

for f in pnp_files:
    handler = CompRepDel(
        f, output_dir / Path(sys.argv[1]) / Path('gamma')
    )
    handler.do()
