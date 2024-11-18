from .predicate import Predicate

#NOTE: Klasa definiująca obiekt kwadratu logicznego
class SquareOfOpposition:
    def __init__(self, predicates: list[Predicate]):
        self._predicates = predicates
        self._identify_predicates()

    def _identify_predicates(self):
        self._initial = self._predicates[0] 
        self._contrary = None
        self._contradictory = None
        self._subalternate = None

        for i in range(1, len(self._predicates)):
            if(self._predicates[i] is None):
                continue

            if(self._predicates[i].contrary_to_initial):
                self._contrary = self._predicates[i]
            elif(self._predicates[i].contradictory_to_initial):
                self._contradictory = self._predicates[i]
            elif(self._predicates[i].subalternate_to_initial):
                self._subalternate = self._predicates[i]

        # self._contrary = self.__filter_predicates("contrary_to_initial")
        # self._contradictory = self.__filter_predicates("contradictory_to_initial")
        # self._subalternate = self.__filter_predicates("subalternate_to_initial")
    
    #NOTE: Metoda zwracająca predykat o konkretnej relacji względem predykatu początkowego
    # def __filter_predicates(self, parameter: str) -> Predicate:
    #     predicate = [predicate for predicate in self._predicates if getattr(predicate, parameter)]
    #     if predicate:
    #         return predicate[0]
    #     return None