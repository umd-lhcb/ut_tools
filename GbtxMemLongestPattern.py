#!/usr/bin/env python3
'''
@author: Manuel Franco Sevilla
@license: BSD 2-clause
@description: Finds the longest ascending/descending continuous patterns
'''

import sys
import csv
import re

from collections import defaultdict
from sty import fg, ef, rs

from CometTools.GbtxMemParser import GbtxMemParser
from CometTools.GbtxMemAnalyzer import ref_cyclic_pattern
from CometTools.GbtxMemAnalyzer import slice_ref_patterns
from CometTools.GbtxMemAnalyzer import check_time_evolution


# Returns e-link name given a global index. It allows us to modularly change e-
# link order.
# Currently it uses the order directly in files.
def elink_names():
    return ['elink' + str(i) for i in range(0, 12)]


def generate_path_to_all_mem_files(
        path_suffix,
        path_format='input/comet_{0}-{1}/comet_{0}-gbtx{2}.txt',
        comet_types=['a', 'b'],
        gbtx_idx=[i for i in range(1, 7)]):
    return {c: {gbtx: path_format.format(c, path_suffix, gbtx)
                for gbtx in gbtx_idx}
            for c in comet_types}


def parse_mem_file(path):
    parser = GbtxMemParser(path)
    return parser.parse()


def regularize_comet_dcb_mapping(path='input/CometDcbShortMapping.csv'):
    regularized = defaultdict(list)
    with open(path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            elink_id = row['Signal ID']
            elink_id = re.sub(r'_1_[N,P]', '', elink_id)
            elink_id = re.sub(r'GBTX_ELK_', '', elink_id)
            elink_id = re.sub(r'_ELKS', '', elink_id)

            gbtx, elink = elink_id.split('.')
            gbtx = str(int(gbtx[2:]) + 1)
            elink = 'elink' + elink[2:]

            key = gbtx + '-' + elink

            comet_pin = row['COMET FPGA pin']
            comet_pin = re.sub(r'COMET_', '', comet_pin)
            comet_pin = re.sub(r'-IC3', '', comet_pin)

            if regularized[key] == []:
                regularized[key].append(comet_pin)
            else:
                connector, pin = comet_pin.split('-')
                regularized[key].append(pin)

    return regularized


if __name__ == '__main__':
    #################
    # Configuration #
    #################

    slice_size = 2
    data_slice_size = slice_size + 1
    threshold = 5  # Consider an elink alive if it has at least 5 counting bytes

    comet_prefix = sys.argv[1]
    preferred_elink_names = elink_names()

    ##############
    # Validation #
    ##############

    comet_mem_files = generate_path_to_all_mem_files(comet_prefix)
    all_parsed_data = {comet: {gbtx: parse_mem_file(f)
                               for gbtx, f in inner.items()}
                       for comet, inner in comet_mem_files.items()}

    ref_patterns = ref_cyclic_pattern(preferred_elink_names, [1]*12)
    sliced_patterns = slice_ref_patterns(ref_patterns, slice_size=slice_size)
    all_test_results = {comet: {
        gbtx: check_time_evolution(sliced_patterns, data,
                                   data_slice_size=data_slice_size,
                                   slice_size=slice_size)
        for gbtx, data in inner.items()}
        for comet, inner in all_parsed_data.items()}

    final_result = {gbtx: {elink: {
        'from': 'none', 'direction': 'none', 'length': 0}
        for elink in preferred_elink_names} for gbtx in range(1, 7)}

    ##########
    # Output #
    ##########

    for gbtx in range(1, 7):
        for comet in ['a', 'b']:
            for elink in preferred_elink_names:
                counting_length = \
                    all_test_results[comet][gbtx][elink]['counting_length']

                if counting_length > threshold:
                    final_result[gbtx][elink]['from'] = comet

                    final_result[gbtx][elink]['direction'] = \
                        all_test_results[comet][gbtx][elink]['counting_direction']

                    final_result[gbtx][elink]['length'] = counting_length

    elink_counting_directions = [final_result[gbtx][elink]['direction']
                                 for gbtx in range(1, 7)
                                 for elink in preferred_elink_names]
    total_num = 72
    num_counting_up = \
        len(list(filter(lambda x: x == 'up', elink_counting_directions)))
    num_counting_down = \
        len(list(filter(lambda x: x == 'down', elink_counting_directions)))
    num_dead = total_num - num_counting_up - num_counting_down

    comet_dcb_map = regularize_comet_dcb_mapping()
    comet_pins_to_check = []

    print('\nFound {0} e-links counting up, {1} counting down, and {2} dead\n'.format(
        num_counting_up, num_counting_down, num_dead
    ))

    # Printing header with e-link names
    width = 13

    length_of_gbtx = len('GBTx-1')
    print(' '*length_of_gbtx, end='')

    for elink in preferred_elink_names:
        print('{0:>{1}}'.format(elink, width), end='')
    print()

    print('-'*(length_of_gbtx + width*len(preferred_elink_names)))

    for gbtx, elinks in final_result.items():
        print('GBTx-{}'.format(gbtx), end=' ')
        for elink_name, elink_info in elinks.items():
            elink_id = str(gbtx) + '-' + elink_name
            comet_pins = ','.join(comet_dcb_map[elink_id])

            comet = elink_info['from']
            if comet == 'a':
                formatted_comet = fg.blue + ef.bold + \
                    '{:>4}'.format(comet.upper()) + rs.bold_dim + fg.rs
            elif comet == 'b':
                formatted_comet = fg.yellow + ef.bold + \
                    '{:>4}'.format(comet.upper()) + rs.bold_dim + fg.rs
            else:
                formatted_comet = fg.red + ef.bold + \
                    '{:>4}'.format(comet.upper()) + rs.bold_dim + fg.rs
                comet_pins_to_check.append((elink_id, comet_pins))
            print(formatted_comet, end=',')

            direction = elink_info['direction']
            print('{:>4}'.format(direction), end=',')

            length = str(elink_info['length'])
            print('{0:>{1}} '.format(length, width-4-4-1-1-1), end='')
        print()

    print('\nAdditional info for the dead elinks:\n')

    print('{:>9}'.format('elink'), end='  ')
    print('{:>15}'.format('COMET FPGA pins'))
    print('-'*(9 + 15 + 2))

    for row in comet_pins_to_check:
        elink_id, comet_pins = row
        print('{:>9}'.format(elink_id), end='  ')
        print('{:>15}'.format(comet_pins))
