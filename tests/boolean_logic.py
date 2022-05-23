"""

    double_negation = (
        parser.parse('not(not(x))'),
        parser.parse('x'))
    de_morgan_and_1 = (
        parser.parse('not(and(x, y))'),
        parser.parse('or(not(x), not(y))'))
    de_morgan_or_1 = (
        parser.parse('not(or(x, y))'),
        parser.parse('and(not(x), not(y))'))
    distributivity_1 = (
        parser.parse(''),
        parser.parse('')
"""
