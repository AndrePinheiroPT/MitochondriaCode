from random import randint
from chloroplast.chemistry import *

# Set all molecules
HYDROGEN_CATION = Molecules('H+', 'Hydrogen cation')
WATER = Molecules('H2O', 'Water')
ADP = Molecules('C10H15N5O10P2', 'ADP')
ATP = Molecules('C10H15N5O10P3', 'ATP')
NADPP = Molecules('C21H29N7O17P3', 'NADP+')
NADPH = Molecules('C21H30N7O17P3', 'NADPH')
CARBON_DIOXIDE = Molecules('CO2', 'Carbon dioxide')
RUDP = Molecules('C5H12O11P2', 'RuDP')
PGAL_S = Molecules('C3H7O6P_S', 'PGAL_S')
PGAL = Molecules('C3H5O5P','PGAL')
GLICOSE = Molecules('C6H12O6', 'Glicose')
PGA = Molecules('C3H7O7P', 'PGA')
OXYGEN_ATOM = Molecules('O', 'Oxygen atom')
OXYGEN = Molecules('O2', 'Oxygen')

# Constants about radiation
SPEED_OF_LIGHT = 3 * 10**8
PLANK_MODIFIED = 1 * 10**-6 
light_intensity = 0

# Set systems
inner_thylakoid_system = []
stroma_system = []
# Number of electrons in some transport chain
# for exemple: transport_electrons[0] represents
# the number of electrons of that transport chain
transport_electrons = [0, 0]

class Photosystem:
    def __init__(self,
                 chlorophyllA_length,
                 chlorophyllB_length,
                 beta_carotene_length):
        
        # Set number of chlorophyll A and B
        self.chlorophyllA_length = chlorophyllA_length
        self.chlorophyllB_length = chlorophyllB_length
        self.beta_carotene_length = beta_carotene_length
        # Energy and number of eletrons in photosystem
        self.energy = 0
        self.electrons = 2
        
    def check_oxidation(self, transport_type, oxi_energy):
        # Oxidation of photosystem if his energy is bigger then 
        # oxidation energy
        if self.energy >= oxi_energy:
            self.electrons -= 2
            self.energy -= oxi_energy
            transport_electrons[transport_type] += 2
    
    def photo_reaction(self, labmda):
        # Probability of absorve some radiation
        if self.electrons > 0:
            # Get energy of radiation
            frequency = SPEED_OF_LIGHT / labmda
            light_energy = PLANK_MODIFIED * frequency
            for i in range(0, self.chlorophyllA_length):
                if self.light_chlorophyllA(labmda) < randint(0, 100):
                    self.energy += light_energy
                    
            for i in range(0, self.chlorophyllB_length):
                if self.light_chlorophyllB(labmda) < randint(0, 100):
                    self.energy += light_energy
                    
            for i in range(0, self.beta_carotene_length):
                if self.light_beta_carotene(labmda) < randint(0, 100):
                    self.energy += light_energy
                    
    
    def light_chlorophyllA(self, x):
        # chlorophyll A probability function
        labmda = x - 400
        if 0 <= labmda < 25:
            return 1.32 * labmda + 134
        elif 25 <= labmda < 50:
            return -2.6 * labmda + 134
        elif 50 <= labmda < 200:
            return 4
        elif 200 <= labmda < 250:
            return 0.1 * labmda - 16
        elif 250 <= labmda < 270:
            return 2.04 * labmda - 500
        elif 270 <= labmda <= 300:
            return -1.57 * labmda + 474
        
    def light_chlorophyllB(self, x):
        # chlorophyll B probability function
        labmda = x - 400
        if 0 <= labmda < 68:
            return 1.18 * labmda + 10
        elif 68 <= labmda < 90:
            return -3.9 * labmda + 352
        elif 90 <= labmda < 210:
            return 5
        elif 210 <= labmda < 250:
            return 0.57 * labmda - 113
        elif 250 <= labmda <= 300:
            return -6 * labmda + 180
        
    def light_beta_carotene(self, x):
        # Beta carotene probability function
        labmda = x - 400
        if 0 <= labmda < 50:
            return 0.86 * labmda + 27
        elif 50 <= labmda < 90:
            return 70
        elif 90 <= labmda < 100:
            return -7 * labmda + 700
        elif 100 <= labmda <= 300:
            return 0
    
# Define photosystems
photosystem1 = Photosystem(23, 12, 40)
photosystem2 = Photosystem(23, 12, 40)

def synthase_of_glicose():
    # Inverse glycolysis
    stroma_system.do_reaction(2*[PGAL_S, ADP], 2*[ATP]+[GLICOSE])


def calvin_cicle():
    # Fixation of carbon
    stroma_system.do_reaction([CARBON_DIOXIDE]+[RUDP]+2*[ATP], 2*[ADP, PGA])
    # Synthase of organic molecules
    stroma_system.do_reaction(2*[PGA, NADPH], 2*[NADPP, PGAL])
    # Regeneration of diphosphate ribulose
    stroma_system.do_reaction(5*[PGAL]+3*[ATP], [PGAL_S]+3*[ADP, RUDP])


def atpase():
    global inner_thylakoid_system, stroma_system
    # Maintain the concentration gradient
    if inner_thylakoid_system.length(HYDROGEN_CATION) > stroma_system.length(HYDROGEN_CATION):
        inner_thylakoid_system.remove_molecule(HYDROGEN_CATION)
        stroma_system.add_molecule(HYDROGEN_CATION)
        # Synthase of ATP
        if stroma_system.length(ADP) >= 1 and inner_thylakoid_system.length(HYDROGEN_CATION) >= 1:
            stroma_system.do_reaction([ADP], [ATP])


def water_photolysis():
    if photosystem1.electrons == 0 and inner_thylakoid_system.length(WATER) > 0:
        inner_thylakoid_system.do_reaction([WATER], 2*[HYDROGEN_CATION]+[OXYGEN_ATOM])
        if inner_thylakoid_system.length(OXYGEN_ATOM) > 1:
            inner_thylakoid_system.do_reaction(2*[OXYGEN_ATOM], [OXYGEN])

        photosystem1.electrons += 2
        

def protein_hydro():
    # This protein does active transport of hydrogen ions
    if transport_electrons[0] >= 2 and stroma_system.length(HYDROGEN_CATION) >= 2: 
        for i in range(0, 2):
            inner_thylakoid_system.add_molecule(HYDROGEN_CATION)
            stroma_system.remove_molecule(HYDROGEN_CATION)

        transport_electrons[0] -= 2
        photosystem2.electrons += 2 


def nadpp_reduction():
    if transport_electrons[1] >= 2 and stroma_system.length(HYDROGEN_CATION) >= 2 and stroma_system.length(NADPP) >= 1:
        stroma_system.do_reaction([NADPP]+2*[HYDROGEN_CATION], [NADPH, HYDROGEN_CATION])
        transport_electrons[1] -= 2


def show_status():
    # Print all variables
    print(f'Thylakoid: Water {inner_thylakoid_system.length(WATER)} | Oxygen {inner_thylakoid_system.length(OXYGEN)} | H+ {inner_thylakoid_system.length(HYDROGEN_CATION)}  ', end='/  ')
    print(f'Stroma: ADP {stroma_system.length(ADP)} | ATP {stroma_system.length(ATP)} | NAPH+ {stroma_system.length(NADPP)} | NADPH {stroma_system.length(NADPH)} | CO2 {stroma_system.length(CARBON_DIOXIDE)} | PGAL {stroma_system.length(PGAL_S)} | Glicose {stroma_system.length(GLICOSE)} | H+ {stroma_system.length(HYDROGEN_CATION)} | Ep1 {photosystem1.energy:.2f} | Ep2 {photosystem2.energy:.2f}')


def simulation(h2o, co2, rudp, adp, nadpp, oxi_energy, intensity, radiation_intervales):
    light_intensity = intensity

    # Get random value of radiation between intervales 
    random_radiations = []
    for radiation in radiation_intervales:
        random_radiations.append(randint(radiation[0], radiation[1]))
    
    # Get the final radiation value
    final_radiation = random_radiations[randint(0, len(radiation_intervales) - 1)]

    global inner_thylakoid_system, stroma_system
    inner_thylakoid_system = System(h2o * [WATER])
    stroma_system = System(adp*[ADP] + nadpp*[NADPP] + co2*[CARBON_DIOXIDE] + rudp*[RUDP])
    
    # Heart of the program
    while True:
        # Photosystem1 get energy from light and use it
        # to oxidate electrons
        for i in range(0, light_intensity):
            photosystem1.photo_reaction(final_radiation)
            photosystem1.check_oxidation(0, oxi_energy)
            water_photolysis()
        
        # Generate balance of hydrogen ions
        protein_hydro()
        
        # Photosystem2 energizes electros to produce NADPH
        for i in range(0, light_intensity):
            photosystem2.photo_reaction(final_radiation)
            photosystem2.check_oxidation(1, oxi_energy)
        
        atpase()
        nadpp_reduction()
        calvin_cicle()
        synthase_of_glicose()
        
        show_status()
