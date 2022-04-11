import ply.lex as lex
import sys

from parser import TRSParser

# List of token names.   This is always required
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'


# A regular expression rule with some action code
# Token type            t.type
# Token value(lexeme)   t.value
# Current line          t.lineno
# Text position         t.lexpos
# Compiled lexer        t.lexer
def t_NUMBER(t):
    r"""\-*[0-9]+"""
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':
    assert len(sys.argv) == 2, "Not enough arguments supplied"
    data = sys.argv[1]

    signature = dict(
        f=2, i=1, e=0
    )

    parser = TRSParser(signature=signature)
    parser.build()
    tree = parser.parse(data)
    new = parser.parse('f(x, y)')

    print(tree)
    print(new)
    print(tree['21'])

    print('Replacing tree[21] with new')
    tree['21'] = new
    print(tree)
    # "f(t, i(f(x, i(y))))"