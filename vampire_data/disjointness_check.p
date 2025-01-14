% This is a TPTP file to check the logical disjointness of two states

% State 1: Initial state
fof(state1, axiom, 
    (state(initial) & 
     property(p1) & 
     property(p2))
).

% State 2: Final state
fof(state2, axiom, 
    (state(final) & 
     property(p3) & 
     property(p4))
).

% Conjecture: State1 and State2 are disjoint
fof(disjointness, conjecture, 
    ~( (state(initial) & 
        property(p1) & 
        property(p2)) 
       & 
       (state(final) & 
        property(p3) & 
        property(p4))
     )
).

