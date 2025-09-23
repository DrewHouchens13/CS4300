'''
Implement pytest test cases to verify the correctness of your code 
for each function, using parameterized tests.
'''

import pytest
from src import task2


'''
test_data_types(func, expected_type, expected_value)
Purpose: Verify that each getter function returns the correct type and value.
'''
@pytest.mark.parametrize("func, expected_type, expected_value", [
    (task2.get_integer, int, 42),
    (task2.get_float, float, 3.14),
    (task2.get_string, str, "hello world"),
    (task2.get_boolean, bool, True),
])
def test_data_types(func, expected_type, expected_value):
    result = func()
    assert isinstance(result, expected_type)
    assert result == expected_value
