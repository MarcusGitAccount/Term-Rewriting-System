def print_mapping(mapping):
    for k, v in mapping.items():
        print(f'{k} -> {str(v)}')


def make_successor_nbr(n):
    if n == 0:
        return '0'
    return f's({make_successor_nbr(n - 1)})'


def translate_successor_number(n):
    """Assumes @param n is a well-formed successor number"""
    valid_chars = '()s0'
    stack = []
    for c in n:
        if c not in valid_chars:
            raise ValueError('Invalid successor number')
        if '(' == c:
            stack.append(1)
        elif ')' == c:
            if len(stack) == 0:
                raise ValueError('Invalid successor number')
            stack.pop()
    if len(stack) != 0:
        raise ValueError('Invalid successor number')
    return n.count('s')


def total_reduce(term, sigma_identities, max_iter=1000, verbose=False):
    i = 0

    while True:
        prev = str(term)  # we can kind of see it like hashing... right?
        term = term.reduction(sigma_identities, new_tree=True, verbose=verbose)
        # print(repr(term))
        # print_mapping(term.cache)
        if verbose:
            print(f'Term at iteration {i}: {str(term)}', end='\n\n')
        if str(term) == prev:
            print(f'Reduction has no effect after {i} iteration(s), will exit')
            break
        if verbose and i > 0 and i % 250 == 0:
            print(f'Checkpoint on iteration: {i}')
            print(f'Current term: {str(term)}')
        i += 1
        if i == max_iter:
            print('Reached maxed iteration, will exit')
            break
    return term
