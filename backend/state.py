from .predicate import Predicate
from .attribute import Attribute

#NOTE: Klasa definiująca obiekt stanu
class State:
    def __init__(self, predicate1: Predicate, predicate2: Predicate = None):
        if(predicate2):
            self.name = predicate1.name + " & " + predicate2.name
        else:
            self.name = predicate1.name

        self.attributes = []

    def add_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)

    def __str__(self):
        attributes_str = [attribute.__str__() for attribute in self.attributes]
        return f"{self.name} {attributes_str}"


    
        