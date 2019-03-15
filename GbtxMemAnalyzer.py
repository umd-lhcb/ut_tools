# -*- coding: utf-8 -*-
'''
Created on Thu Mar 14 16:16:49 2019

@author: Nitzan Hirshberg, Raymond Su, Ben Flaggs
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
    # Need to use imported cyclic_pattern to implement this.
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

def check_shift_single_byte(ref_byte, actual_byte):
    shift = 0

    for i in range(0, 4):
        if actual_byte << i == ref_byte:
            shift = i
            break
        elif actual_byte >> i == ref_byte:
            shift = -i
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

            If it is not a shift, rather a mismatch, the int should be set to an
            integer that is >= 4.

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