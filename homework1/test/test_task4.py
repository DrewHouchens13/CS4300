'''
Write pytest test cases to test the calculate_discount function with
various types (integers, floats) for price and discount.
''' 

import pytest
from src import task4

def test_calculate_discount_with_ints():
    assert task4.calculate_discount(100, 20) == 80
    assert task4.calculate_discount(50, 0) == 50


def test_calculate_discount_with_floats():
    assert task4.calculate_discount(100.0, 25.5) == 74.5
    assert task4.calculate_discount(200.0, 10.0) == 180.0


def test_calculate_discount_mixed_types():

    # int price, float discount
    assert task4.calculate_discount(100, 12.5) == 87.5

    # float price, int discount
    assert task4.calculate_discount(99.99, 10) == 89.991


#also have to ensure that we test throwing errors correctly
def test_invalid_discount():
    with pytest.raises(ValueError):
        task4.calculate_discount(100, -5)
        
    with pytest.raises(ValueError):
        task4.calculate_discount(100, 150)