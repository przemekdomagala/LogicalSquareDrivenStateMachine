from .predicate import Predicate
from .attribute import Attribute
from .state import State


def generate_disjointness_check(state1: State, state2: State, filename: str):
    """
    Generate a .p file to check disjointness of two states in Vampire.

    :param state1: First state
    :param state2: Second state
    :param filename: Output file name
    """
    def format_attribute(attr):
        if attr.value["kind"] == "Value":
            return f"{attr.name} = {attr.value['value']}"
        elif attr.value["kind"] == "Range":
            start_cond = f"{attr.name} > {attr.value['start']}" if attr.value["bound_type"] in ["Open Start", "Open Both"] else f"{attr.name} >= {attr.value['start']}"
            end_cond = f"{attr.name} < {attr.value['end']}" if attr.value["bound_type"] in ["Open End", "Open Both"] else f"{attr.name} <= {attr.value['end']}"
            return f"({start_cond} & {end_cond})"
        return ""

    with open(filename, "w") as file:
        # Write header
        file.write("% Vampire Problem File: Disjointness Check\n")
        file.write("% Goal: Prove that two states are disjoint\n\n")

        # Define State 1
        file.write("fof(state1, axiom, (! [X] : (member(X, S1) <=> (")
        file.write(" & ".join([format_attribute(attr) for attr in state1.attributes]))
        file.write(")))).\n")

        # Define State 2
        file.write("fof(state2, axiom, (! [X] : (member(X, S2) <=> (")
        file.write(" & ".join([format_attribute(attr) for attr in state2.attributes]))
        file.write(")))).\n")

        # Conjecture: States are disjoint
        file.write("fof(disjointness_goal, conjecture, (~ (? [X] : (member(X, S1) & member(X, S2))))).\n")

    print(f"Disjointness check file generated: {filename}")


# Example Usage
if __name__ == "__main__":
    # Define predicates and attributes
    predicate1 = Predicate(name="State1_Predicate")
    predicate2 = Predicate(name="State2_Predicate")

    state1 = State(predicate1)
    state1.add_attribute(Attribute("velocity", {"kind": "Range", "start": 20.0, "end": 100.0, "bound_type": "Open Start"}))
    state1.add_attribute(Attribute("weight", {"kind": "Value", "value": 15}))
    state1.add_attribute(Attribute("error_message", {"kind": "Value", "value": "Velocity must be greater than 20 and weight must be 15"}))

    state2 = State(predicate2)
    state2.add_attribute(Attribute("velocity", {"kind": "Range", "start": 100.01, "end": 200.0, "bound_type": "Closed"}))
    state2.add_attribute(Attribute("weight", {"kind": "Value", "value": 15}))
    state2.add_attribute(Attribute("error_message", {"kind": "Value", "value": "Velocity must be greater than 20 and weight must be 15"}))

    # Generate the .p file
    generate_disjointness_check(state1, state2, "disjointness_check.p")



# Example Usage
if __name__ == "__main__":
    # Define predicates and attributes
    predicate1 = Predicate(name="State1_Predicate")
    predicate2 = Predicate(name="State2_Predicate")

    state1 = State(predicate1)
    state1.add_attribute(Attribute("velocity", {"kind": "Range", "start": 20.0, "end": 100.0, "bound_type": "Open Start"}))
    state1.add_attribute(Attribute("weight", {"kind": "Value", "value": 15}))
    state1.add_attribute(Attribute("error_message", {"kind": "Value", "value": "Velocity must be greater than 20 and weight must be 15"}))

    state2 = State(predicate2)
    state2.add_attribute(Attribute("velocity", {"kind": "Range", "start": 100.01, "end": 100.0, "bound_type": "Closed"}))
    state2.add_attribute(Attribute("weight", {"kind": "Value", "value": 15}))
    state2.add_attribute(Attribute("error_message", {"kind": "Value", "value": "Velocity must be greater than 20 and weight must be 15"}))

    # Generate the .p file
    generate_disjointness_check(state1, state2, "disjointness_check.p")
