''' 
task3.py Create an if statement to check if a given number is positive,
negative, or zero. Implement a for loop to print the first 10 prime numbers (you may need to
research how to calculate prime numbers). Create a while loop to find the sum of all numbers from
1 to 100. 
''' 


"""
check_sign(n)
Returns:
    - "positive" if n > 0
    - "negative" if n < 0
    - "zero" if n == 0
"""
def check_sign(n):

    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


"""
first_n_primes(n)
Returns a list of the first n prime numbers.
"""
def first_n_primes(n):

    primes = []
    candidate = 2

    while len(primes) < n:
        is_prime = True

        for p in primes:
            if candidate % p == 0:
                is_prime = False

        if is_prime:
            primes.append(candidate)

        candidate += 1
    return primes


"""
sum_1_to_n(n)
Returns the sum of all integers from 1 to n inclusive.
"""
def sum_1_to_n(n):
    total = 0
    i = 1

    while i <= n:
        total += i
        i += 1

    return total

