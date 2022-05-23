#  Grammar to be parsed for our TRS(term rewriting system):
#
#
#  function_expression: ZERO_ARITY
#                     | FUNCTION_NAME LEFT_PAR expression RIGHT_PAR
#
#  expression:
#             | function_expression
#             | ID
#             | expression COMMA expression

import ply.lex as lex
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from tree import TreeNode, Tree


class TRSParser(object):
    ############################################
    #
    # Lex lexer tokens parsing definition
    #
    ############################################

    ZERO_ARITY_TOKEN = 'ZERO_ARITY'
    ID_TOKEN = 'ID'
    FUNCTION_NAME_TOKEN = 'FUNCTION_NAME'

    tokens = [
        ID_TOKEN,
        'COMMA',
        'LEFT_PAR',
        'RIGHT_PAR',
        ZERO_ARITY_TOKEN,
        FUNCTION_NAME_TOKEN
    ]

    t_LEFT_PAR = r'\('
    t_RIGHT_PAR = r'\)'
    t_COMMA = r'\,'

    t_ignore = ' \t\n\r'

    # @symbols - dict() consisting of function symbols and their arity
    def __init__(self, signature):
        self.parser = None
        self.tree = None
        self.lexer = None
        self.signature = signature
        self.variables = set()

    def t_error(self, t):
        msg = "Illegal character '%s'" % t.value[0]
        raise KeyError(msg)

    # Check for function symbols
    def t_ID(self, t):
        r"""[a-zA-Z_0-9]+"""
        token_type = TRSParser.ID_TOKEN

        if t.value in self.signature:
            arity = self.signature[t.value]
            token_type = TRSParser.ZERO_ARITY_TOKEN if arity == 0 else TRSParser.FUNCTION_NAME_TOKEN

        if TRSParser.ID_TOKEN == token_type:
            self.variables.add(t.value)

        t.type = token_type
        return t

    ############################################
    #
    # Yacc grammar syntax rules definitions
    #
    ############################################

    # def p_term_term(self, p):
    #     """term : function_expression"""
    #     p[0] = p[1]

    # def p_term_function(self, p):
    #     """term : function_expression"""
    #     p[0] = p[1]

    def p_term_variable(self, p):
        """expression : ID"""
        p[0] = TreeNode(value=p[1], is_variable=True)

    def p_function_expression_zero_arity(self, p):
        """function_expression : ZERO_ARITY"""
        p[0] = TreeNode(value=p[1], is_variable=False, children=[])

    def p_function_expression_higher_arity(self, p):
        """function_expression : FUNCTION_NAME LEFT_PAR expression RIGHT_PAR"""
        children = p[3]
        arity = self.signature[p[1]]

        if not isinstance(children, list):
            children = [children]

        node = TreeNode(value=p[1], is_variable=False, children=children, arity=arity)
        assert isinstance(children, list) and len(node.children) == arity, f'Expected arity of {arity} for \'{p[1]}\''

        p[0] = node

    # For the expression rules we need to create the children of the parent node
    # def p_expression_term(self, p):
    #     """expression : term"""
    #     p[0] = [p[1]]

    def p_expression_function(self, p):
        """expression : function_expression"""
        p[0] = p[1]

    def p_expression_expr(self, p):
        """expression : expression COMMA expression"""
        p[0] = p[1] + p[3]

    # Error rule for syntax errors
    def p_error(self, p):
        print(p)
        msg = "Syntax error"
        raise KeyError(msg)

    ############################################
    #
    # Wrapper additional methods
    #
    ############################################

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.parser = yacc.yacc(module=self)

    def parse(self, literal, **kwargs):
        verbose = kwargs.get('verbose', False)
        self.tree = None

        # if verbose:
        #     self.lexer.input(literal)
        #     for tok in self.lexer:
        #         print(tok)
        try:
            root_node = self.parser.parse(literal)
            return Tree(root=root_node, signature=self.signature)
        except BaseException as e:
            print(f"Invalid term\n{str(e)}")
            return None
