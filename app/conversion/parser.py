import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NUMBER',
    'CURRENCY',
    'TO'
)

t_TO = r'to'
t_CURRENCY = r'[A-Z]{3}'
t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_error(t):
    raise ValueError(f"Illegal character '{t.value[0]}'")

lexer = lex.lex()

def p_expression(p):
    'expression : NUMBER CURRENCY TO CURRENCY'
    p[0] = {'amount': p[1], 'from_currency': p[2], 'to_currency': p[4]}

def p_error(p):
    raise ValueError("Syntax error in input")

parser = yacc.yacc()

def parse_query(query):
    return parser.parse(query)