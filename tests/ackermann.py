import sys

import unittest
from parser import TRSParser
from helpers import make_successor_nbr, translate_successor_number, total_reduce

if __name__ == '__main__':
    # assert len(sys.argv) == 2, "Not enough arguments supplied"
    # data = sys.argv[1]

    signature = {
        'a': 2, 's': 1, '0': 0
    }

    parser = TRSParser(signature=signature)
    parser.build()

    '''
        Ackermann function
    
        r1: A(0, n) = n + 1
        r2: A(m + 1, 0) = A(m, 1)
        r3: A(m + 1, n + 1) = A(m, A(m + 1, n))
        
        A(2, 1) = 5
    '''

    r1 = (
        parser.parse('a(0, n)'),
        parser.parse('s(n)'))
    r2 = (
        parser.parse('a(s(m), 0)'),
        parser.parse('a(m, s(0))'))
    r3 = (
        parser.parse('a(s(m), s(n))'),
        parser.parse('a(m, a(s(m), n))'))

    sigma_identities = [
        r1, r2, r3
    ]

    a = make_successor_nbr(2)
    b = make_successor_nbr(10)

    term = parser.parse(f'a({a}, {b})')
    print(term)

    term = total_reduce(term, sigma_identities, max_iter=5000, verbose=False)
    print(term)
    print(translate_successor_number(str(term)))
