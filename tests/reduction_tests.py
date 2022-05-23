import sys

from parser import TRSParser

if __name__ == '__main__':
    # assert len(sys.argv) == 2, "Not enough arguments supplied"
    # data = sys.argv[1]

    signature = dict(
        f=2, i=1, e=0
    )

    parser = TRSParser(signature=signature)
    parser.build()

    # term = parser.parse('f(i(e), f(e, e))')
    term = parser.parse('f(i(x), f(e, x))')

    associativity = (
            parser.parse('f(x, f(y, z))'),
            parser.parse('f(f(x, y), z)'))
    neutral_element = (
            parser.parse('f(e, x)'),
            parser.parse('x'))
    inverse = (
            parser.parse('f(i(x), x)'),
            parser.parse('e'))

    sigma_identities = [
        neutral_element, inverse
    ]

    print(term)
    print(term.reduction(sigma_identities), end='\n\n')
    print(term.reduction(sigma_identities), end='\n\n')
    # print(term.reduction_mod_e(sigma_identities), end='\n\n')
