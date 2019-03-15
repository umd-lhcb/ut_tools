#!/usr/bin/env python
'''
Created on Wed Jan 23 08:42:00 2019

@author: Raymond Su, Yipeng Sun
@license: BSD 2-clause
'''

from pathlib import Path

output_dir = Path('gen')


##########
# Output #
##########

# Each csv file requires a different serial number. Here we generate all 20 at
# once.
serial_numbers = ['{0:08b}'.format(n)
                  for n in range(0b00100000, 0b00100000+20)]

csv_preamble = ["260", "10101010"]
csv_epilogue = ["00000000", "01010101"]


def write_to_comet_csv(filename, serial, body, mode='w', eol='\n'):
    with open(filename, mode) as f:
        for row in csv_preamble+[serial]+body+csv_epilogue:
            f.write(row + eol)


############
# Patterns #
############

def fixed_pattern(mode=0b01010101, length=256):
    return ['{0:08b}'.format(mode) for n in range(0, length)]


def ref_cyclic_pattern(head, length):
    return ['{0:08b}'.format(n) for n in range(head, head+length)]


def cyclic_pattern(head=0b00000000, length=256, offset=0):
    ref_pattern = ref_cyclic_pattern(head, length)
    return ref_pattern[offset:] + ref_pattern[:offset]


######################
# Generate csv files #
######################

if __name__ == '__main__':
    for idx in range(0, 20):
        # Fixed pattern
        write_to_comet_csv(
            output_dir / Path('fixed') / Path('nTx_seq_{}.csv'.format(idx)),
            serial_numbers[idx],
            fixed_pattern()
        )

        # Cyclic pattern
        write_to_comet_csv(
            output_dir / Path('cyclic') / Path('nTx_seq_{}.csv'.format(idx)),
            serial_numbers[idx],
            cyclic_pattern()
        )
