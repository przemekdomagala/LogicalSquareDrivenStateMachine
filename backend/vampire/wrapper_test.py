from vampire import Vampire

def check_logical_disjointness(state1, state2):
    """
    Function to check logical disjointness between two logical states using Vampire.

    Parameters:
        state1 (str): The first logical state in formal logic representation.
        state2 (str): The second logical state in formal logic representation.

    Returns:
        bool: True if the states are logically disjoint, False otherwise.
    """
    # Create Vampire instance
    vampire_instance = Vampire()

    # Construct the query to check if both states can be true simultaneously
    query = f"{state1} & {state2}"

    # Negate the query to check for inconsistency
    negated_query = f"~({query})"

    # Use Vampire to check satisfiability of the negated query
    is_satisfiable = vampire_instance.is_satisfiable(negated_query)

    # If the negated query is satisfiable, states are not disjoint
    return not is_satisfiable

# Example usage
if __name__ == "__main__":
    state1 = "P(x)"
    state2 = "~P(x)"

    if check_logical_disjointness(state1, state2):
        print("The states are logically disjoint.")
    else:
        print("The states are not logically disjoint.")
