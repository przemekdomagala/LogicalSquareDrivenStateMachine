from .predicate import Predicate

class State:
    def __init__(self, predicate1: Predicate, predicate2: Predicate = None):
        if(predicate2):
            self.name = predicate1.name + " & " + predicate2.name
        else:
            self.name = predicate1.name
        