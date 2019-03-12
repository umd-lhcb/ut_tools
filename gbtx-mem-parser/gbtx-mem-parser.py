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

def IdentifyBits(bitlist):  # identify unique bits
    uniques = []
    
    for bit in bitlist:
        if bit not in uniques:  # TODO: count each appearance of unique simult.
            uniques.append(bit)
            
    return uniques

def ConvertBits(hexlist, datatype):  # general conversion method
    outputlist = []
    
    if datatype == "int":
        for num in hexlist:
            outputlist.append(int(num, 16))
            
    elif datatype == "bin": 
        for num in hexlist:
            outputlist.append(bin(int(num, 16))[2:])  # remove "0b" with [2:]
    
    else:
        print("Invalid datatype: expected 'int' or 'bin'")
        
    return outputlist

##########Debug Methods##############

def PrintLines(memlist):  # debug method, spits out entire raw list
    for line in memlist:
        print(line)

def main(filepath, x, y):  # standard procedure, run through every method 
    print("\n\nProcessing",filepath,"\n\n")
    data = GetData(filepath)
    bitlist = ExtractBits(6, 7, data)
    uniques = IdentifyBits(bitlist)
    print(uniques,"\n")
    print(ConvertBits(uniques, "bin"),"\n")
    print(ConvertBits(uniques, "int"),"\n")
    
#main("mem_mon_table-const.txt", 6, 7)  # bits are on indices 6 and 7
main("mem_mon_table-cyclic.txt", 6, 7)  # bits are on indices 6 and 7

####### METHODS TO ADD #######
### identify "legal" permutations