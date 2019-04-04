#!/usr/bin/env python3
'''
@author: Manuel Franco Sevilla
@license: BSD 2-clause
@description: Finds the longest ascending/descending continuous patterns
'''

from GbtxMemParser import GbtxMemParser
import sys


# Returns e-link name given a global index. It allows us to modularly change e-
# link order Currently it uses the order directly in files, starting in e-group
# 5 since there is no data in 6
def ElinkNames():
    Enames = []
    for egroup in range(5, -1, -1):
        for bit in range(2):
            Enames.append('elink' + str(egroup) + '-' + str(bit))

    return Enames


# For count = 1 (count = -1) it finds the longest ascending (descending) continuous patterns
# for each e-link in filename
def FindLongestPatterns(filename, count):
    pars = GbtxMemParser(filename)
    file = pars.parse()

    Nelinks = 12
    ENames = ElinkNames()

    lastshift = -1  # Last shift needed to have a continuous pattern

    lastrow2  = [-1]*Nelinks  # Bytes from the row before last
    lastrow   = [-1]*Nelinks  # Bytes from the last row
    lastshift = [-1]*Nelinks  # Last shift needed for a continuous pattern
    nordered  =  [0]*Nelinks  # Current length of continuous pattern
    longest   =  [0]*Nelinks  # Longest continuous pattern for each e-link

    for row in range(len(file)):
        for elink in range(Nelinks):
            dic = file[row]
            ename = ENames[elink]
            val = dic[ename]

            if(lastrow2[elink] >= 0):
                # Putting together the last 3 rows
                rows3 = (lastrow2[elink] << 16) + (lastrow[elink] << 8) + val
                # Searching continuous patters for any shift between 0 and 7
                for shift in range(8):
                    last    = 0xFF & (rows3 >> (16-shift))
                    current = 0xFF & (rows3 >> (8-shift))
                    nextcount = last + count
                    if(nextcount == 0x100):
                        nextcount = 0
                    if(nextcount == -1):
                        nextcount = 0xFF
                    if(current == nextcount):
                        # If the pattern is continuous with the same shift as last continuous pattern,
                        # increase length of continuous pattern
                        if(shift == lastshift[elink]):
                            nordered[elink] += 1
                        else:
                            nordered[elink] = 1
                            lastshift[elink] = shift
                        break
                    # If it does all shifts and does not find a continuous pattern, reset nordered/lastshift
                    if(shift == 7):
                        nordered[elink] = 0
                        lastshift[elink] = -1
                if(nordered[elink] > longest[elink]):
                    longest[elink] = nordered[elink]

            # Filling the last rows for the next iteration
            lastrow2[elink] = lastrow[elink]
            lastrow[elink]  = val

    for ind in range(len(longest)):
        longest[ind] *= count
    return longest


######################################################################################################
# MAIN: Loops over the 12 input files and finds the longest ascending/descending continuous patterns #
######################################################################################################

cometa = []
cometb = []

# Number of e-links countin up, down, or not counting
Nup = 0
Ndown = 0
Ndead = 0
threshold = 10

comets = ['a', 'b']
longestAll = []

for gbtx in range(1, 7):
    dataTakenDate = sys.argv[1]
    longestAll.append([])
    for comet in comets:
        filename = 'input/comet_' + comet + '-{}/comet_'.format(dataTakenDate) + comet + '-gbtx' + str(gbtx) + '.txt'
        longUp   = FindLongestPatterns(filename,  1)
        longDown = FindLongestPatterns(filename, -1)
        maxlong = []
        for ind in range(len(longUp)):
            if(abs(longUp[ind]) > abs(longDown[ind])):
                maxlong.append(longUp[ind])
            else:
                maxlong.append(longDown[ind])
        longestAll[gbtx-1].append(maxlong)
        Nup   += sum(x >=  threshold for x in maxlong)
        Ndown += sum(x <= -threshold for x in maxlong)

    # Finding number of dead links by finding the longest pattern between COMETs a and b
    cometa = list(map(abs, longestAll[gbtx-1][0]))
    cometb = list(map(abs, longestAll[gbtx-1][1]))
    longest = [max(l1, l2) for l1, l2 in zip(cometa, cometb)]
    Ndead += sum(x > -threshold and x < threshold for x in longest)

print('\nFound ' + str(Nup) + ' e-links counting up, ' + str(Ndown) + ' counting down, and ' + str(Ndead) + ' dead\n')

# Printing header with e-link names
width = 10
ENames = ElinkNames()
print(' '*15, end=' ')
for elink in range(len(longestAll[0][0])):
    print(f'{ENames[elink]:>10}', end=' ')
print()

# Printing longest patterns
for gbtx in range(len(longestAll)):
    for comet in range(len(longestAll[gbtx])):
        print('GBTx-'+str(gbtx+1)+', COMET-'+comets[comet], end=" ")
        for elink in range(len(longestAll[gbtx][comet])):
            print(f'{longestAll[gbtx][comet][elink]:>10}', end=" ")
        print()
    print()
