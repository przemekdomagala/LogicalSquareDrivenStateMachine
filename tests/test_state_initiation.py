from backend.square_of_opposition import SquareOfOpposition
from backend.state_machine import StateMachine

def test_predicates_initiaion_all_predicates(all_predicates):

    assert len(all_predicates) == 4

def test_states_initiation_all_predicates(all_predicates):
    square_of_opposition = SquareOfOpposition(all_predicates)
    assert square_of_opposition._initial.name == "A1"
    assert square_of_opposition._contrary.name == "E1"
    assert square_of_opposition._contradictory.name == "O1"
    assert square_of_opposition._subalternate.name == "I1"
    
    state_machine = StateMachine(square_of_opposition)
    assert len(state_machine.states) == 3
    assert state_machine.states[0].name == "A1 & I1"
    assert state_machine.states[1].name == "E1 & O1"
    assert state_machine.states[2].name == "I1 & O1"

def test_states_initiation_a_e_i_predicates(a_e_i_predicates):
    square_of_opposition = SquareOfOpposition(a_e_i_predicates)
    assert square_of_opposition._initial.name == "A1"
    assert square_of_opposition._contrary.name == "E1"
    assert square_of_opposition._contradictory is None
    assert square_of_opposition._subalternate.name == "I1"
    
    state_machine = StateMachine(square_of_opposition)
    assert len(state_machine.states) == 2
    assert state_machine.states[0].name == "A1 & I1"
    assert state_machine.states[1].name == "E1"

def test_states_initiation_a_o_i_predicates(a_o_i_predicates):
    square_of_opposition = SquareOfOpposition(a_o_i_predicates)
    assert square_of_opposition._initial.name == "A1"
    assert square_of_opposition._contrary is None
    assert square_of_opposition._contradictory.name == "O1"
    assert square_of_opposition._subalternate.name == "I1"
    
    state_machine = StateMachine(square_of_opposition)
    assert len(state_machine.states) == 2
    assert state_machine.states[0].name == "A1 & I1"
    assert state_machine.states[1].name == "I1 & O1"

def test_state_initiation_a_e_o_predicates(a_e_o_predicates):
    square_of_opposition = SquareOfOpposition(a_e_o_predicates)
    assert square_of_opposition._initial.name == "A1"
    assert square_of_opposition._contrary.name == "E1"
    assert square_of_opposition._contradictory.name == "O1"
    assert square_of_opposition._subalternate is None
    
    state_machine = StateMachine(square_of_opposition)
    assert len(state_machine.states) == 2
    assert state_machine.states[0].name == "A1"
    assert state_machine.states[1].name == "E1 & O1"

def test_state_initiation_a_i_predicates(a_i_predicates):
    square_of_opposition = SquareOfOpposition(a_i_predicates)
    assert square_of_opposition._initial.name == "A1"
    assert square_of_opposition._contrary is None
    assert square_of_opposition._contradictory is None
    assert square_of_opposition._subalternate.name == "I1"
    
    state_machine = StateMachine(square_of_opposition)
    assert len(state_machine.states) == 2
    assert state_machine.states[0].name == "A1 & I1"
    assert state_machine.states[1].name == "I1"

def test_state_initiation_a_e_predicates(a_e_predicates):
    square_of_opposition = SquareOfOpposition(a_e_predicates)
    assert square_of_opposition._initial.name == "A1"
    assert square_of_opposition._contrary.name == "E1"
    assert square_of_opposition._contradictory is None
    assert square_of_opposition._subalternate is None
    
    state_machine = StateMachine(square_of_opposition)
    assert len(state_machine.states) == 2
    assert state_machine.states[0].name == "A1"
    assert state_machine.states[1].name == "E1"

def test_state_initiation_a_o_predicates(a_o_predicates):
    square_of_opposition = SquareOfOpposition(a_o_predicates)
    assert square_of_opposition._initial.name == "A1"
    assert square_of_opposition._contrary is None
    assert square_of_opposition._contradictory.name == "O1"
    assert square_of_opposition._subalternate is None
    
    state_machine = StateMachine(square_of_opposition)
    assert len(state_machine.states) == 2
    assert state_machine.states[0].name == "A1"
    assert state_machine.states[1].name == "O1"

def test_state_initiation_a_predicate(a_predicate):
    square_of_opposition = SquareOfOpposition(a_predicate)
    assert square_of_opposition._initial.name == "A1"
    assert square_of_opposition._contrary is None
    assert square_of_opposition._contradictory is None
    assert square_of_opposition._subalternate is None
    
    state_machine = StateMachine(square_of_opposition)
    assert len(state_machine.states) == 1
    assert state_machine.states[0].name == "A1"