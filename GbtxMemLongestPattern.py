#!/usr/bin/env python3
'''
@author: Manuel Franco Sevilla
@license: BSD 2-clause
@description: Finds the longest ascending/descending continuous patterns
'''

import sys

from sty import fg, bg, ef, rs

from CometTools.GbtxMemParser import GbtxMemParser
from CometTools.GbtxMemAnalyzer import ref_cyclic_pattern
from CometTools.GbtxMemAnalyzer import check_time_evolution


# Returns e-link name given a global index. It allows us to modularly change e-
# link order Currently it uses the order directly in files, starting in e-group
# 5 since there is no data in 6
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


if __name__ == '__main__':
    comet_prefix = sys.argv[1]

    elinks = elink_names()
    comet_mem_files = generate_path_to_all_mem_files(comet_prefix)

    all_parsed_data = {comet: {gbtx: parse_mem_file(f)
                               for gbtx, f in inner.items()}
                       for comet, inner in comet_mem_files.items()}

    ref_patterns = ref_cyclic_pattern(elinks, [1]*12)
    all_test_results = {comet: {gbtx: check_time_evolution(ref_patterns, data)
                                for gbtx, data in inner.items()}
                        for comet, inner in all_parsed_data.items()}

    threshold = 5  # Consider an elink alive if it has at least 5 counting bytes
    final_result = {gbtx: {elink: {'from': 'none', 'direction': 'none',
                                   'length': 0}
                           for elink in elink_names()}
                    for gbtx in range(1, 7)}

    for gbtx in range(1, 7):
        for comet in ['a', 'b']:
            for elink in elink_names():
                final_result[gbtx][elink]['length'] = \
                    all_test_results[comet][gbtx][elink]['counting_length']
                if all_test_results[comet][gbtx][elink]['counting_length'] > \
                        threshold:
                    final_result[gbtx][elink]['from'] = comet

                    final_result[gbtx][elink]['direction'] = \
                        all_test_results[comet][gbtx][elink]['counting_direction']

    elink_counting_directions = [final_result[gbtx][elink]['direction']
                                 for gbtx in range(1, 7)
                                 for elink in elink_names()]
    total_num = 72
    num_counting_up = \
        len(list(filter(lambda x: x == 'up', elink_counting_directions)))
    num_counting_down = \
        len(list(filter(lambda x: x == 'down', elink_counting_directions)))
    num_dead = total_num - num_counting_up - num_counting_down

    print('\nFound {0} e-links counting up, {1} counting down, and {2} dead\n'.format(
        num_counting_up, num_counting_down, num_dead
    ))

    # Printing header with e-link names
    width = 13

    length_of_gbtx = len('GBTx-1')
    print(' '*length_of_gbtx, end=' ')

    for elink in elink_names():
        print('{0:>{1}}'.format(elink, width), end='')
    print()

    print('-'*(1 + length_of_gbtx + width*len(elink_names())))

    for gbtx, elinks in final_result.items():
        print('GBTx-{}'.format(gbtx), end=' ')
        for _, elink_info in elinks.items():
            comet = elink_info['from']
            if comet == 'a':
                formatted_comet = bg.blue + ef.bold + \
                    '{:>4}'.format(comet.upper()) + rs.bold_dim + bg.rs
            elif comet == 'b':
                formatted_comet = bg.yellow + ef.bold + \
                    '{:>4}'.format(comet.upper()) + rs.bold_dim + bg.rs
            else:
                formatted_comet = bg.red + ef.bold + \
                    '{:>4}'.format(comet.upper()) + rs.bold_dim + bg.rs
            print(formatted_comet, end=',')

            direction = elink_info['direction']
            print('{:>4}'.format(direction), end=',')

            length = str(elink_info['length'])
            print('{0:>{1}} '.format(length, width-4-4-1-1-1), end='')
        print()
