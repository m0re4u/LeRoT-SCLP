import re
def make_experiment_args(file, var_name, var_value):
    new_text = ""
    # Regex to find variable in config file
    regex = re.escape(var_name) + r'+.*'
    with open(file, 'r') as f:
        for line in f:
            # Replace variable value once found
            line = re.sub(regex, var_name+' '+str(var_value), line)
            new_text += line
    # Write back to file
    with open(file, 'w') as f:
        f.write(new_text)
