import re
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class variable:
    name: str
    arrSize: int
    unit: str
    min: float
    default: float
    max: float
    comment: str

def parse_file(file_path):
    variable_pattern = re.compile(r'^\s*(\w*)\s*(\w*)\s*\[?(\w*)\]?\;\s*\/*\<\s*\[(\w*)\]\s*\[(-*\w*\.*\w*)\]\s*\[(-*\w*\.*\w*)\]\s*\[(-*\w*\.*\w*)\]\s*(\w.*)')
    variables = defaultdict(list)

    with open(file_path, 'r') as file:
        for line in file:
            match = variable_pattern.match(line)
            if match:
                var_type, var_name, array_size, unit, min, default, max, comment = match.groups()
                var = variable(var_name, array_size, unit, min, default, max, comment)
                if var_type in variables:
                    variables[var_type].append(var)
                else:
                    variables[var_type] = [var]
    return variables