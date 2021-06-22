from random import randint
from time import sleep
from chemistry import *

# Set all molecules
HYDROGEN_CATION = Molecules('H+', 'Hydrogen cation')
WATER = Molecules('H2O', 'Water')
ADP = Molecules('C10H15N5O10P2', 'ADP')
ATP = Molecules('C10H15N5O10P3', 'ATP')
NADP = Molecules('C21H27N7O14P2', 'NAD+')
NADHP = Molecules('C21H28N7O14P2', 'NADH')
FAD = Molecules('C27H33P2N9O15', 'FAD')
FADH2 = Molecules('C27H35N9O15P2', 'FADH2')
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

cytoplasm_system = System(1*[GLICOSE] + 2*[ATP] + 2*[ADP] + 2*[NADP])
mitochondria_inner_system = System(2*[COA] + 8*[NADP] + 2*[FAD] + 1*[OXALOACETIC_ACID] + 100*[ADP] + 16*[OXYGEN])
mitochondria_outer_system = System([])

protein_memory = 0
subs = 0
q = 0

def glycolysis():
    cytoplasm_system.do_reaction(1*[GLICOSE] + 2*[ATP], 2*[PGAL] + 2*[ADP])
    cytoplasm_system.do_reaction(1*[PGAL, NADP] + 2*[ADP], 1*[PYRUVATE, NADHP, HYDROGEN_CATION] + 2*[ATP])


def acetyl_CoA_synthase():
    mitochondria_inner_system.do_reaction(1*[PYRUVATE, NADP, COA], 1*[CARBON_DIOXIDE, NADHP, HYDROGEN_CATION, ACETYL_COA])


def krebs_circle():
    mitochondria_inner_system.do_reaction(1*[ACETYL_COA, OXALOACETIC_ACID], 1*[CITRIC_ACID])
    mitochondria_inner_system.do_reaction(
        1*[CITRIC_ACID, FAD, ADP] + 3*[NADP], 
        2*[CARBON_DIOXIDE] + 1*[OXALOACETIC_ACID, FADH2, ATP] + 3*[NADHP, HYDROGEN_CATION]
    )


def atpase():
    if mitochondria_outer_system.length(HYDROGEN_CATION) > mitochondria_inner_system.length(HYDROGEN_CATION):
        if mitochondria_outer_system.length(HYDROGEN_CATION) >= 2:
            for i in range(0, 2):
                mitochondria_outer_system.remove_molecule(HYDROGEN_CATION)
                mitochondria_inner_system.add_molecule(HYDROGEN_CATION)
            mitochondria_inner_system.do_reaction([ADP], [ATP])


def hydro_protein():
    for k in range(0, 2):
        mitochondria_inner_system.remove_molecule(HYDROGEN_CATION)
        mitochondria_outer_system.add_molecule(HYDROGEN_CATION)


def electron_transport_chain():
    global subs, q, protein_memory

    if mitochondria_inner_system.length(NADHP) >= 1 and mitochondria_inner_system.length(HYDROGEN_CATION) >= 2:
        hydro_protein()
        mitochondria_inner_system.do_reaction(1*[NADHP], 1*[NADP] + 2*[HYDROGEN_CATION])
        q += 2

    if mitochondria_inner_system.length(FADH2) >= 1 and mitochondria_inner_system.length(HYDROGEN_CATION) >= 2:
        hydro_protein()
        mitochondria_inner_system.do_reaction(1*[FADH2], 1*[FAD] + 2*[HYDROGEN_CATION])
        q += 2

    if mitochondria_inner_system.length(HYDROGEN_CATION) >= 2 and q >= 2 and protein_memory < 4:
        hydro_protein()
        q -= 2
        protein_memory += 2

    if mitochondria_inner_system.length(HYDROGEN_CATION) >= 4 and mitochondria_inner_system.length(OXYGEN) >= 1 and protein_memory == 4:
        protein_memory -= 4
        mitochondria_inner_system.do_reaction(4*[HYDROGEN_CATION] + 2*[OXYGEN], 2*[WATER])


def show_status():
    print(f'cytoplasm_system: Glicose {cytoplasm_system.length(GLICOSE)} | ATP {cytoplasm_system.length(ATP)} | NADH+ {cytoplasm_system.length(NADHP)}  ', end='/  ')
    print(f'mitochondria_inner_system: ATP {mitochondria_inner_system.length(ATP)} | NADH {mitochondria_inner_system.length(NADHP)} | CO2 {mitochondria_inner_system.length(CARBON_DIOXIDE)} ', end='')
    print(f'| FADH2 {mitochondria_inner_system.length(FADH2)} | H+ {mitochondria_inner_system.length(HYDROGEN_CATION)} | Water {mitochondria_inner_system.length(WATER)} | Nº of electrons in chain {q} ')


while True:
    glycolysis()

    if cytoplasm_system.length(PYRUVATE) >= 1:
        cytoplasm_system.remove_molecule(PYRUVATE)
        mitochondria_inner_system.add_molecule(PYRUVATE)

    if cytoplasm_system.length(NADHP) >= 1:
        cytoplasm_system.remove_molecule(NADHP)
        mitochondria_inner_system.add_molecule(NADHP)

    acetyl_CoA_synthase()
    krebs_circle()

    electron_transport_chain()
    atpase()

    show_status()
    sleep(1/4)
    






