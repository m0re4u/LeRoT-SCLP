import re


def update_config(file, var_name, var_value):
    """
    Given file, variable name and a new value,
    update the variable to the new value in the
    given file
    """
    new_text = ""
    # Regex to find variable in config file
    regex = re.escape(var_name) + r'.*'
    with open(file, 'r') as f:
        for line in f:
            # Replace variable value once found
            # if there is a : in the line then make sure to place it back
            if re.match(r'.+:+.+', line):
                line = re.sub(regex, var_name+': '+str(int(var_value)), line)
            else:
                line = re.sub(regex, var_name+' '+str(var_value), line)
            new_text += line
    # Write back to file
    with open(file, 'w') as f:
        f.write(new_text)
