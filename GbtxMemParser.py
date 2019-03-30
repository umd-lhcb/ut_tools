#!/usr/bin/env python
'''
Created on Mon Mar 11 12:41:00 2019

@author: Jorge Ramirez
@license: BSD 2-clause
'''

import csv


class GbtxMemParser(object):
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        '''Parse the supplied filename and return a list of dictionary.

        Parameters: None

        Returns:
            parsed_data (list): A list of dictionary. Each dictionary has the
                following form:
                    {'elink0-0': <1-byte int>,
                     'elink0-1': <1-byte int>,
                     'elink1-0': <1-byte int>,
                     'elink1-1': <1-byte int>,
                     'elink2-0': <1-byte int>,
                     'elink2-1': <1-byte int>,
                     'elink3-0': <1-byte int>,
                     'elink3-1': <1-byte int>,
                     'elink4-0': <1-byte int>,
                     'elink4-1': <1-byte int>,
                     'elink5-0': <1-byte int>,
                     'elink5-1': <1-byte int>,
                     'elink6-0': <1-byte int>,
                     'elink6-1': <1-byte int>}
                Note that the header is removed from the final result.
        '''
        with open(self.filename) as f:  # open txt file
            raw_data = f.readlines()    # create list "raw_data" from file

        return self.dissect_str_to_dict(raw_data)

    @staticmethod
    def dissect_str_to_dict(raw_data):
        '''Take a list of string, dissecting them to list of dictionary.

        Parameters:
            raw_data (list): A list of str, each str is a single line in the
                memory monitoring file.

        Returns:
            parsed_data (list): Same form as defined in 'parse' method.
                This is the normal output of the parser.
        '''

        default = (204)    # placeholder- (204) = (CC)
        dict_list = []
        sample_dict = {       # sample egroup_dict, dummy values
            'elink6-0': default,
            'elink6-1': default,
            'elink5-0': default,
            'elink5-1': default,
            'elink4-0': default,
            'elink4-1': default,
            'elink3-0': default,
            'elink3-1': default,
            'elink2-0': default,  # elink identifiers (strings)
            'elink2-1': default,  # key[5] = 2, key[7] = 1
            'elink1-0': default,
            'elink1-1': default,
            'elink0-0': default,
            'elink0-1': default,
        }

        # Elink ordering: 6 (0,1) ,5 (0,1), 4 (0,1), 3 (0,1), 2 (0,1), 1 (0,1),
        #                 0 (0,1)

        # begin by looping through every line in the data file
        for string_of_hexes in raw_data:
            unsorted_elinks = []  # make sure to refresh our list every loop
            elink_dict = sample_dict.copy()  # refresh dict every loop

            # extract the data from the line we grabbed, sort into elinks
            for index, digit in enumerate(string_of_hexes):

                # use every even index, skipping the header (indices 0-3),
                # and extract that index and the next one which we convert to decimal.
                # every line has a pesky "\n" at the end so we remove it
                if digit != "\n" and index > 3 and index % 2 == 0:
                    unsorted_elinks.append(int(string_of_hexes[index:index+2], 16))

            # match each key in the sample dictionary to its correct index
            for key in elink_dict:
                x, y = int(key[5]), int(key[7])  # see sample dict

                # use magic formula to match values to keys... see comment below
                for index, value in enumerate(unsorted_elinks):
                    if index == (2*(6-x)+y):  # magic formula
                        elink_dict[key] = value  # found match

            dict_list.append(elink_dict)  # save our finalized dictionary into list

        return dict_list  # after we loop through every line, return our list

        '''
        0-0 -> index 12
        0-1 -> index 13
        1-0 -> index 10
        1-1 -> index 11
        ...
        5-0 -> index 2
        5-1 -> index 3
        6-0 -> index 1
        6-1 -> index 0

        x-y -> index z
        z = (2(6-x) + y)

        see github issue 8 (https://github.com/umd-lhcb/comet_tools/issues/8)
        for explanation on magic formula

        '''

    @staticmethod
    def output_to_csv(parsed_data, filename="gen/parsed_elinks.csv"):
        '''Write parsed memory data to a CSV file.

        Parameters:
            filename (Path or str): Output CSV filename, full path or relative
                path.
            parsed_data (list): Same form as defined in 'parse' method.

        Returns: None
        '''

        if filename == "exports/unnamed.csv":  # test if no name given
            print("\nFilepath unspecificed. Defaulting to", filename, "\n")

        csv_headers = list(parsed_data[0].keys())  # get keys for csv headers
        with open(filename, 'w', newline='') as csvfile:  # open csv file
            # use csv.DictWriter to convert Dict to CSV
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()  # write headers

            for elink_dict in parsed_data:   # work on a dict by dict basis
                writer.writerow(elink_dict)  # write each dict onto a single row

        return
