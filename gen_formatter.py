import re

# Function to process and format the lines
def format_lines(input_file):
    # Define the regex pattern to match the lines
    pattern = re.compile(r'^(\[?\w*\]?)\s*(\[?\w*\]?)\s*\[?(\w*\s?[(]?\w*[)]?)\]?\;\s*\/*\<\s*\[(\w*)\]\s*\[(-*\w*\.*\w*)\]\s*\[(-*\w*\.*\w*)\]\s*\[(-*\w*\.*\w*)\]\s*\[?([A-Z,a-z,0-9,., ,-]*)\]?\s*\*?\/?')

    totalLines = []
    totalParts = []

    # Read the file and process each line to get the required information
    with open(input_file, 'r') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                # Extract the groups from the match
                parts = match.groups()
                totalParts.append(parts)

    maxLengths = [0]*8
    for part in totalParts:
        for i in range(8):
            maxLengths[i] = max(maxLengths[i], len(part[i]))



    # Read the file and process each line to modify it
    matchIndx = 0
    with open(input_file, 'r') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                formatted_line = "{:<{}}".format(totalParts[matchIndx][0],maxLengths[0]+3)
                if totalParts[matchIndx][2] != '':
                    formatted_line += " {:<{}} {:<{}} ///< ".format(f'{totalParts[matchIndx][1]}', maxLengths[1]+2, f'[{totalParts[matchIndx][2]}];',maxLengths[2]+3)
                else:
                    formatted_line += " {:<{}} {:<{}} ///< ".format(f'{totalParts[matchIndx][1]};', maxLengths[1]+2, "",maxLengths[2]+3)
                slice1 = totalParts[matchIndx][3:7]
                slice2 = maxLengths[3:7]
                for partText,lengthInt in zip(slice1,slice2):
                    formatted_line += "{:<{}} ".format(f'[{partText}]', lengthInt+3)
                if matchIndx == 0:
                    formatted_line += f' [{totalParts[matchIndx][7]}]'
                else:
                    formatted_line += f' {totalParts[matchIndx][7]}'
                formatted_line += "\n"
                matchIndx = matchIndx+1
                totalLines.append(formatted_line)
            else:
                totalLines.append(line)

    with open(input_file, 'w') as file:
        file.writelines(totalLines)