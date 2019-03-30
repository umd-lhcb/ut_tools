# -*- coding: utf-8 -*-
'''
Created on Thu Mar 14 16:16:49 2019

@author: Jorge Ramirez, Nitzan Hirshberg, Raymond Su, Ben Flaggs, Yipeng Sun
@license: BSD 2-clause
'''


###############################
# Generate reference patterns #
###############################

def fixed_pattern(mode=0b01010101, length=256):
    return ['{0:08b}'.format(mode) for n in range(0, length)]


def cyclic_pattern(head=0b00000000, length=256):
    return ['{0:08b}'.format(n) for n in range(head, head+length)]


def ref_fixed_pattern(mode, elinks, length=1000):
    '''Generate a reference fixed pattern.

    Parameters:
        mode (list): A list of integers defining the fixed pattern for each
            egroup.
        elinks (list): A list of str defining the elink names.
        length (int): An integers defining the total length of the generated
            list.

    Note that len(mode) = len(elinks).

    Returns:
        ref_data (list): A list of dictionary. Each dictionary has the following
            form:
                {'elinkA-0': <1-byte int>,
                 'elinkB-1': <1-byte int>,
                 'elinkC-0': <1-byte int>, ...}
    '''
    pass


def ref_cyclic_pattern(head, elinks, period, length=1000):
    '''Generate a reference cyclic pattern.

    Parameters:
        head (list): A list of integers defining the initial pattern for each
            egroup.
        elinks (list): A list of str defining the elink names.
        period (list): A list of integers indicating the period for each egroup.
        length (int): An integers defining the total length of the generated
            list.

    Note that len(head) = len(period) = len(elinks).

    Returns:
        ref_data (list): Same form as defined in 'ref_fixed_pattern'.
    '''
    pass


##############################################
# Check if the parsed data match expectation #
##############################################

def check_match(ref_data, parsed_data):
    '''Check if parsed data matches reference data (expected data).

    Parameters:
        ref_data (list): Same form as defined in 'ref_fixed_pattern'.
        parsed_data (list): Same form as defined in 'ref_fixed_pattern'.

    Returns:
        stats (dict): A dict of dict that summarizes the number of match and
            mismatch, and percentage of match and mismatch for each egroup. The
            return value should have the following form:
                {'elinkA-0': {'num_match': int, 'num_of_mismatch': int,
                             'percent_match': float, 'percent_mismatch': float}
                 'elinkB-1': ...
                }

            Note that only the elinks present in 'ref_data' will be compared.
    '''
    pass


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


def check_shift(ref_data, parsed_data):
    '''Check if parsed data is shifted compared to reference data.

    Parameters:
        ref_data (list): Same form as defined in 'ref_fixed_pattern'.
        parsed_data (list): Same form as defined in 'ref_fixed_pattern'.

    Returns:
        shifts (dict): A dict of list of the following form:
                {'elinkA-0': [int, int, int, ...]
                 'elinkB-1': ...
                }
            each int represents number of bits shifted.

            If it is a mismatch, rather than a shift, the return value is set to
            an integer that is >= 8.

            Note that only the elinks present in 'ref_data' will be compared.
    '''
    pass


def plot_shift(shifts):
    '''Plot the shift value for all elinks.

    Parameters:
        shifts: Same form as defined in 'check_shift'.

    Returns: None
    '''
    pass
