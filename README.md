# Comet Tools
In this repository you will find various tools and scripts used in the testing of 

## GBTX-mem-parser
Python code prototyped by Jorge Ramirez to parse through the states of the GBTx's in order to check the consistency between the GBTx's signal and the signal we sent using our generated CSV's.

Future functionality will include analyzing patterns, identifying cyclical values, legal vs illegal states

## COMET-cmd-gen
Python script by Raymond Su to generate csv instruction sets to program COMET. Each CSV consists of 260 lines: 3 "opening" bytes, 256 bytes of data, and 1 "closing" byte, seen below. These 260 lines are packaged into a CSV and then fed into the COMET to establish a pattern that is then sent to the DCB. The opening and closing bytes are always the same- we can control the signal sent to the DCB by changing the 256 bytes of data. The most common signals we send are constant 1111111's, alternating 01010101's, "chunky" 11110011's, and a "ladder" sequence that counts from 0-255 in binary (00000001, 00000010, 00000011, etc). 

###Example CSV 

```
  260                     
  10101010		  #header
  00100000
  --------		  
 256 Lines of Data
  --------
 01010101         #closer

```