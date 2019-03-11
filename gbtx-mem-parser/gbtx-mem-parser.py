"""
Created on Mon Mar 11 12:41:00 2019

@author: JorgeR
"""

def GetData(filepath):  # method will parse a given txt file
    with open(filepath) as file:
         data = file.readlines()  # place each line into a list named 'data'
    
    return data


def PrintLines(memlist):  # debug method
    for line in memlist:
        print(line)
    

###Debug
unparsed_memory = GetData("mem_mon_table-const.txt")
PrintLines(unparsed_memory)

