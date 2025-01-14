from z3 import *
from .state import State
from .predicate import Predicate
from .attribute import Attribute

def prepare_states(states, variables):
    for state in states:
        attributes = state.attributes
        for attribute in attributes:
            if attribute.value["kind"] == "Value":
                if attribute.name not in variables:
                    value = attribute.value["value"]
                    name = attribute.name
                    if type(value) == int:
                        variables[name] = Int(name)
                    elif type(value) == float:
                        variables[name] = Real(name)
                    elif type(value) == str:
                        variables[name] = String(name)
                    elif type(value) == bool:
                        variables[name] = Bool(name)
            else:
                if attribute.name not in variables:
                    name = attribute.name
                    variables[name] = Real(name)

def prepare_conditions(variables, state):
    attributes = state.attributes
    conditions_arr = []
    for attribute in attributes:
        if attribute.value["kind"] == "Value":
            conditions_arr.append(create_cond(attribute.name, attribute.value["value"], variables))
        else:
            if attribute.value["bound_type"] == "Closed":
                conditions_arr.append(create_cond(attribute.name, attribute.value["start"], variables, 'greater_equal'))
                conditions_arr.append(create_cond(attribute.name, attribute.value["end"], variables, 'less_equal'))
            elif attribute.value["bound_type"] == "Open Both":
                conditions_arr.append(create_cond(attribute.name, attribute.value["start"], variables, 'greater'))
                conditions_arr.append(create_cond(attribute.name, attribute.value["end"], variables, 'less'))
            elif attribute.value["bound_type"] == "Open Start":
                conditions_arr.append(create_cond(attribute.name, attribute.value["start"], variables, 'greater'))
                conditions_arr.append(create_cond(attribute.name, attribute.value["end"], variables, 'less_equal'))
            elif attribute.value["bound_type"] == "Open End":
                conditions_arr.append(create_cond(attribute.name, attribute.value["start"], variables, 'greater_equal'))
                conditions_arr.append(create_cond(attribute.name, attribute.value["end"], variables, 'less'))

    return conditions_arr

        

def create_cond(name, range_end, variables, inequality_type = 'equal'):
    if inequality_type == 'greater':
        return variables[name] > range_end
    elif inequality_type == 'greater_equal':
        return variables[name] >= range_end
    elif inequality_type == 'less':
        return variables[name] < range_end
    elif inequality_type == 'less_equal':
        return variables[name] <= range_end
    elif inequality_type == 'equal':
        return variables[name] == range_end
    else:
        raise Exception("Unknown inequality type")

def check_disjointness(states):
    variables = {}
    prepare_states(states, variables)

    prove_states = []
    for state in states:
        prove_states.append(And(prepare_conditions(variables, state)))

    solver = Solver()
    n = len(prove_states)
    disjoint = True
    result_str = ""
    for i in range(n):
        for j in range(i + 1, n):
            overlap_query = And(prove_states[i], prove_states[j])
            solver.push() 
            solver.add(overlap_query)
            if solver.check() == sat:
                disjoint = False
                result_str += f"States {i+1} and {j+1} are not disjoint.\n"
                result_str += "Example of overlapping values:\n"
                result_str += str(solver.model())
                print(f"States {i+1} and {j+1} are not disjoint.")
                print("Example of overlapping values:")
                print(solver.model())
            solver.pop()  
    if disjoint:
        result_str += "All states are disjoint."
        print("All states are disjoint.")
    else:
        result_str += "Some states overlap."
        print("Some states overlap.")
    return result_str

if __name__ == "__main__":
    state1 = State(Predicate("state1"))
    state1.add_attribute(Attribute("velocity", {"kind": "Range", "start": 20.0, "end": 100.0, "bound_type": "Open Start"}))
    state1.add_attribute(Attribute("weight", {"kind": "Value", "value": 15}))
    state1.add_attribute(Attribute("error_message", {"kind": "Value", "value": "Velocity must be greater than 20 and weight must be 15"}))

    state2 = State(Predicate("state2"))
    state2.add_attribute(Attribute("velocity", {"kind": "Range", "start": 100.01, "end": 100.0, "bound_type": "Closed"}))
    state2.add_attribute(Attribute("weight", {"kind": "Value", "value": 15}))
    state2.add_attribute(Attribute("error_message", {"kind": "Value", "value": "Velocity must be greater than 20 and weight must be 15"}))

    states = [state1, state2]

    check_disjointness(states)

