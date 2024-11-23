#ifndef MOD1_RTDB_VARS_H
#define MOD1_RTDB_VARS_H

#include "rtdb.h"

/*
[varType]    [arrName]              [SIZE (optional)]; ///< [unit]   [min]              [default]          [max]               [comment]
*/
tS16S        mod1_ti_timeVar_S16;                      ///< [ms]     [-1]               [0]                [120]               to je najdaljsi komentar kar se ga loh spomnem za tole zadevo
tS16S        mod1_u_voltVar_S16;                       ///< [V]      [-120]             [-1]               [120]               voltage variable
tS32S        mod1_s_statusVar_S32;                     ///< []       [SOME_MIN_STATUS]  [SOME_DEF_STATUS]  [SOME_MAX_STATUS]   status variable
tU8S         mod1_n_speedVar_U8;                       ///< [RPM]    []                 []                 []                  speed variable
tU8S         mod1_n_speedVar2_U8;                      ///< [RPM]    []                 [100]              []                  speed variable
tU32S        mod1_p_prcntArr_U32    [10];              ///< [a]      []                 []                 []                  percent array
tF32S        mod1_t_tempVar_F32;                       ///< [prcnt]  []                 [0.0]              [100.1f]            temperature variable from some sensor

#endif