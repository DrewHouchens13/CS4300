from src import task2

def test_get_integer():
    result = task2.get_integer()
    assert isinstance(result, int)
    assert result == 42

def test_get_float():
    result = task2.get_float()
    assert isinstance(result, float)
    assert result == 3.14

def test_get_string():
    result = task2.get_string()
    assert isinstance(result, str)
    assert result == "hello world"

def test_get_boolean():
    result = task2.get_boolean()
    assert isinstance(result, bool)
    assert result is True
