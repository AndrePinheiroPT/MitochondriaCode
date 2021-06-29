from mitochondria.reactions import simulation
from menu_tools import *

variables = {
    'nº O2': 0,
    'nº Glisose': 0,
    'nº CoA': 0,
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
    },
    'nº FAD': 0
}
variables_names = ['nº O2', 'nº Glicose', 'nº CoA', 'nº ATP', 'nº ADP', 'nº NAD+', 'nº NADH+', 'nº FAD']

line()
print('MitochondriaCode v1.0.0\n\
Copyright \u00a9 André Pinheiro\n\
Read the licence for more information')

line()
print('Welcome to the MitochondriaCode! For start a simulation, you\n\
need the set the follow variables:')
    
# Menu loop for check values
state = True
while state:
    # Show all variable value typed
    count = 1
    for key in variables:
        print(f'{count}) {key} -> {variables[key]}')
        count += 1

    print('9) Start the simulation')
    line()

    # Ask for check all values
    while True:
        option = read_int('Chose the variable you want change? ')
        if 1 <= option <= 9:
            break
        print('Please, type a valid option')

    line()

    if option == 9:
        break

    if isinstance(variables[f'{variables_names[option - 1]}'], dict):
        variables[f'{variables_names[option - 1]}']['In cytoplasm'] = read_int('In cytoplasm: ')
        variables[f'{variables_names[option - 1]}']['In mitochondria'] = read_int('In mitochondria: ')
    else:
        variables[f'{variables_names[option - 1]}'] = read_int(f'{variables_names[option - 1]}: ')


# Load countdown and simulatin functions           
countdown()
simulation(*[value for key, value in variables.items()])