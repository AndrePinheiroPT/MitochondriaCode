class Molecules:
    def __init__(self, molecular_form, name):
        self.molecular_form = molecular_form
        self.name = name

    def __eq__(self, other):
        if (isinstance(other, Molecules)):
            return self.molecular_form == other.molecular_form
        return False


class System:
    def __init__(self, entities):
        self.storage = []

        for entitie in entities:
            self.storage.append(entitie) 

    def do_reaction(self, reagents, reaction_products):
        for reagent in reagents:
            if self.storage.count(reagent) < reagents.count(reagent):
                return "it's impossible do the reaction!"
        
        for reagent in reagents:
            del self.storage[self.storage.index(reagent)]
        
        for product in reaction_products:
            self.storage.append(product)
        

    def add_molecule(self, molecule_object):
        self.storage.append(molecule_object)

    def remove_molecule(self, molecule_object):
        self.storage.remove(molecule_object)

    def length(self, molecule_object):
        return self.storage.count(molecule_object)
    
