from unittest.mock import patch
from backend.input_handler import InputHandler
import pytest
from backend.predicate import Predicate
from typing import List

@pytest.fixture
def mock_input():
    with patch('builtins.input') as mocked_input:
        yield mocked_input

@pytest.fixture
def all_predicates(mock_input) -> List[Predicate]:
    mock_input.side_effect = ["A1", "E1", "O1", "I1"]
    input_handler = InputHandler()
    return input_handler._get_predicates()

@pytest.fixture
def a_e_i_predicates(mock_input) -> List[Predicate]:
    mock_input.side_effect = ["A1", "E1", "", "I1"]
    input_handler = InputHandler()
    return input_handler._get_predicates()

@pytest.fixture
def a_o_i_predicates(mock_input) -> List[Predicate]:
    mock_input.side_effect = ["A1", "", "O1", "I1"]
    input_handler = InputHandler()
    return input_handler._get_predicates()

@pytest.fixture
def a_e_o_predicates(mock_input) -> List[Predicate]:
    mock_input.side_effect = ["A1", "E1", "O1", ""]
    input_handler = InputHandler()
    return input_handler._get_predicates()

@pytest.fixture
def a_i_predicates(mock_input) -> List[Predicate]:
    mock_input.side_effect = ["A1", "", "", "I1"]
    input_handler = InputHandler()
    return input_handler._get_predicates()

@pytest.fixture
def a_e_predicates(mock_input) -> List[Predicate]:
    mock_input.side_effect = ["A1", "E1", "", ""]
    input_handler = InputHandler()
    return input_handler._get_predicates()

@pytest.fixture
def a_o_predicates(mock_input) -> List[Predicate]:
    mock_input.side_effect = ["A1", "", "O1", ""]
    input_handler = InputHandler()
    return input_handler._get_predicates()

@pytest.fixture
def a_predicate(mock_input) -> List[Predicate]:
    mock_input.side_effect = ["A1", "", "", ""]
    input_handler = InputHandler()
    return input_handler._get_predicates()


