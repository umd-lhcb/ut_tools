#!/usr/bin/env python3
'''
@author: Raymond Su, Yipeng Sun
@license: BSD 2-clause
'''

from pathlib import Path

from GbtxMemAnalyzer import fixed_pattern, cyclic_pattern

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


######################
# Generate csv files #
######################

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
