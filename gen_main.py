import glob
from collections import defaultdict
import gen_formatter
import gen_c_file_parsing
import gen_c_file_making

def process_files():
    rtdb_var_files = glob.glob('*_rtdb_vars.h')
    all_variables = defaultdict(list)

    for var_file in rtdb_var_files:
        # format files with variables
        gen_formatter.format_lines(var_file)

        # extract variables from files
        variables = gen_c_file_parsing.parse_file(var_file) # a dictionary[var type] that holds lists of var structs
        rtdb_file = var_file.replace('_rtdb_vars.h', '_rtdb.h')

        # Extract the prefix from the filename
        prefix = var_file.split('_rtdb_vars.h')[0]

        # create each module's rtdb
        gen_c_file_making.write_module_rtdb(prefix, rtdb_file, variables)

        # Aggregate all variables into one list
        for var_type, var_names in variables.items():
            all_variables[var_type].extend(var_names)

    # create rtdb variables file that contains references to all rtdb variables
    gen_c_file_making.write_rtdb_vars_h(all_variables)

    # create rtdb.c file with all of the required read/write access functionalities
    gen_c_file_making.write_rtdb_c(all_variables)


if __name__ == "__main__":
    process_files()
