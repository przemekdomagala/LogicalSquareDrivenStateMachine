from .predicate import Predicate

class SquareOfOpposition:
    def __init__(self, predicates: list[Predicate]):
        self._predicates = predicates
        self._identify_predicates()

    def _identify_predicates(self):
        self._initial = self._predicates[0] 
        self._contrary = self.__filter_predicates("contrary_to_initial")
        self._contradictory = self.__filter_predicates("contradictory_to_initial")
        self._subalternate = self.__filter_predicates("subalternate_to_initial")

        return
    
    def __filter_predicates(self, parameter: str) -> Predicate:
        predicate = [predicate for predicate in self._predicates if getattr(predicate, parameter)]
        if predicate:
            return predicate[0]
        return None