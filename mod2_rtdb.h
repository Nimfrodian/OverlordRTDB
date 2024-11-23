#ifndef MOD2_RTDB_H
#define MOD2_RTDB_H

#include "rtdb.h"
#include "mod2_rtdb_vars.h"

void mod2_rtdb_init()
{
	rtdb_assign_tS16S(&mod2_c_countVar_S16, MOD2_C_COUNTVAR_S16, VAR_UNIT_A, TS16_MIN, 0, TS16_MAX, "counter variable");
	rtdb_assign_tS32S(&mod2_i_currVar_S32, MOD2_I_CURRVAR_S32, VAR_UNIT_c, TS32_MIN, 0, TS32_MAX, "current variable");
	rtdb_assign_tS32S(&mod2_t_tempVar_S32, MOD2_T_TEMPVAR_S32, VAR_UNIT_b, TS32_MIN, 0, TS32_MAX, "temperature variable");
	rtdb_assign_tS32S(&mod2_x_arrVar_S32[0], MOD2_X_ARRVAR_S32_0, VAR_UNIT_degC, TS32_MIN, 0, TS32_MAX, "unspecified array");
	rtdb_assign_tS32S(&mod2_x_arrVar_S32[1], MOD2_X_ARRVAR_S32_1, VAR_UNIT_degC, TS32_MIN, 0, TS32_MAX, "unspecified array");
	rtdb_assign_tS32S(&mod2_x_arrVar_S32[2], MOD2_X_ARRVAR_S32_2, VAR_UNIT_degC, TS32_MIN, 0, TS32_MAX, "unspecified array");
	rtdb_assign_tES(&mod2_st_stateMachine_tE, MOD2_ST_STATEMACHINE_TE, VAR_UNIT_NONE, TE_MIN, MOD2_STATE_MACHINE_OFF, TE_MAX, "state machine status");
}
#endif
