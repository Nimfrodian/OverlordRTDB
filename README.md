# The Real Time Database (RTDB) project for Overlord

## Project's Purpose
This aim of the project is to develop a tool that automates the following tasks:

    File Search: Scans the parent project for files matching the naming format [moduleName]_rtdb_vars.h.
    File Generation: Combines the relevant data from these files to generate two common files:
        rtdb.h
        rtdb.c

These generated files, rtdb.h and rtdb.c, will then be utilized by the Direct Memory Access (DMA) server within the parent project.


### This project assumes the following;
1. It is located in the root of the parent project, e.g.,
```
- src
    someCfiles.c
    ...
- lib
  ...
- include
    moduleName1Header.h
    moduleName2Header.h
    moduleName1_rtdb_vars.h
    moduleName2_rtdb_vars.h
    ...
- thisProjectsFolder
```
2. *_rtdb_vars.h files are located in 'include' folder of the parent project
3. the *_rtdb_vars.h files have the following format
```
#ifndef MOD1_RTDB_VARS_H
#define MOD1_RTDB_VARS_H
#include "rtdb.h"
/*
 * note; min, default and max can be left empty if their value is not limited or relevant
 * [varType]    [arrName]                              [SIZE (optional)]; ///< [unit]  [min]  [default]  [max]    [comment]
 */
tS16S        mod1_ti_timeVar_S16;                      ///< [ms]     [-1]               [0]                [120]               time variable
tU32S        mod1_p_prcntArr_U32    [10];              ///< [a]      []                 []                 []                  percent array
#endif
```
5. the use of rtdbT (and connected) files types, as defined and created by the tool
6. Requires Python 3.10 (possibly works with other versions as well)

## Using the tool
The tool should be configured to run as a pre-build task so that it generates the relevant RTDB files for the project compilation unit to use.
It can also be used before compilation to allow the IDE to use the generated variables in suggestions etc.
