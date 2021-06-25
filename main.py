from mitochondria.reactions import simulation
from menu_tools import *

variables = {
    'nº O2': 0,
    'nº Glisose': 0,
    'nº CoA': 0,
    'nº ATP': [
        'In cytoplasm': 0
        'In mitochondria': 0 
    ],
    'nº ADP': [
        'In cytoplasm': 0
        'In mitochondria': 0 
    ],
    'nº NAD+': [
        'In cytoplasm': 0
        'In mitochondria': 0 
    ],
    'nº NADH+': [
        'In cytoplasm': 0
        'In mitochondria': 0 
    ]
    'nº FAD': 0
}


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
    # Set all variables except "radiation"
    for key in variables:
        variables[key] = read_int(f'{key}: ')
    
    line()
    # Show all variable value typed
    for key in variables:
        print(f'{key} -> {variables[key]}')

    line()
    # Ask for check all values
    while True:
        cont = input('Are you sure? [Y/N] ').strip().upper()
        if cont == 'Y' or cont == 'N':
            state = False if cont == 'Y' else True
            break
    line()


# Load countdown and simulatin functions           
countdown()
simulation(*[value for key, value in variables.items()])