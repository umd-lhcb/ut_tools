#!/usr/bin/env python3
'''
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
                    {'elink0': <1-byte int>,
                     'elink1': <1-byte int>,
                     'elink2': <1-byte int>,
                     'elink3': <1-byte int>,
                     'elink4': <1-byte int>,
                     'elink5': <1-byte int>,
                     'elink6': <1-byte int>,
                     'elink7': <1-byte int>,
                     'elink8': <1-byte int>,
                     'elink9': <1-byte int>,
                     'elink10': <1-byte int>,
                     'elink11': <1-byte int>}
                Note that the header is removed from the final result.
        '''
        with open(self.filename) as f:  # open txt file
            raw_data = f.readlines()    # create list "raw_data" from file

        return self.dissect_str_to_dict(raw_data)

    @classmethod
    def dissect_str_to_dict(cls, raw_data):
        '''Take a list of string, dissecting them to list of dictionary.

        Parameters:
            raw_data (list): A list of str, each str is a single line in the
                memory monitoring file.

        Returns:
            parsed_data (list): Same form as defined in 'parse' method.
                This is the normal output of the parser.
        '''
        elink_idx_map = cls.elink_channel_idx_mapping()
        parsed_data = []

        for raw_packet in raw_data:
            parsed_packet = {}
            for elink, idx in elink_idx_map.items():
                idx = len(raw_packet) - idx
                parsed_packet[elink] = int(raw_packet[idx-2:idx], 16)
            parsed_data.append(parsed_packet)

        return parsed_data

    @staticmethod
    def elink_channel_idx_mapping():
        '''Define the mapping between elink channel name to its byte index in
        the GBTx frame.

        Counting from right: idx 0 -> rightmost.
        '''
        return {
            'elink0': 2,
            'elink1': 0,
            'elink2': 6,
            'elink3': 4,
            'elink4': 10,
            'elink5': 8,
            'elink6': 14,
            'elink7': 12,
            'elink8': 18,
            'elink9': 16,
            'elink10': 22,
            'elink11': 20
        }

    @staticmethod
    def output_to_csv(parsed_data, filename="gen/parsed_elinks.csv"):
        '''Write parsed memory data to a CSV file.

        Parameters:
            parsed_data (list): Same form as defined in 'parse' method.
            filename (Path or str): Output CSV filename, full path or relative
                path.

        Returns: None
        '''
        csv_headers = list(parsed_data[0].keys())  # get keys for csv headers

        with open(filename, 'w', newline='') as csvfile:  # open csv file
            # use csv.DictWriter to convert Dict to CSV
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()  # write headers

            for elink_dict in parsed_data:   # work on a dict by dict basis
                writer.writerow(elink_dict)  # write each dict onto a single row
