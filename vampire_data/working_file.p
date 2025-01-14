% Define "lt" (less than) and "mt" (more than) as binary predicates

% Irreflexivity: No element is less than or more than itself
fof(irreflexivity_lt, axiom, ! [X]: ~lt(X, X)).
fof(irreflexivity_mt, axiom, ! [X]: ~mt(X, X)).

% Transitivity: If X < Y and Y < Z, then X < Z
fof(transitivity_lt, axiom, ! [X, Y, Z]: (lt(X, Y) & lt(Y, Z) => lt(X, Z))).

% Transitivity: If X > Y and Y > Z, then X > Z
fof(transitivity_mt, axiom, ! [X, Y, Z]: (mt(X, Y) & mt(Y, Z) => mt(X, Z))).

% Asymmetry: If X < Y, then Y is not less than X
fof(asymmetry_lt, axiom, ! [X, Y]: (lt(X, Y) => ~lt(Y, X))).

% Asymmetry: If X > Y, then Y is not greater than X
fof(asymmetry_mt, axiom, ! [X, Y]: (mt(X, Y) => ~mt(Y, X))).

% Define "lt" and "mt" as complementary relations
fof(lt_mt_complement, axiom, ! [X, Y]: (lt(X, Y) => ~mt(X, Y))).
fof(mt_lt_complement, axiom, ! [X, Y]: (mt(X, Y) => ~lt(X, Y))).

% Facts: Some example relations
fof(fact1, axiom, lt(a, b)). % a < b
fof(fact2, axiom, lt(b, c)). % b < c
fof(fact3, axiom, mt(c, d)). % c > d

% Conjecture: Prove that a < d (Choose one conjecture at a time)
fof(conjecture, conjecture, lt(a, c)).
