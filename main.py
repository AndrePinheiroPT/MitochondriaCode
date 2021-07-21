from mitochondria.reactions import simulation
from menu_tools import *

energy_forms = [
    '1 - Aerobic respiration', 
    '2 - Latic fermentation',
    '3 - Alcoholic fermentation'
]

variables = {
    'nº CoA': 0,
    'nº FAD': 0,
    'nº O2': 0,
    'nº Glicose': 0,
    'nº ATP': {
        'In cytoplasm': 0,
        'In mitochondria': 0 
    },
    'nº ADP': {
        'In cytoplasm': 0,
        'In mitochondria': 0 
    },
    'nº NAD+': {
        'In cytoplasm': 0,
        'In mitochondria': 0 
    },
    'nº NADH+': {
        'In cytoplasm': 0,
        'In mitochondria': 0 
    }
}
variables_names = ['nº CoA', 'nº FAD', 'nº O2', 'nº Glicose', 'nº ATP', 'nº ADP', 'nº NAD+', 'nº NADH+']

line()
print('MitochondriaCode v1.0.0\n\
Copyright \u00a9 André Pinheiro\n\
Read the licence for more information')

line()
print('Welcome to the MitochondriaCode! For start a simulation, you\n\
need the set the follow variables:')

# Show energy forms
for form in energy_forms:
    print(form)

# Ask for select a value
while True:
    line()
    simulate_option = read_int('Chose the form you want simulate: ')
    if 1 <= simulate_option <= 3:
        break
    print('Please, type a valid option')
    
# Menu loop for check values
state = True
while state:
    # Show all variables
    count = 1
    for key in variables:
        if simulate_option == 1:
            print(f'{count}) {key} -> {variables[key]}')
            count += 1
        elif key != 'nº CoA' and key != 'nº FAD':
            print(f'{count}) {key} -> {variables[key]}')
            count += 1

    print(f'{9 if simulate_option == 1 else 7}) Start the simulation')
    line()

    # Ask for select a value
    while True:
        option = read_int('Chose the variable you want change: ')
        if simulate_option == 1:
            if 1 <= option <= 9:
                break
        else:
            if 1 <= option <= 7:
                break
        print('Please, type a valid option')

    line()

    # Get out of loop
    if (option == 9 and simulate_option == 1) or (option == 7 and simulate_option != 1):
        break

    # Get values
    key_type = option - 1 if simulate_option == 1 else option + 1
    if isinstance(variables[f'{variables_names[key_type]}'], dict):
        variables[f'{variables_names[key_type]}']['In cytoplasm'] = read_int('In cytoplasm: ')
        variables[f'{variables_names[key_type]}']['In mitochondria'] = 0
    else:
        variables[f'{variables_names[key_type]}'] = read_int(f'{variables_names[key_type]}: ')


# Load countdown and simulatin functions        
countdown()

# Make a list with all values typed
variables_values = []
for key, value in variables.items():
    if isinstance(value, dict):
        variables_values.append(value['In cytoplasm'])
        variables_values.append(value['In mitochondria'])
    else:
        variables_values.append(value)

simulation(*variables_values, simulate_option)