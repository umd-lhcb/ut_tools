# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 08:42:00 2019

@author: raymo
"""
import csv

"""
Reference on how CSV reads data
csvData = [[1], [22], [21], [24]]

Opening preamble:
260
10101010
00100000
"""

"""
## Binary Range Generator, for the third line of the preamble.

FileRange = list(range(0,20))
BinaryRange = []
for x in FileRange:
    Number_Binary = "{0:b}".format(FileRange[x])
    BinaryRange.append(Number_Binary)
    
"""

## Kludge

serial_numbers =  [[["00100000"]],[["00100001"]],[["00100010"]],[["00100011"]],
                  [["00100100"]],[["00100101"]],[["00100110"]],[["00100111"]],
                  [["00101000"]],[["00101001"]],[["00101010"]],[["00101011"]],
                  [["00101100"]],[["00101101"]],[["00101110"]],[["00101111"]],
                  [["00110000"]],[["00110001"]],[["00110010"]],[["00110011"]]]

## CSV Preamble, lines 1 and 2 correspond to the two items.
    
csvPreamble = [["260"],["10101010"]]

## CSV "Junk Data" initializer
  
csvData = []
Data_Line_1 = ["01010101"]

## CSV Closer

csvCloser = [["00000000"],["01010101"]] 

## Loop to create csvData list.

"""
Used in regular CSV.
x = 0
while x < 256:
    csvData.append(Data_Line_1)
    x = x + 1

"""

count = list(range(0,256))
x = list(range(0,256))

for n in x:
    x[n] = format(x[n], '08b')


## Look to create 20 CSV files, with preamble.
for y in range(0, 20):
    Name = 'nTx_seq_' + str(y) + '.csv'
    ## csvPreamble_Serial = str(BinaryRange[y])
    with open(Name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvPreamble)
        writer.writerows(serial_numbers[y])
        for z in count:
            writer.writerow([x[z]])
        writer.writerows(csvCloser)
        csvFile.close()
"""
while x < 255:
    my_randoms = random.sample(range(100), 8)
    csvData.append(my_randoms)
    x = x + 1
"""