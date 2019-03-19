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
        # Egroup ordering: 6-5-4-3-2-1 (will)
        #                  4-3-2-1-6-5 ????
        
        
        default = (245,95)    # placeholder- (245,95) = (F5, 5F)
        egroup_list = []
        egroup_dict = {       # sample egroup_dict, dummy value s
                'egroup0': default,
                'egroup1': default,
                'egroup2': default,
                'egroup3': default,
                'egroup4': default,
                'egroup5': default,
                'egroup6': default
                 }  
    
        for string_of_bytes in raw_data:  # grab each line of bytes
            elinks = []
            for index, byte in enumerate(string_of_bytes):  
                if index % 2 == 0 and not index > 29:  # we will only work with even indices
                    elinks.append((int(string_of_bytes[index:index+2],16), int(string_of_bytes[index+2:index+4],16)))
                    
                    ''' assuming we have string x = "AABBCCDD"
                    (x[0:2] , x[2:4]) = (AA, BB)
                    (x[4:6] , x[6:8]) = (CC, DD) '''
                    
        pass

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



test = GbtxMemParser("samples/mem_mon_table-fixed-20190226.txt")
test.parse()