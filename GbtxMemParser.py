#!/usr/bin/env python
'''
Created on Mon Mar 11 12:41:00 2019

@author: Jorge Ramirez
@license: BSD 2-clause
'''


class GbtxMemParser(object):
    def __init__(filename):
        self.filename = filename

    def parse(self):
        '''Parse the supplied filename and return a list of dictionary.'''
        with open(self.filename) as f:
            pass

    @staticmethod
    def dissect_str_to_dict(raw_data):
        '''Take a list of string, dissecting them to list of dictionary.

        The list of dictionaries should have the following form:
            [
                {'header':  <2-byte int data>,
                 'egroup0': <2-byte int data>,
                 'egroup1': <2-byte int data>,
                 'egroup2': <2-byte int data>,
                 'egroup3': <2-byte int data>,
                 'egroup4': <2-byte int data>,
                 'egroup5': <2-byte int data>,
                 'egroup6': <2-byte int data>,
                }
            ]

        This is the normal output of the parser.
        '''
        pass

    @staticmethod
    def output_to_csv(filename, parsed_data):
        '''Write parsed memory data to a CSV file'''
        pass


def GetData(filepath):  # method will parse a given txt file path
    with open(filepath) as file:
         data = file.readlines()  # place each line into a list named 'data'
    return data


def ExtractBits(x, y, memlist):  # returns the xth and yth digits
    bitlist = []

    for line in memlist:
        bitlist.append(line[x-1:y])

    return bitlist


#####################################################
############ Method sent to the Analyzer ############
#####################################################
def PrepAnalyzer(filepath):

    x = 7   # assuming locations do not change, this is where the bits are
    y = 8
    raw_data = GetData(filepath)                  # import data from csv
    processed_data = ExtractBits(x, y, raw_data)  # take out hexes from csv

    return processed_data
#####################################################
#####################################################
#####################################################


#####################################################
##################  Debug Methods  ##################
#####################################################

def PrintLines(memlist):  # debug method, spits out entire raw list
    for line in memlist:
        print(line)


def maindebug(filepath, x, y):  # standard procedure, run through every method
    print("\n\nProcessing",filepath,"\n\n")
    data = GetData(filepath)                # import data from csv
    bitlist = ExtractBits(x, y, data)       # take out hexadecimal bits from csv
    print(bitlist)
    print("\n")

#maindebug("mem_mon_table-const.txt", 7, 8)  # bits are on indices 6 and 7
#maindebug("mem_mon_table-cyclic.txt", 7, 8)  # bits are on indices 6 and 7
