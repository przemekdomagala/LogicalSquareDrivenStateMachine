from typing import List

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.states_variant import StatesVariant
from backend.state import State
from backend.predicate import Predicate

#NOTE: Klasa odpowiedzialna za idenfikację stanów na podstawie kwadratu logicznego
class StatesIdentifier:
    
    #NOTE: Identifikacja stanów na podstawie kwadratu logicznego
    def _idenfity_states(self, leaves: List[str]) -> List[State]:
        state_variant = self.__identify_states_variant(leaves)
        print(state_variant)

        initial = Predicate(leaves[0])
        subalternate = Predicate(leaves[2])
        contradictory = Predicate(leaves[3])
        contrary = Predicate(leaves[1])
        
        match state_variant:
            case StatesVariant.INITIAL_ONLY:
                return [State(initial)]
            case StatesVariant.INITIAL_CONTRARY:
                return [State(initial), State(contrary)]
            case StatesVariant.INITIAL_CONTRADICTORY:
                return [State(initial), State(contradictory)]
            case StatesVariant.INITIAL_SUBALTERNATE:
                return [State(initial, subalternate), State(subalternate)]
            case StatesVariant.INITIAL_CONTRARY_CONTRADICTORY:
                state_initial = State(initial)
                state_contrary_contradictory = State(contrary, contradictory)
                return [state_initial, state_contrary_contradictory]
            case StatesVariant.INITIAL_SUBALTERNATE_CONTRADICTORY:
                state_initial_subalternate = State(initial, subalternate)
                state_subalternate_contradictory = State(subalternate, contradictory)
                return [state_initial_subalternate, state_subalternate_contradictory]
            case StatesVariant.INITIAL_CONTRARY_SUBALTERNATE:
                state_initial_subalternate = State(initial, subalternate)
                state_contrary = State(contrary)
                return [state_initial_subalternate, state_contrary]
            case StatesVariant.ALL_PREDICATES:
                state_initial_subalternate = State(initial, subalternate)
                state_subalternate_contradictory = State(subalternate, contradictory)
                state_contrary_contradictory = State(contrary, contradictory)
                return [state_initial_subalternate, state_contrary_contradictory, state_subalternate_contradictory]
            case _:
                return []
    
    #NOTE: Metoda identyfikująca z jakim wariantem kwadratu mamy do czynienia
    def __identify_states_variant(self, leaves: List[str]) -> StatesVariant:
        pass
        if '' not in leaves:
            return StatesVariant.ALL_PREDICATES

        subalternate = leaves[2]
        contradictory = leaves[3]
        contrary = leaves[1]

        if not subalternate:
            if not contradictory and not contrary:
                return StatesVariant.INITIAL_ONLY
            if not contrary:
                return StatesVariant.INITIAL_CONTRADICTORY
            if not contradictory:
                return StatesVariant.INITIAL_CONTRARY
            return StatesVariant.INITIAL_CONTRARY_CONTRADICTORY

        if not contradictory:
            if not contrary:
                return StatesVariant.INITIAL_SUBALTERNATE
            return StatesVariant.INITIAL_CONTRARY_SUBALTERNATE

        if not contrary:
            return StatesVariant.INITIAL_SUBALTERNATE_CONTRADICTORY

        return StatesVariant.INITIAL_ONLY
