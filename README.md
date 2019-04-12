# comet_tools [![Build status](https://travis-ci.com/umd-lhcb/comet_tools.svg?branch=master)](https://travis-ci.com/umd-lhcb)
A collection of COMET tools for various LHCb UT upgrade testings.


## `GbtxMemAnalyzer.py`
Analyze the elink signal transmission quality by analyze parsed elink tables.


## `GbtxMemParser.py`
Parse through elink tables exported on MiniDAQ. Prototyped by Jorge Ramirez


## `CsvGen.py`
Generate csv instruction sets to program COMET. For more technical details,
refer to the script source code. Prototyped by Raymond Su.


## Exported elink memory
The following table lists the DCB+Pathfinder combination on which the data was
taken:

| date       | combo         | COMET firmware |
|------------|---------------|----------------|
| `20190329` | `BP03+DCB013` | `original`     |
| `20190401` | `BP03+DCB008` | `original`     |
| `20190403` | `BP02+DCB008` | `original`     |
| `20190412` | `BP02+DCB008` | `f45b0e`       |
