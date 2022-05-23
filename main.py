import sys

from parser import TRSParser
from tree import print_mapping

if __name__ == '__main__':
    assert len(sys.argv) == 2, "Not enough arguments supplied"
    data = sys.argv[1]

    signature = dict(
        f=2, i=1, e=0
    )

    parser = TRSParser(signature=signature)
    parser.build()

    # tree = parser.parse("f(t, i(f(x, i(y))))")
    # print(repr(tree))
    # print(tree)
    #
    # print(tree['21'])
    #
    # new = parser.parse('f(x, y)')
    # print(new)
    #
    # print('Replacing tree[21] with new')
    # tree['21'] = new
    # print(tree)
    # print(repr(tree))
    # test variable substitutions

    tr = parser.parse('f(i(f(x, y)), f(i(y), f(y, z)))')
    print(tr)
    # print(repr(tr))
    substitutions = dict(
        x=parser.parse('f(x, i(y))'),
        y=parser.parse('x'),
        z=parser.parse('f(x, e)')
    )

    new = tr.copy()
    new.substitute_variables(substitutions)

    print(tr)
    print(new)

    is_mapping, mapping = new.is_instance_from(tr)
    if is_mapping:
        print_mapping(mapping)

    # print(tr)
    # print(len(tr))
    # print(tr.get_variable_positions())
    # print(tr.get_variables())
    # print(tr == tr)
    # print(tr == parser.parse('f(x, i(y))'))


    # parser = TRSParser(signature=signature)
    # parser.build()
    # tr = parser.parse('function(a)')

    # print(repr(tr))
    # print(tr)
