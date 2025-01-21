from abc import ABC, abstractmethod

# Interface representing a state
class State(ABC):
    # Abstract method to handle an event in the context
    @abstractmethod
    def handle_event(self, context):
        pass

class s(State):
   def handle_event(self, context):


class Context:
    def __init__(self):
        # Setting initial state to State1a
        self.current_state = s
    # Method to set the current state
    def set_state(self, state):
        self.current_state 
    # Method to handle an event
    def handle_event(self):
        # Delegating event to the current state
        self.current_state.handle_event(self)

if __name__ == "__main__":
    context = Context()
    for i in range(0):
        context.handle_event()