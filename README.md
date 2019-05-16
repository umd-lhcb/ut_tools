# ut_tools [![Build status](https://travis-ci.com/umd-lhcb/ut_tools.svg?branch=master)](https://travis-ci.com/umd-lhcb)
A collection of COMET tools for various LHCb UT upgrade testings.


## Backplane
### `BackplaneVarGen.py`
Generate BOM and pick-and-place files for the 3 variant of specified backplane
type.

To use:
```
BackplaneVarGen.py <type:true|mirror> <date:20190516>
```


## COMET
### `CsvGen.py`
Generate csv instruction sets to program COMET. For more technical details,
refer to the script source code. Prototyped by Raymond Su.


### `GbtxMemLongestPattern.py`
Find the maximum continuous pattern for each elink based on exported elink
memory files.

To use:
```
GbtxMemLongestPattern.py <date:20190417>
```


### Exported elink memory
The following table lists the DCB+Pathfinder combination on which the data was
taken:

| suffix          | combo         | COMET firmware |
|-----------------|---------------|----------------|
| `20190329`      | `BP03+DCB013` | `v0-0`         |
| `20190401`      | `BP03+DCB008` | `v0-0`         |
| `20190403`      | `BP02+DCB008` | `v0-0`         |
| `20190412`      | `BP03+DCB008` | `v0-1`         |
| `20190412-v0-0` | `BP03+DCB008` | `v0-0`         |
| `20190417`      | `BP03+DCB013` | `v0-1`         |
