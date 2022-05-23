import sys

from parser import TRSParser
from tree import print_mapping

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
    new = parser.parse('f(x, y)')
    term['1'] = new
    od = parser.parse('i(i(z))')
    term['12'] = od

    print(term)
    print(repr(term))
    print_mapping(term.cache)
    # print(term.reduction(sigma_identities), end='\n\n')
    # print(term.reduction_mod_e(sigma_identities), end='\n\n')
