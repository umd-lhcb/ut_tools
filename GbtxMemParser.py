#!/usr/bin/env python
'''
Created on Mon Mar 11 12:41:00 2019

@author: Jorge Ramirez
@license: BSD 2-clause
'''


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
        elink_dict = {       # sample egroup_dict, dummy values
                 'elink0-0': default,
                 'elink0-1': default,
                 'elink1-0': default,
                 'elink1-1': default,
                 'elink2-0': default,
                 'elink2-1': default,
                 'elink3-0': default,
                 'elink3-1': default,
                 'elink4-0': default,
                 'elink4-1': default,  # key[5] = 4, key[7] = 1 : elink identifiers
                 'elink5-0': default, 
                 'elink5-1': default,
                 'elink6-0': default,
                 'elink6-1': default,
                 }  
    
        # begin by looping through every line in the memory file        
        for string_of_hexes in raw_data:  # grab each line
            elinks = []  # refresh our list every loop
            
            # extract the data from the line we grabbed, place in list "elinks"
            for index, digit in enumerate(string_of_hexes): 
                # use every even index, skipping the header, and extract 2 digits
                if digit != "\n" and index > 3 and index % 2 == 0:
                    elinks.append(int(string_of_hexes[index:index+2], 16))
                
            # match elink identifiers (keys in dict) to index of each byte
            for key in elink_dict:
                x, y = int(key[5]), int(key[7])  # figure out which elink we have
                for index, elink in enumerate(elinks):
                    # look at every elink and match identifiers to index
                    if index == ((-1)*(2*x + y - 13)):  # magical formula, see comment
                        elink_dict[key] = elink  # found value, save
            
            dict_list.append(elink_dict)  # save our finalized dictionary
            
        
        '''
        0-0 -> index 13
        0-1 -> index 12
        1-0 -> index 11
        1-1 -> index 10
        .
        6-1 -> index 1
        x-y -> index z
        
        it would be easy if 0-0 -> 0, 0-1 -> 1, because then it'd be 2x+y=z
        but since we start at 13, we can subtract 13 and then take the negative
        
        (-1)*(2x+y-13)
        
        Elink ordering: 6 (0,1) ,5 (0,1), 4 (0,1), 3 (0,1), 2 (0,1), 1 (0,1)
          (will)
        
        '''

        return dict_list  

    @staticmethod
    def output_to_csv(filename, parsed_data):
        '''Write parsed memory data to a CSV file.

        Parameters:
            filename (Path or str): Output CSV filename, full path or relative
                path.
            parsed_data (list): Same form as defined in 'parse' method.

        Returns: None
        '''
        pass


# debug
test = GbtxMemParser("samples/mem_mon_table-fixed-20190226.txt")
test.parse()