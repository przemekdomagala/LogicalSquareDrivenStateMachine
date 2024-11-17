from .square_of_opposition import SquareOfOpposition
from .states_variant import StatesVariant
from .state import State
from typing import List

class StatesIdentifier:
    
    def _idenfity_states(self, square_of_opposition: SquareOfOpposition) -> List[State]:
        state_variant = self.__identify_states_variant(square_of_opposition)

        match state_variant:
            case StatesVariant.INITIAL_ONLY:
                return [State(square_of_opposition._initial)]
            case StatesVariant.INITIAL_CONTRARY:
                return [State(square_of_opposition._initial), State(square_of_opposition._contrary)]
            case StatesVariant.INITIAL_CONTRADICTORY:
                return [State(square_of_opposition._initial), State(square_of_opposition._contradictory)]
            case StatesVariant.INITIAL_SUBALTERNATE:
                return [State(square_of_opposition._initial, square_of_opposition._subalternate), State(square_of_opposition._subalternate)]
            case StatesVariant.INITIAL_CONTRARY_CONTRADICTORY:
                state_initial = State(square_of_opposition._initial)
                state_contrary_contradictory = State(square_of_opposition._contrary, square_of_opposition._contradictory)
                return [state_initial, state_contrary_contradictory]
            case StatesVariant.INITIAL_SUBALTERNATE_CONTRADICTORY:
                state_initial_subalternate = State(square_of_opposition._initial, square_of_opposition._subalternate)
                state_subalternate_contradictory = State(square_of_opposition._subalternate, square_of_opposition._contradictory)
                return [state_initial_subalternate, state_subalternate_contradictory]
            case StatesVariant.INITIAL_CONTRARY_SUBALTERNATE:
                state_initial_subalternate = State(square_of_opposition._initial, square_of_opposition._subalternate)
                state_contrary = State(square_of_opposition._contrary)
                return [state_initial_subalternate, state_contrary]
            case StatesVariant.ALL_PREDICATES:
                state_initial_subalternate = State(square_of_opposition._initial, square_of_opposition._subalternate)
                state_subalternate_contradictory = State(square_of_opposition._subalternate, square_of_opposition._contradictory)
                state_contrary_contradictory = State(square_of_opposition._contrary, square_of_opposition._contradictory)
                return [state_initial_subalternate, state_contrary_contradictory, state_subalternate_contradictory]
            case _:
                return []
    
    def __identify_states_variant(self, square_of_opposition: SquareOfOpposition) -> StatesVariant:
        if None not in square_of_opposition._predicates:
            return StatesVariant.ALL_PREDICATES

        subalternate = square_of_opposition._subalternate
        contradictory = square_of_opposition._contradictory
        contrary = square_of_opposition._contrary

        if not subalternate:
            if not contradictory and not contrary:
                return StatesVariant.INITIAL_CONTRARY
            if not contrary:
                return StatesVariant.INITIAL_CONTRADICTORY
            if not contradictory:
                return StatesVariant.INITIAL_CONTRARY_CONTRADICTORY
            return StatesVariant.INITIAL_ONLY

        if not contradictory:
            if not contrary:
                return StatesVariant.INITIAL_SUBALTERNATE
            return StatesVariant.INITIAL_CONTRARY_SUBALTERNATE

        if not contrary:
            return StatesVariant.INITIAL_SUBALTERNATE_CONTRADICTORY

        return StatesVariant.INITIAL_ONLY
