#!/usr/bin/env python3
'''
@author: Jorge Ramirez, Raymond Su, Ben Flaggs, Yipeng Sun
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

def check_shift_single_byte(expected_byte, parsed_byte):
    '''Check the shift of a single byte.

    Parameters:
        expected_byte (int)
        parsed_byte (int)

    Returns:
        shift (int): Number of right shifts. Note this this is always a
        non-negative integer between 0-8, where 8 indicates error.
    '''
    shift = 8

    expected_byte_two_cycles = '{0:08b}'.format(expected_byte) * 2
    parsed_byte = '{0:08b}'.format(parsed_byte)

    for i in range(0, 8):
        if expected_byte_two_cycles[0+i:8+i] == parsed_byte:
            shift = i
            break

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
                {'elinkN': {'num_match': int, 'num_of_mismatch': int,
                           'percent_match': float, 'percent_mismatch': float}
                 'elinkM': { ... },
                 ...
                }

            Note that only the elinks present in 'ref_values' will be compared.
    '''
    pass


################################################################################
# Check if the time evolution of the parsed data matched reference pattern, up #
# to a shift                                                                   #
################################################################################

def check_time_evolution(ref_patterns, parsed_data):
    '''Check if parsed data is shifted compared to reference data.

    Parameters:
        ref_patterns (dict): Same form as defined in 'ref_cyclic_pattern'.
        parsed_data (list): Same form as defined in 'check_match'.

    Returns:
        result (dict): A dict of list of the following form:
                {'elinkN': ['counting': up|down,
                            'num_of_consecutive_packet', <int>],
                 'elinkN': [ ... ],
                 ...
                }

            Note that only the elinks present in 'ref_patterns' will be
            compared.
    '''
    pass
