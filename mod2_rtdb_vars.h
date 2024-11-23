#ifndef MOD2_RTDB_VARS_H
#define MOD2_RTDB_VARS_H

#include "rtdb.h"

typedef enum
{
    MOD2_STATE_MACHINE_OFF = 0,
    MOD2_STATE_MACHINE_ON,
} mod2_stMachine;

/*
[varType]    [arrName]                 [SIZE (optional)]; ///< [unit]  [min]  [default]                 [max]   [comment]
*/
tS16S        mod2_c_countVar_S16;                         ///< [A]     []     []                        []      counter variable
tS32S        mod2_t_tempVar_S32;                          ///< [b]     []     []                        []      temperature variable
tS32S        mod2_i_currVar_S32;                          ///< [c]     []     []                        []      current variable
tS32S        mod2_x_arrVar_S32         [3];               ///< [degC]  []     []                        []      unspecified array
tES          mod2_st_stateMachine_tE;                     ///< []      []     [MOD2_STATE_MACHINE_OFF]  []      state machine status

#endif