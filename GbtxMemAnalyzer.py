# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:16:49 2019

@author: Jorge R, Nitzan H, Ben F, Raymond S
@license: BSD 2-clause
"""

from .csv-gen import

##############################
# Generate reference results #
##############################

def ref_fixed_pattern()



def IdentifyBits(bitlist):  # identify unique bits in given array
    uniques = []

    for bit in bitlist:
        if bit not in uniques:  # TODO: count each appearance of unique simult.
            uniques.append(bit)

    return uniques


def ConvertBits(hexlist, datatype):  # convert entire array
    outputlist = []

    if datatype == "int":
        for num in hexlist:
            outputlist.append(int(num, 16))

    elif datatype == "bin":
        for num in hexlist:
            outputlist.append(bin(int(num, 16))[2:].zfill(8))
                # remove "0b" with [2:], add leading 0's

    else:
        print("Invalid datatype: expected 'int' or 'bin'")

    return outputlist



def Histogram():



    return
