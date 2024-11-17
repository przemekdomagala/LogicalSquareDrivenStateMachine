#NOTE: Klasa definiująca obiekt predykatu
class Predicate:
    def __init__(self, name: str, contrary_to_initial: bool = False, contradictory_to_initial: bool = False, 
                 subalternate_to_initial: bool = False):
        self.name = name
        self.contrary_to_initial = contrary_to_initial
        self.contradictory_to_initial = contradictory_to_initial
        self.subalternate_to_initial = subalternate_to_initial
        

