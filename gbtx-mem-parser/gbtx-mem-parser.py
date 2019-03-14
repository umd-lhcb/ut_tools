"""
Created on Mon Mar 11 12:41:00 2019

@author: JorgeR
"""

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


# raw txt file

