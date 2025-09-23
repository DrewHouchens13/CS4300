'''
Implement a unit test using pytest to test case for each
data type, ensuring that the script’s behavior matches the expected outcomes.
'''

from src import task2

'''
test_get_integer()
Purpose: Check get_interger() returns correct type
'''
def test_get_integer():
    result = task2.get_integer()
    assert isinstance(result, int)
    assert result == 42

'''
test_get_float()
Purpose: Check get_float() returns correct type
'''
def test_get_float():
    result = task2.get_float()
    assert isinstance(result, float)
    assert result == 3.14

'''
test_get_string()
Purpose: Check get_string() returns correct type
'''
def test_get_string():
    result = task2.get_string()
    assert isinstance(result, str)
    assert result == "hello world"


'''
test_get_boolean()
Purpose: Check get_boolean() returns correct type
'''
def test_get_boolean():
    result = task2.get_boolean()
    assert isinstance(result, bool)
    assert result is True
