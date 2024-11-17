from .states_identifier import StatesIdentifier

#NOTE: Klasa definiująca obiekt maszyny stanów
class StateMachine:
    def __init__(self, square_of_opposition):
        state_identifier = StatesIdentifier()
        square_of_opposition = square_of_opposition
        self.states = state_identifier._idenfity_states(square_of_opposition)
