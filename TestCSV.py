# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 08:42:00 2019

@author: raymo
"""
import csv
import random

"""
This is just reference for how csvData reads inputs.
csvData = [[1], [22], [21], [24]]
"""
## csvData created to hold 256 rows of junk data, csvOpener for the opening commands needed. Data_Line_1 is for holding the byte to fill each line of csvData.

csvData = []
csvOpener = [["Whatever opening commands are needed."],["Whatever opening commands are needed."],["Whatever opening commands are needed."]]
Data_Line_1 = ["01010101"]

## Loop for filling csvData with Data_Line_1
x = 0

while x < 255:
    csvData.append(Data_Line_1)
    x = x + 1
    
## This is just CSV creation. writerows calls the list you want to make append inot the file.


with open("ConfigTestNumbers", 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvOpener)
    writer.writerows(csvData)
    csvFile.close()

"""
Basic psuedo-random input for Data_Line_1. Needs minor tweaking to remove commas inbetween numbers.
while x < 255:
    my_randoms = random.sample(range(100), 8)
    csvData.append(my_randoms)
    x = x + 1
"""