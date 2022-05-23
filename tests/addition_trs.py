import sys

from parser import TRSParser
from helpers import make_successor_nbr, translate_successor_number, total_reduce


if __name__ == '__main__':
    # assert len(sys.argv) == 2, "Not enough arguments supplied"
    # data = sys.argv[1]

    signature = {
        'add': 2, 's': 1, '0': 0, 'mul': 2,
        'factorial': 1,
        'fib': 1
    }

    parser = TRSParser(signature=signature)
    parser.build()

    # (2 + 1) * (2 + 1)
    term = parser.parse('mul(add(s(s(0)), s(0)), add(s(s(0)), s(0)))')

    addition = (
            parser.parse('add(n, s(m))'),
            parser.parse('s(add(n, m))'))
    neutral_element_add = (
            parser.parse('add(n, 0)'),
            parser.parse('n'))
    multiplication = (
            parser.parse('mul(n, s(m))'),
            parser.parse('add(n, mul(n, m))'))
    neutral_element_mul = (
            parser.parse('mul(n, 0)'),
            parser.parse('0'))
    '''
        Factorial 
        
        factorial(0) = 1
        factorial(n) = n * factorial(n - 1)
    '''
    factorial_r1 = (
        parser.parse('factorial(0)'),
        parser.parse('s(0)')
    )
    factorial_r2 = (
        parser.parse('factorial(s(n))'),
        parser.parse('mul(s(n), factorial(n))')
    )
    '''
        Fibonacci sequence
        
        fib(0) = 0
        fib(1) = 1
        fib(n) = fib(n - 1) + fib(n - 2)
    '''
    fib_r1 = (
        parser.parse('fib(0)'),
        parser.parse('0')
    )
    fib_r2 = (
        parser.parse('fib(s(0))'),
        parser.parse('s(0)')
    )
    fib_r3 = (
        parser.parse('fib(s(s(n)))'),
        parser.parse('add(fib(s(n)), fib(n))')
    )
    sigma_identities = [
        addition, neutral_element_add, multiplication, neutral_element_mul,
        factorial_r1, factorial_r2,
        fib_r1, fib_r2, fib_r3
    ]

    # (2 + 1) * (2 + 1)
    # mul(add(s(s(0)), s(0)), add(s(s(0)), s(0)))
    print(term)
    term = total_reduce(term, sigma_identities)
    print(term)
    print(translate_successor_number(str(term)), end='\n\n')

    term = parser.parse(f'factorial({make_successor_nbr(3)})')
    print(term)
    term = total_reduce(term, sigma_identities)
    print(term)
    print(translate_successor_number(str(term)), end='\n\n')

    term = parser.parse(f'fib({make_successor_nbr(4)})')
    print(term)
    term = total_reduce(term, sigma_identities)
    print(term)
    print(translate_successor_number(str(term)), end='\n\n')



