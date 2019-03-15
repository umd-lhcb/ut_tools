#!/usr/bin/env python
#
# Authors: Ramond Su, Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Mar 15, 2019 at 01:25 AM -0400

from pathlib import Path

output_dir = Path('gen')


##########
# Output #
##########

# Each csv file requires a different serial number. Here we generate all 20 at
# once.
serial_numbers = ['{0:08b}'.format(n)
                  for n in range(int('00100000', 2), int('00100000', 2)+20)]

csv_preamble = ["260", "10101010"]
csv_epilogue = ["00000000", "01010101"]


def write_to_comet_csv(filename, serial, body, mode='w', eol='\n'):
    with open(filename, mode) as f:
        for row in csv_preamble+[serial]+body+csv_epilogue:
            f.write(row + eol)


############
# Patterns #
############

def fixed_pattern(mode='01010101', length=256):
    return [mode for i in range(0, length)]


def cyclic_pattern(head='00000000', length=256, start_idx=0):
    ref_cyclic_pattern = ['{0:08b}'.format(n)
                          for n in range(int(head, 2), int(head, 2)+length)]
    return ref_cyclic_pattern[start_idx:] + ref_cyclic_pattern[:start_idx]
