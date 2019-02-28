# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 17:01:44 2019

@author: raymo
"""    

import csv

count = list(range(0,256))
x = list(range(0,256))

for n in x:
    x[n] = format(x[n], '08b')


for y in range(0, 20):
    Name = 'nTx_seq_' + str(y) + '.csv'
    ## csvPreamble_Serial = str(BinaryRange[y])
    with open(Name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        for y in count:
            writer.writerow([x[y]])
        csvFile.close()
