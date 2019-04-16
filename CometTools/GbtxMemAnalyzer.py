#!/usr/bin/env python3
'''
@author: Jorge Ramirez, Raymond Su, Ben Flaggs, Yipeng Sun,
         Manuel Franco Sevilla
@license: BSD 2-clause
'''


###############################
# Generate reference patterns #
###############################

def fixed_pattern(mode=0b01010101, length=256):
    return ['{0:08b}'.format(mode) for n in range(0, length)]


def cyclic_pattern(head=0b00000000, length=256, stepsize=1):
    return ['{0:08b}'.format(n) for n in range(head, head+length, stepsize)]


def ref_cyclic_pattern(elinks, stepsizes, heads=None):
    '''Generate a reference cyclic pattern.

    Parameters:
        elinks (list): A list of str defining the elink names.
        stepsizes (list): A list of integers indicating the stepsize for each
            elink.

            For more info about stepsize, go to the definition of
            'cyclic_pattern'.

    Returns:
        ref_patterns (dict): A dictionary of the following form:
            {'elinkN': [<list of int>],
             'elinkM': [<list of int>], ... }
    '''
    ref_patterns = {
        elink: [int(i, 2) for i in cyclic_pattern(stepsize=step)]
        for elink, step in zip(elinks, stepsizes)
    }
    return ref_patterns


########################################
# Check if the parsed data has shifted #
########################################

# Based on Manuel's bitwise operation checking method.
def check_shift(expected, data, length_expected, length_data):
    length = length_data - length_expected

    if length < 0:
        raise ValueError(
            '{} is longer than {} in binary representation'.format(
                expected, data
            ))

    test_pattern = int('0b'+'1'*length_expected, 2)
    checksum = test_pattern & expected

    shift = length
    for s in range(0, length):
        if test_pattern & (data >> s) == checksum:
            shift = s
            break

    return shift


def check_shift_single_byte(expected_byte, parsed_byte):
    '''Check the shift of a single byte.

    Parameters:
        expected_byte (int)
        parsed_byte (int)

    Returns:
        shift (int): Number of right shifts. Note this this is always a
        non-negative integer between 0-8, where 8 indicates error.
    '''
    shift = check_shift(expected_byte, (parsed_byte << 8)+parsed_byte,
                        8, 16)
    return shift


#############################################################
# Check if the parsed data match expectation, up to a shift #
#############################################################

def check_match(ref_values, parsed_data):
    '''Check if parsed data matches reference data (expected data).

    Parameters:
        ref_values (dict): A dictionary of the following form:
            {'elinkN': <int>,
             'elinkM': <int>, ... }
        parsed_data (list): A list of the following form:
            [
                {'elinkN': <int>, 'elinkM': <int>, ... },
                {'elinkN': <int>, 'elinkM': <int>, ... },
                ...
            ]

    Returns:
        result (dict): A dict of dict that summarizes the number of match and
            mismatch, and percentage of match and mismatch for each egroup. The
            return value should have the following form:
                {'elinkN': {'num_of_match': int,
                            'num_of_mismatch': int,
                            'num_of_shifts': int,
                            'percent_match': float,
                            'percent_mismatch': float,
                            'badness': [int]}
                 'elinkM': { ... },
                 ...
                }

            Note that only the elinks present in 'ref_values' will be compared.

            Also, the std of 'badness' is a naive characterization of jitter.
    '''
    result = {}

    for elink, ref_value in ref_values.items():
        badness = [check_shift_single_byte(ref_value, p[elink])
                   for p in parsed_data]

        num_of_data_points = len(badness)

        num_of_mismatch = len([i for i in badness if i == 8])
        num_of_unshifted_match = len([i for i in badness if i == 0])

        num_of_match = num_of_data_points - num_of_mismatch
        num_of_shifts = num_of_match - num_of_unshifted_match

        # NOTE: We use 'round' to workaround machine-precision float issue
        percent_match = round(num_of_match / num_of_data_points, 5)
        percent_mismatch = round(1 - percent_match, 5)

        result[elink] = {
            'num_of_match': num_of_match,
            'num_of_mismatch': num_of_mismatch,
            'num_of_shifts': num_of_shifts,
            'percent_match': percent_match,
            'percent_mismatch': percent_mismatch,
            'badness': badness
        }

    return result


################################################################################
# Check if the time evolution of the parsed data matched reference pattern, up #
# to a shift                                                                   #
################################################################################

def concatenate_bytes(byte_list):
    # NOTE: In 'byte_list', the first element represent the right-most byte in
    # the concatenated byte.
    return sum([byte_list[i] << (8*i) for i in range(0, len(byte_list))])


def find_slicing_idx(current_idx, prev=2, next=2):
    prev_idx = max(0, current_idx - prev)
    next_idx = current_idx + next
    return (prev_idx, next_idx)


def find_counting_direction(ref_pattern, elink, data,
                            length_data=24, **kwargs):
    length_prev = 2 if 'prev' not in kwargs.keys() else kwargs['prev']
    length_next = 2 if 'next' not in kwargs.keys() else kwargs['next']

    for idx in range(0, len(ref_pattern)):
        prev_idx, next_idx = find_slicing_idx(idx, **kwargs)
        prev_slice = [ref_pattern[i][elink] for i in range(idx, prev_idx, -1)]
        next_slice = [ref_pattern[i][elink] for i in range(idx, next_idx)]


def check_time_evolution(ref_patterns, parsed_data,
                         data_slice_size=3, **kwargs):
    '''Check if the time evolution of parsed data is following a reference
    pattern.

    Parameters:
        ref_patterns (dict): Same form as defined in 'ref_cyclic_pattern'.
        parsed_data (list): Same form as defined in 'check_match'.
        match_thresh (float): Consider match only if the percentage of match is
            greater or equal to the value set here
        **kwargs: Additional keyword arguments that will be passed to
            'find_slicing_idx'.

    Returns:
        result (dict): A dict of dict of the following form:
                {'elinkN': {'counting': 'up'|'down'|'none',
                            'num_of_consecutive_packet': int,
                            'badness': [int],
                            'max_counting_pattern': [int]},
                 'elinkN': { ... },
                 ...
                }

            Note that only the elinks present in 'ref_patterns' will be
            compared.
    '''
    result = {}
    counting_direction = {0: 'none', 1: 'up', -1: 'down'}

    for elink, ref_pattern in ref_patterns.items():
        num_of_consecutive_packet = 0
        max_counting_pattern = []
        badness = []

        direction = 0

        for idx in range(0, len(parsed_data)-data_slice_size+1):
            data_slice = [parsed_data[i][elink]
                          for i in range(idx, idx+data_slice_size)]

            for ref_idx in range(0, len(ref_pattern)):
                prev_idx, next_idx = find_slicing_idx(ref_idx, **kwargs)
