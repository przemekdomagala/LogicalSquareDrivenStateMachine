from .input_handler import InputHandler
from .square_of_opposition import SquareOfOpposition
from .state_machine import StateMachine

#NOTE: Klasa odpowiedzialna za uruchomienie aplikacji
class App:
    def __init__(self):
        return
    
    def run(self):
        input_handler = InputHandler()
        predicates = input_handler._get_predicates()

        square_of_opposition = SquareOfOpposition(predicates)
        state_machine = StateMachine(square_of_opposition)