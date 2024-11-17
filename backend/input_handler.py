from typing import List
from .predicate import Predicate

class InputHandler:
    def _get_predicates(self) -> List[Predicate]:
        A, E, I, O = "", "", "", ""
        
        A = input("Podaj predykat A: ")
        if(A == ""):
            A = input("Spróbuj ponownie: ")
        if(A == ""):
            print("Nie podano predykatu A")
            return
        
        E = input("Podaj predykat E, jeśli nie chcesz podawać wciśnij enter: ")
        O = input("Podaj predykat O, jeśli nie chcesz podawać wciśnij enter: ")
        I = input("Podaj predykat I, jeśli nie chcesz podawać wciśnij enter: ")
        
        predicates = self.__create_predicates([A, E, O, I])

        return predicates

    def __create_predicates(self, predicates: List[str]) -> List[Predicate]:
        initial_predicate = Predicate(predicates[0])
        contrary_to_initial = Predicate(predicates[1], contrary_to_initial=True) if predicates[1] != "" else None
        contradictory_to_initial = Predicate(predicates[2], contradictory_to_initial=True) if predicates[2] != "" else None
        subalternate_to_initial = Predicate(predicates[3], subalternate_to_initial=True) if predicates[3] != "" else None

        return [initial_predicate, contrary_to_initial, contradictory_to_initial, subalternate_to_initial]