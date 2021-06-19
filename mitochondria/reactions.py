from random import randint
from mitochondria.chemistry import *

# Set all molecules
HYDROGEN_CATION = Molecules('H+', 'Hydrogen cation')
WATER = Molecules('H2O', 'Water')
ADP = Molecules('C10H15N5O10P2', 'ADP')
ATP = Molecules('C10H15N5O10P3', 'ATP')
NADP = Molecules('C21H27N7O14P2', 'NAD+')
NADHP = Molecules('C21H28N7O14P2', 'NADH')
FAD = Molecules('C27H33P2N9O15', 'FAD')
FAH2 = Molecules('C27H35N9O15P2', 'FADH2')
CARBON_DIOXIDE = Molecules('CO2', 'Carbon dioxide')
PGAL = Molecules('C3H5O5P','PGAL')
GLICOSE = Molecules('C6H12O6', 'Glicose')
OXYGEN_ATOM = Molecules('O', 'Oxygen atom')
OXYGEN = Molecules('O2', 'Oxygen')
PYRUVATE = Molecules('C3H4O3', 'Pyruvate')
COA = Molecules('C21H36N7O16P3S', 'CoA')
ACETYL_COA = Molecules('C23H38N7O17P3S', 'Acetyl CoA')
OXALOACETIC_ACID = Molecules('C4H4O5', 'Oxaloacetic acid')
CITRIC_ACID = Molecules('C6H8O7', 'Citric acid')

cytoplasm_system = System(1*[GLICOSE] + 2*[ATP] + 4*[ATD] + 2*[NADP])
mitochondria_matrix_system = System()

def glycolysis():
    cytoplasm_system.do_reaction(1*[GLICOSE] + 2[ATP], 2*[PGAL] + 2*[ADP])
    cytoplasm_system.do_reaction(1*[PGAL, NADP] + 2*[ADP], 1*[PYRUVATE, NADHP, HYDROGEN_CATION] + 2*[ATP])


def acetyl_CoA_synthase():
    mitochondria_matrix_system.do_reaction(1*[PYRUVATE, NADP, COA], 1*[CARBON_DIOXIDE, NADHP, HYDROGEN_CATION, ACETYL_COA])


def krebs_circle():
    mitochondria_matrix_system.do_reaction(1*[ACETYL_COA, OXALOACETIC_ACID], 1*[CITRIC_ACID])
    mitochondria_matrix_system.do_reaction(1*[CITRIC_ACID, FAD, ADP] + 3*[NADP], 1*[OXALOACETIC_ACID, FADH2, ATP] + 3*[NADHP, HYDROGEN_CATION])


while True:
    glycolysis()

    cytoplasm_system.remove_molecule(PYRUVATE)
    cytoplasm_system.add_molecule(PYRUVATE)

    cytoplasm_system.remove_molecule(NADHP)
    cytoplasm_system.add_molecule(NADHP)

    acetyl_CoA_synthase()
    krebs_circle()
    





