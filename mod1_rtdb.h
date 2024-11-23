#ifndef MOD1_RTDB_H
#define MOD1_RTDB_H

#include "rtdb.h"
#include "mod1_rtdb_vars.h"

void mod1_rtdb_init()
{
	rtdb_assign_tS16S(&mod1_ti_timeVar_S16, MOD1_TI_TIMEVAR_S16, VAR_UNIT_ms, -1, 0, 120, "to je najdaljsi komentar kar se ga loh spomnem za tole zadevo");
	rtdb_assign_tS16S(&mod1_u_voltVar_S16, MOD1_U_VOLTVAR_S16, VAR_UNIT_V, -120, -1, 120, "voltage variable");
	rtdb_assign_tS32S(&mod1_s_statusVar_S32, MOD1_S_STATUSVAR_S32, VAR_UNIT_NONE, SOME_MIN_STATUS, SOME_DEF_STATUS, SOME_MAX_STATUS, "status variable");
	rtdb_assign_tU8S(&mod1_n_speedVar2_U8, MOD1_N_SPEEDVAR2_U8, VAR_UNIT_RPM, TU8_MIN, 100, TU8_MAX, "speed variable");
	rtdb_assign_tU8S(&mod1_n_speedVar_U8, MOD1_N_SPEEDVAR_U8, VAR_UNIT_RPM, TU8_MIN, 0, TU8_MAX, "speed variable");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[0], MOD1_P_PRCNTARR_U32_0, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[1], MOD1_P_PRCNTARR_U32_1, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[2], MOD1_P_PRCNTARR_U32_2, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[3], MOD1_P_PRCNTARR_U32_3, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[4], MOD1_P_PRCNTARR_U32_4, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[5], MOD1_P_PRCNTARR_U32_5, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[6], MOD1_P_PRCNTARR_U32_6, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[7], MOD1_P_PRCNTARR_U32_7, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[8], MOD1_P_PRCNTARR_U32_8, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tU32S(&mod1_p_prcntArr_U32[9], MOD1_P_PRCNTARR_U32_9, VAR_UNIT_a, TU32_MIN, 0, TU32_MAX, "percent array");
	rtdb_assign_tF32S(&mod1_t_tempVar_F32, MOD1_T_TEMPVAR_F32, VAR_UNIT_prcnt, TF32_MIN, 0.0, 100.1f, "temperature variable from some sensor");
}
#endif
