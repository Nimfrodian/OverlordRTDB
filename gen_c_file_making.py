import re
import time

at = ["tU8S",   # all types
      "tU16S",
      "tU32S",
      "tS8S",
      "tS16S",
      "tS32S",
      "tES",
      "tBS",
      "tF32S",]

bt = {  # base type
  "tU8S": "tU8",
  "tU16S": "tU16",
  "tU32S": "tU32",
  "tS8S": "tS8",
  "tS16S": "tS16",
  "tS32S": "tS32",
  "tES": "tE",
  "tBS": "tB",
  "tF32S": "tF32",
}

def to_all_caps(text):
    new_text = text.upper()
    new_text = new_text.replace("[","_")
    new_text = new_text.replace("]","")
    return new_text

def sorted_nicely(l, key=lambda x: x):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=lambda item: alphanum_key(key(item)))

def assign_aux_data(file, var, var_type):
    if var.unit == '':
        file.write(', VAR_UNIT_NONE')
    else:
        file.write(f', VAR_UNIT_{var.unit}')
    if var.min == '':
        file.write(f', {to_all_caps(bt[var_type])}_MIN')
    else:
        file.write(f', {var.min}')
    if var.default == '':
        file.write(f', 0')
    else:
        file.write(f', {var.default}')
    if var.max == '':
        file.write(f', {to_all_caps(bt[var_type])}_MAX')
    else:
        file.write(f', {var.max}')
    if var.comment == '':
        file.write(f', "/"')
    else:
        file.write(f', "{var.comment}"')
    file.write(');\n')

def write_autogenerated_header(file):
    file.write('/*\n')
    file.write(' * This file was autogenerated by RTDB Generator script\n')
    file.write(f' * Date of generation: {time.strftime("%d %B %Y")} at {time.strftime("%H:%M:%S")}\n')
    file.write(' * To modify this file run the RTDB Generator script again\n')
    file.write(' */\n\n')

def write_module_rtdb(module_name, file_path, variables):
    with open(file_path, 'w') as file:
        write_autogenerated_header(file)
        file.write(f"#ifndef {module_name.upper()}_RTDB_H\n")
        file.write(f"#define {module_name.upper()}_RTDB_H\n\n")

        file.write(f"#include \"rtdb.h\"\n")
        file.write(f"#include \"{module_name}_rtdb_vars.h\"\n\n")

        file.write(f"void {module_name}_rtdb_init()\n")
        file.write("{\n")
        for var_type,var_list in variables.items():
            for var in sorted_nicely(var_list, key=lambda var: var.name):
                if var.arrSize == '':
                    file.write(f'    rtdb_assign_{var_type}(&{var.name}, {to_all_caps(var.name)}')
                    assign_aux_data(file, var, var_type)
                else:
                    for i in range(0,int(var.arrSize)):
                        file.write(f'    rtdb_assign_{var_type}(&{var.name}[{i}], {to_all_caps(var.name)}_{i}')
                        assign_aux_data(file,var, var_type)
        file.write("}\n")

        file.write(f"#endif\n")


def write_rtdb_vars_h(variables):
    counter = 0
    with open('include/rtdb_vars.h', 'w') as file:
        write_autogenerated_header(file)
        file.write("#ifndef RTDB_VARS_H\n")
        file.write("#define RTDB_VARS_H\n\n")
        file.write("#include<limits.h>\n")
        file.write("#include<stdint.h>\n")
        file.write("#include<float.h>\n\n")

        file.write("#define TU8_MIN (0)\n")
        file.write("#define TU8_MAX (UCHAR_MAX)\n")
        file.write("#define TU16_MIN (0)\n")
        file.write("#define TU16_MAX (USHRT_MAX)\n")
        file.write("#define TU32_MIN (0)\n")
        file.write("#define TU32_MAX (UINT_MAX)\n")
        file.write("#define TS8_MIN (SCHAR_MIN)\n")
        file.write("#define TS8_MAX (SCHAR_MAX)\n")
        file.write("#define TS16_MIN (SHRT_MIN)\n")
        file.write("#define TS16_MAX (SHRT_MAX)\n")
        file.write("#define TS32_MIN (INT_MIN)\n")
        file.write("#define TS32_MAX (INT_MAX)\n")

        file.write("#define TB_MIN (0)\n")
        file.write("#define TB_MAX (1)\n")
        file.write("#define TE_MIN (0)\n")
        file.write("#define TE_MAX (TU32_MAX)\n")
        file.write("#define TF32_MIN (FLT_MIN)\n")
        file.write("#define TF32_MAX (FLT_MAX)\n\n")

        file.write("typedef uint8_t tU8;\n")
        file.write("typedef uint16_t tU16;\n")
        file.write("typedef uint32_t tU32;\n")
        file.write("typedef int8_t tS8;\n")
        file.write("typedef int16_t tS16;\n")
        file.write("typedef int32_t tS32;\n")
        file.write("typedef tU8 tB;\n")
        file.write("typedef tU32 tE;\n")
        file.write("typedef float tF32;\n\n")

        file.write("// Variable units lookup table and enum\n")
        file.write('typedef enum\n')
        file.write('{\n')
        first = 1
        printed_units = set()
        for var_type,var_list in variables.items():
            for var in var_list:
                if var.unit not in printed_units:
                    printed_units.add(var.unit)

        nicelySortedUnits = sorted(printed_units)
        for unit in nicelySortedUnits:
            file.write(f'    VAR_UNIT_{(unit)}')
            if unit == '':
                file.write('NONE')
            if first:
                first = 0
                file.write(' = 0')
            file.write(',\n')
        file.write('    VAR_UNIT_MAX_NUM\n')
        file.write('} unitEnumT;\n\n')

        for var_type_at in at:
            file.write(f'// {var_type_at}\n')
            file.write('typedef enum\n{\n')
            if var_type_at in variables:
                counter = 0
                for var in sorted_nicely(var_list, key=lambda var: var.name):
                    if var.arrSize == '':
                        file.write(f'    {to_all_caps(var.name)} = {counter},\n')
                        counter = counter + 1
                    else:
                        for i in range(0,int(var.arrSize)):
                            file.write(f'    {to_all_caps(var.name)}_{i} = {counter},\n')
                            counter = counter + 1
            file.write(f"    NUM_OF_{var_type_at} = {counter}\n")
            file.write('}')
            file.write(f' {var_type_at}EnumT;\n\n')  # Add extra newline between types

        file.write("typedef enum\n")
        file.write("{\n")
        file.write("    SIGNAL_ERROR = 0,           ///< Value unreliable, use default\n")
        file.write("    SIGNAL_CAN_TIMEOUT = 194,   ///< Timeout on CAN signal\n")
        file.write("    SIGNAL_OK = 255\n")
        file.write("} signalStateT;\n\n")

        file.write("typedef enum\n")
        file.write("{\n")
        file.write("    OBJECT_STANDARD = 0,    ///< Value is derived from program\n")
        file.write("    OBJECT_OVERRIDDEN = 1,  ///< Value is derived from external source\n")
        file.write("    OBJECT_NOT_INIT = 255,\n")
        file.write("} objectStatusT;\n\n")

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    tU32 crc32;                         ///< currently unused. CRC of all object's variables\n")
        file.write(f'    signalStateT signalState : 8;       ///< state of the signal, i.e., its reliability\n')
        file.write(f'    objectStatusT objectStatus : 8;     ///< status of this object\n')
        file.write(f'    tU8 signalUnit;                     ///< unit of the signal, i.e., volt or RPM\n')
        file.write(f'    const char* signalCmnt;             ///< Signal comment\n')
        file.write('} rtdbT;\n\n')

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    rtdbT ss;\n")
        file.write(f"    tS8 tS8_val;\n")
        file.write(f"    tS8 tS8_min;\n")
        file.write(f"    tS8 tS8_def;\n")
        file.write(f"    tS8 tS8_max;\n")
        file.write("} tS8S;\n\n")

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    rtdbT ss;\n")
        file.write(f"    tS16 tS16_val;\n")
        file.write(f"    tS16 tS16_min;\n")
        file.write(f"    tS16 tS16_def;\n")
        file.write(f"    tS16 tS16_max;\n")
        file.write("} tS16S;\n\n")

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    rtdbT ss;\n")
        file.write(f"    tS32 tS32_val;\n")
        file.write(f"    tS32 tS32_min;\n")
        file.write(f"    tS32 tS32_def;\n")
        file.write(f"    tS32 tS32_max;\n")
        file.write("} tS32S;\n\n")

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    rtdbT ss;\n")
        file.write(f"    tU8 tU8_val;\n")
        file.write(f"    tU8 tU8_min;\n")
        file.write(f"    tU8 tU8_def;\n")
        file.write(f"    tU8 tU8_max;\n")
        file.write("} tU8S;\n\n")

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    rtdbT ss;\n")
        file.write(f"    tU16 tU16_val;\n")
        file.write(f"    tU16 tU16_min;\n")
        file.write(f"    tU16 tU16_def;\n")
        file.write(f"    tU16 tU16_max;\n")
        file.write("} tU16S;\n\n")

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    rtdbT ss;\n")
        file.write(f"    tU32 tU32_val;\n")
        file.write(f"    tU32 tU32_min;\n")
        file.write(f"    tU32 tU32_def;\n")
        file.write(f"    tU32 tU32_max;\n")
        file.write("} tU32S;\n\n")

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    rtdbT ss;\n")
        file.write(f"    tF32 tF32_val;\n")
        file.write(f"    tF32 tF32_min;\n")
        file.write(f"    tF32 tF32_def;\n")
        file.write(f"    tF32 tF32_max;\n")
        file.write("} tF32S;\n\n")

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    rtdbT ss;\n")
        file.write(f"    tU8 tB_val;\n")
        file.write(f"    tU8 tB_min;\n")
        file.write(f"    tU8 tB_def;\n")
        file.write(f"    tU8 tB_max;\n")
        file.write("} tBS;\n\n")

        file.write(f"typedef struct\n")
        file.write("{\n")
        file.write(f"    rtdbT ss;\n")
        file.write(f"    tU32 tE_val;\n")
        file.write(f"    tU32 tE_min;\n")
        file.write(f"    tU32 tE_def;\n")
        file.write(f"    tU32 tE_max;\n")
        file.write("} tES;\n\n")
        file.write(f"#endif\n")


def write_rtdb_c(variables, modules):
    with open('src/rtdb.cpp', 'w') as file:
        write_autogenerated_header(file)
        file.write('#include"rtdb.h"\n')
        for module in modules:
            file.write(f'#include "{module}_rtdb.h"\n')

        file.write('\nstatic bool rtdb_s_moduleInit_tB = false;\n')
        file.write('static uint32_t rtdb_nr_moduleId_U32 = 0;\n')

        file.write('\nconst char* rtdb_unitLookupTable[VAR_UNIT_MAX_NUM] =\n')
        file.write('{\n')

        printed_units = set()
        for var_type,var_list in variables.items():
            for var in var_list:
                if var.unit not in printed_units:
                    printed_units.add(var.unit)
        nicelySortedUnits = sorted(printed_units)
        for item in nicelySortedUnits:
            if item == '':
                file.write(f'    [VAR_UNIT_NONE] = "/",\n')
            else:
                file.write(f'    [VAR_UNIT_{item}] = "{item}",\n')
        file.write('};\n\n')
        for var_type in variables:
            file.write(f"{var_type}* rtdb_arr_{var_type}[NUM_OF_{var_type}]")
            file.write(" = {0};\n")

        file.write('\ntU32 rtdb_calcCrc32 (void* VarAddrs, tU32 VarSize )\n')
        file.write('{\n')
        file.write('    // TODO\n')
        file.write('    return -1;\n')
        file.write('}\n')

        for var_type in variables:
            file.write(f'\nvoid rtdb_assign_{var_type}( {var_type}* VarAddrs,\n')
            file.write(f'                         tU32 Indx,\n')
            file.write(f'                         unitEnumT Unit,\n')
            file.write(f'                         {bt[var_type]} Min,\n')
            file.write(f'                         {bt[var_type]} Def,\n')
            file.write(f'                         {bt[var_type]} Max,\n')
            file.write(f'                         const char* Comment )\n')
            file.write('{\n')
            file.write(f'    rtdb_arr_{var_type}[Indx] = VarAddrs; // Copy address of variable to lookup table\n')
            file.write(f'    VarAddrs->{bt[var_type]}_val = Def;\n')
            file.write(f'    VarAddrs->{bt[var_type]}_min = Min;\n')
            file.write(f'    VarAddrs->{bt[var_type]}_def = Def;\n')
            file.write(f'    VarAddrs->{bt[var_type]}_max = Max;\n')
            file.write(f'    VarAddrs->ss.signalUnit = Unit;\n')
            file.write(f'    VarAddrs->ss.signalCmnt = Comment;\n')
            file.write(f'    VarAddrs->ss.signalState = SIGNAL_OK;\n')
            file.write(f'    VarAddrs->ss.objectStatus = OBJECT_STANDARD;\n')
            file.write(f'    VarAddrs->ss.crc32 = rtdb_calcCrc32(VarAddrs, sizeof({var_type}));\n')
            file.write('};')

        for var_type in variables:
            file.write(f'\n\ntU32 rtdb_write_{var_type}( {var_type}* VarAddrs, {bt[var_type]} NewVal )\n')
            file.write('{\n')
            file.write(f'    tU32 stsCode = 0;\n')
            file.write(f'    {bt[var_type]} valToWrite = VarAddrs->{bt[var_type]}_def;\n')
            file.write(f'    // check CRC\n')
            file.write('    if (rtdb_checkCrc32(VarAddrs, sizeof(VarAddrs)))\n')
            file.write('    {\n')
            file.write('        // TODO\n')
            file.write('    }\n')
            file.write(f'    // check for MIN\n')
            file.write(f'    else if ( NewVal < VarAddrs->{bt[var_type]}_min)\n')
            file.write('    {\n')
            file.write(f'        // TODO: Report error\n')
            file.write(f'        stsCode = 2;\n')
            file.write('    }\n')
            file.write(f'    // check for MAX\n')
            file.write(f'    else if ( NewVal > VarAddrs->{bt[var_type]}_max)\n')
            file.write('    {\n')
            file.write(f'        // TODO: Report error\n')
            file.write(f'        stsCode = 3;\n')
            file.write('    }\n')
            file.write(f'    else\n')
            file.write('    {\n')
            file.write('        if (OBJECT_STANDARD == VarAddrs->ss.objectStatus)\n')
            file.write('        {\n')
            file.write('            valToWrite = NewVal;\n')
            file.write(f'            rtdb_calcCrc32( VarAddrs, sizeof({var_type}));\n')
            file.write('        }\n')
            file.write('    }\n')
            file.write(f'\n')
            file.write(f'    VarAddrs->{bt[var_type]}_val = valToWrite;\n')
            file.write(f'    return stsCode;\n')
            file.write('}')

        for var_type in variables:
            file.write(f'\n\ntU32 rtdb_overwrite_{var_type}( {var_type}* VarAddrs, {bt[var_type]} NewVal )\n')
            file.write('{\n')
            file.write(f'    tU32 stsCode = 0;\n')
            file.write(f'    {bt[var_type]} valToWrite = VarAddrs->{bt[var_type]}_def;\n')
            file.write(f'    // check CRC\n')
            file.write('    if (rtdb_checkCrc32( VarAddrs, sizeof(VarAddrs))) // TODO\n')
            file.write('    {\n')
            file.write('        // TODO\n')
            file.write('        stsCode = 1;\n')
            file.write('    }\n')
            file.write(f'    else\n')
            file.write('    {\n')
            file.write(f'        valToWrite = NewVal;\n')
            file.write(f'        VarAddrs->ss.objectStatus = OBJECT_OVERRIDDEN;\n')
            file.write('    }\n')
            file.write(f'\n')
            file.write(f'    VarAddrs->{bt[var_type]}_val = valToWrite;\n')
            file.write(f'\n    //Recalculate CRC32\n')
            file.write(f'    rtdb_calcCrc32( VarAddrs, sizeof({var_type}));\n')
            file.write(f'    return stsCode;\n')
            file.write('}')

        for var_type in variables:
            file.write(f'\n\ntU32 rtdb_releaseOverwrite_{var_type}( {var_type}* VarAddrs )\n')
            file.write('{\n')
            file.write(f'    tU32 stsCode = 0;\n')
            file.write(f'    // check CRC\n')
            file.write('    if (0) // TODO\n')
            file.write('    {\n')
            file.write('        // TODO\n')
            file.write('        stsCode = 1;\n')
            file.write('    }\n')
            file.write(f'    else\n')
            file.write('    {\n')
            file.write(f'        VarAddrs->ss.objectStatus = OBJECT_STANDARD;\n')
            file.write('        // TODO: Recalculate CRC\n')
            file.write('    }\n')
            file.write(f'\n')
            file.write(f'    return stsCode;\n')
            file.write('}')

        for var_type in variables:
            file.write('\n\n/**\n')
            file.write('* @brief Function returns current value of given variable\n')
            file.write('* @param {var_type}EnumT VarName name of the variable as an enum\n')
            file.write('* @return Verified value of the given variable\n')
            file.write('*/\n')
            file.write(f'{bt[var_type]} rtdb_read_{var_type}( {var_type}EnumT VarName )\n')
            file.write('{\n')
            file.write(f'    {bt[var_type]} toReturn = rtdb_arr_{var_type}[VarName]->{bt[var_type]}_val;\n')
            file.write(f'    // Check CRC\n')
            file.write(f'    if (0)\n')
            file.write('    {\n')
            file.write(f'        // TODO: implement CRC failed case\n')
            file.write('    }\n')
            file.write(f'\n')
            file.write(f'    return toReturn;\n')
            file.write('}')

        file.write('\n\nvoid rtdb_init(tRTDB_INITDATA_STR* RtdbCfg)\n')
        file.write('{\n')
        file.write('    if (true == rtdb_s_moduleInit_tB)\n')
        file.write('    {\n')
        file.write('        errh_reportError(ERRH_NOTIF, rtdb_nr_moduleId_U32, 0, RTDB_API_INIT_U32, ERRH_MODULE_ALREADY_INIT);\n')
        file.write('    }\n')
        file.write('    else if (NULL == RtdbCfg)\n')
        file.write('    {\n')
        file.write('        errh_reportError(ERRH_ERROR_CRITICAL, rtdb_nr_moduleId_U32, 0, RTDB_API_INIT_U32, ERRH_POINTER_IS_NULL);\n')
        file.write('    }\n')
        file.write('    else\n')
        file.write('    {\n')
        file.write('        rtdb_s_moduleInit_tB = true;\n')
        for module in modules:
            file.write(f'        {module}_rtdb_init();\n')
        file.write('    }\n')
        file.write('}\n')

def write_rtdb_h(modules):
    with open('include/rtdb.h', 'w') as file:
        write_autogenerated_header(file)
        file.write('#ifndef RTDB_H\n')
        file.write('#define RTDB_H\n')
        file.write('\n')
        file.write('#include "rtdb_vars.h"\n')
        file.write('#include "errh.h"\n\n')
        file.write('\n#define RTDB_API_INIT_U32                  ((uint32_t) 1)\n')
        file.write('\n')
        file.write('typedef struct\n')
        file.write('{\n')
        file.write('    uint32_t nr_moduleId_U32;       ///< ID of the module\n')
        file.write('} tRTDB_INITDATA_STR;\n\n')
        file.write('// ASSIGN DURING INIT\n')
        file.write('void rtdb_assign_tU8S ( tU8S* VarAddrs, tU32 Indx, unitEnumT Unit, tU8 Min, tU8 Def, tU8 Max, const char* Comment );\n')
        file.write('void rtdb_assign_tU16S( tU16S* VarAddrs, tU32 Indx, unitEnumT Unit, tU16 Min, tU16 Def, tU16 Max, const char* Comment );\n')
        file.write('void rtdb_assign_tU32S( tU32S* VarAddrs, tU32 Indx, unitEnumT Unit, tU32 Min, tU32 Def, tU32 Max, const char* Comment );\n')
        file.write('\n')
        file.write('void rtdb_assign_tS8S ( tS8S* VarAddrs, tU32 Indx, unitEnumT Unit, tS8 Min, tS8 Def, tS8 Max, const char* Comment );\n')
        file.write('void rtdb_assign_tS16S( tS16S* VarAddrs, tU32 Indx, unitEnumT Unit, tS16 Min, tS16 Def, tS16 Max, const char* Comment );\n')
        file.write('void rtdb_assign_tS32S( tS32S* VarAddrs, tU32 Indx, unitEnumT Unit, tS32 Min, tS32 Def, tS32 Max, const char* Comment );\n')
        file.write('\n')
        file.write('void rtdb_assign_tES   ( tES*  VarAddrs, tU32 Indx, unitEnumT Unit, tU32 Min, tU32 Def, tU32 Max, const char* Comment );\n')
        file.write('void rtdb_assign_tBS   ( tBS*  VarAddrs, tU32 Indx, unitEnumT Unit, tU8 Min, tU8 Def, tU8 Max, const char* Comment );\n')
        file.write('void rtdb_assign_tF32S ( tF32S* VarAddrs, tU32 Indx, unitEnumT Unit, float Min, float Def, float Max, const char* Comment );\n')
        file.write('\n')
        file.write('\n')
        file.write('// WRITE DURING RUNTIME\n')
        file.write('tU32 rtdb_write_tU8S ( tU8S* VarAddrs, tU8 NewVal );\n')
        file.write('tU32 rtdb_write_tU16S( tU16S* VarAddrs, tU16 NewVal );\n')
        file.write('tU32 rtdb_write_tU32S( tU32S* VarAddrs, tU32 NewVal );\n')
        file.write('\n')
        file.write('tU32 rtdb_write_tS8S ( tS8S* VarAddrs, tS8 NewVal );\n')
        file.write('tU32 rtdb_write_tS16S( tS16S* VarAddrs, tS16 NewVal );\n')
        file.write('tU32 rtdb_write_tS32S( tS32S* VarAddrs, tS32 NewVal );\n')
        file.write('\n')
        file.write('tU32 rtdb_write_tES   ( tES*  VarAddrs, tS32 NewVal );\n')
        file.write('tU32 rtdb_write_tBS   ( tBS*  VarAddrs, tS8 NewVal );\n')
        file.write('tU32 rtdb_write_tF32S ( tF32S* VarAddrs, float NewVal );\n')
        file.write('\n')
        file.write('// OVERWRITE DURING RUNTIME\n')
        file.write('tU32 rtdb_overwrite_tU8S ( tU8S* VarAddrs, tU8 NewVal );\n')
        file.write('tU32 rtdb_overwrite_tU16S( tU16S* VarAddrs, tU16 NewVal );\n')
        file.write('tU32 rtdb_overwrite_tU32S( tU32S* VarAddrs, tU32 NewVal );\n')
        file.write('\n')
        file.write('tU32 rtdb_overwrite_tS8S ( tS8S* VarAddrs, tS8 NewVal );\n')
        file.write('tU32 rtdb_overwrite_tS16S( tS16S* VarAddrs, tS16 NewVal );\n')
        file.write('tU32 rtdb_overwrite_tS32S( tS32S* VarAddrs, tS32 NewVal );\n')
        file.write('\n')
        file.write('tU32 rtdb_overwrite_tES   ( tES*  VarAddrs, tS32 NewVal );\n')
        file.write('tU32 rtdb_overwrite_tBS   ( tBS*  VarAddrs, tS8 NewVal );\n')
        file.write('tU32 rtdb_overwrite_tF32S ( tF32S* VarAddrs, float NewVal );\n')
        file.write('\n')
        file.write('\n')
        file.write('// READ DURING RUNTIME\n')
        file.write('tU8  rtdb_read_tU8S ( tU8SEnumT VarName );\n')
        file.write('tU16 rtdb_read_tU16S( tU16SEnumT VarName );\n')
        file.write('tU32 rtdb_read_tU32S( tU32SEnumT VarName );\n')
        file.write('\n')
        file.write('tS8  rtdb_read_tS8S ( tS8SEnumT VarName );\n')
        file.write('tS16 rtdb_read_tS16S( tS16SEnumT VarName );\n')
        file.write('tS32 rtdb_read_tS32S( tS32SEnumT VarName );\n')
        file.write('\n')
        file.write('tE    rtdb_read_tES   ( tESEnumT  VarName );\n')
        file.write('tB    rtdb_read_tBS   ( tBSEnumT  VarName );\n')
        file.write('tF32  rtdb_read_tF32S ( tF32SEnumT VarName );\n')
        file.write('\n')
        file.write('\n')
        file.write('// AUXILLIARY FUNCTIONS\n')
        file.write('tU32 rtdb_checkCrc32 (void* VarAddrs, tU32 VarSize );\n')
        file.write('tU32 rtdb_calcCrc32  (void* VarAddrs, tU32 VarSize );\n')
        file.write('\n')
        for module in modules:
            file.write(f'void {module}_rtdb_init(void);\n')
        file.write(f'void rtdb_init(tRTDB_INITDATA_STR* RtdbCfg);\n')
        file.write('\n#endif\n')