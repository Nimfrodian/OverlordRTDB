import re
import os

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

def write_module_rtdb(module_name, file_path, variables):
    with open(file_path, 'w') as file:

        file.write(f"#ifndef {module_name.upper()}_RTDB_H\n")
        file.write(f"#define {module_name.upper()}_RTDB_H\n\n")

        file.write(f"#include \"rtdb.h\"\n")
        file.write(f"#include \"{module_name}_rtdb_vars.h\"\n\n")

        file.write(f"void {module_name}_rtdb_init()\n")
        file.write("{\n")
        for var_type,var_list in variables.items():
            for var in sorted_nicely(var_list, key=lambda var: var.name):
                if var.arrSize == '':
                    file.write(f'\trtdb_assign_{var_type}(&{var.name}, {to_all_caps(var.name)}')
                    assign_aux_data(file, var, var_type)
                else:
                    for i in range(0,int(var.arrSize)):
                        file.write(f'\trtdb_assign_{var_type}(&{var.name}[{i}], {to_all_caps(var.name)}_{i}')
                        assign_aux_data(file,var, var_type)
        file.write("}\n")

        file.write(f"#endif\n")


def write_rtdb_vars_h(variables):
    counter = 0
    with open('include/rtdb_vars.h', 'w') as file:
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
        file.write('} unitEnumT;\n')
        file.write('\nunsigned char* rtdb_unitLookupTable[VAR_UNIT_MAX_NUM] =\n')
        file.write('{\n')
        for item in nicelySortedUnits:
            if item == '':
                file.write(f'    [VAR_UNIT_NONE] = "/",\n')
            else:
                file.write(f'    [VAR_UNIT_{item}] = "{item}",\n')
        file.write('};\n\n')

        for var_type,var_list in variables.items():
            file.write(f'// {var_type}\n')
            file.write('enum\n{\n')
            for var in sorted_nicely(var_list, key=lambda var: var.name):
                if var.arrSize == '':
                    file.write(f'\t{to_all_caps(var.name)} = {counter},\n')
                    counter = counter + 1
                else:
                    for i in range(0,int(var.arrSize)):
                        file.write(f'\t{to_all_caps(var.name)}_{i} = {counter},\n')
                        counter = counter + 1

            file.write(f"\n\tNUM_OF_{var_type.upper()} = {counter}\n")
            counter = 0
            file.write('};\n\n')  # Add extra newline between types

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
        file.write(f'    tU8* signalCmnt;                    ///< Signal comment\n')
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

        for var_type in variables:
            file.write(f"{var_type}* rtdb_arr_{var_type}[NUM_OF_{var_type.upper()}]")
            file.write(" = {0};\n")
        file.write(f"#endif\n")


def write_rtdb_c(variables):
    with open('src/rtdb.c', 'w') as file:
        file.write('#include"rtdb.h"\n')

        for var_type in variables:
            file.write(f'\n\n{var_type} rtdb_assign_{var_type}( {var_type}* VarAddrs,\n')
            file.write(f'                         tU32 Indx,\n')
            file.write(f'                         unitEnumT Unit,\n')
            file.write(f'                         {bt[var_type]} Min,\n')
            file.write(f'                         {bt[var_type]} Def,\n')
            file.write(f'                         {bt[var_type]} Max,\n')
            file.write(f'                         char* Comment )\n')
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
            file.write(f'            VarAddrs->{bt[var_type]}_val = NewVal;\n')
            file.write(f'            rtdb_calcCrc32( VarAddrs, sizeof({var_type}));\n')
            file.write('        }\n')
            file.write('    }\n')
            file.write(f'\n')
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
            file.write(f'\n\n{var_type} rtdb_read_{var_type}( {var_type}* VarAddrs )\n')
            file.write('{\n')
            file.write(f'    {var_type} toReturn = *VarAddrs;\n')
            file.write(f'    // Check CRC\n')
            file.write(f'    if (0)\n')
            file.write('    {\n')
            file.write(f'        // TODO: implement CRC failed case\n')
            file.write('    }\n')
            file.write(f'\n')
            file.write(f'    return toReturn;\n')
            file.write('}')

def write_rtdb_h():
    with open('include/rtdb.h', 'w') as file:
        file.write('#ifndef RTDB_H\n')
        file.write('#define RTDB_H\n')
        file.write('\n')
        file.write('#include "rtdb_vars.h"\n')
        file.write('\n')
        file.write('// ASSIGN DURING INIT\n')
        file.write('tU8  rtdb_assign_tU8S ( tU8S* VarAddrs, tU32 Indx, unitEnumT Unit, tU8 Min, tU8 Def, tU8 Max, char* Comment );\n')
        file.write('tU16 rtdb_assign_tU16S( tU16S* VarAddrs, tU32 Indx, unitEnumT Unit, tU16 Min, tU16 Def, tU16 Max, char* Comment );\n')
        file.write('tU32 rtdb_assign_tU32S( tU32S* VarAddrs, tU32 Indx, unitEnumT Unit, tU32 Min, tU32 Def, tU32 Max, char* Comment );\n')
        file.write('\n')
        file.write('tS8  rtdb_assign_tS8S ( tS8S* VarAddrs, tU32 Indx, unitEnumT Unit, tS8 Min, tS8 Def, tS8 Max, char* Comment );\n')
        file.write('tS16 rtdb_assign_tS16S( tS16S* VarAddrs, tU32 Indx, unitEnumT Unit, tS16 Min, tS16 Def, tS16 Max, char* Comment );\n')
        file.write('tS32 rtdb_assign_tS32S( tS32S* VarAddrs, tU32 Indx, unitEnumT Unit, tS32 Min, tS32 Def, tS32 Max, char* Comment );\n')
        file.write('\n')
        file.write('tE    rtdb_assign_tES   ( tES*  VarAddrs, tU32 Indx, unitEnumT Unit, tU32 Min, tU32 Def, tU32 Max, char* Comment );\n')
        file.write('tB    rtdb_assign_tBS   ( tBS*  VarAddrs, tU32 Indx, unitEnumT Unit, tU8 Min, tU8 Def, tU8 Max, char* Comment );\n')
        file.write('tF32  rtdb_assign_tF32S ( tF32S* VarAddrs, tU32 Indx, unitEnumT Unit, float Min, float Def, float Max, char* Comment );\n')
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
        file.write('tU8  rtdb_read_tU8S ( tU8S* VarAddrs );\n')
        file.write('tU16 rtdb_read_tU16S( tU16S* VarAddrs );\n')
        file.write('tU32 rtdb_read_tU32S( tU32S* VarAddrs );\n')
        file.write('\n')
        file.write('tS8  rtdb_read_tS8S ( tS8S* VarAddrs );\n')
        file.write('tS16 rtdb_read_tS16S( tS16S* VarAddrs );\n')
        file.write('tS32 rtdb_read_tS32S( tS32S* VarAddrs );\n')
        file.write('\n')
        file.write('tE    rtdb_read_tES   ( tES*  VarAddrs );\n')
        file.write('tB    rtdb_read_tBS   ( tBS*  VarAddrs );\n')
        file.write('tF32  rtdb_read_tF32S ( tF32S* VarAddrs );\n')
        file.write('\n')
        file.write('\n')
        file.write('// AUXILLIARY FUNCTIONS\n')
        file.write('tU32 rtdb_checkCrc32 (void* VarAddrs, tU32 VarSize );\n')
        file.write('tU32 rtdb_calcCrc32  (void* VarAddrs, tU32 VarSize );\n')
        file.write('\n')
        file.write('#endif\n')