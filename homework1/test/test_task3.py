'''
Write pytest test cases to verify the correctness of your code for each control structure.
'''

from src import task3

'''
test_check_sign()
Purpose: Validate check_sign returns correct string on proper input
'''
def test_check_sign():
    assert task3.check_sign(5) == "positive"
    assert task3.check_sign(-2) == "negative"
    assert task3.check_sign(0) == "zero"

'''
test_first_n_primes()
Purpose: Ensure first_n_primes returns the correct list of numbers
'''
def test_first_n_primes():
    assert task3.first_n_primes(5) == [2, 3, 5, 7, 11]

'''
test_sum_1_to_n()
Purpose: Test sum_1_to_n correctly performs addition
'''
def test_sum_1_to_n():
    assert task3.sum_1_to_n(10) == 55 
    assert task3.sum_1_to_n(100) == 5050
