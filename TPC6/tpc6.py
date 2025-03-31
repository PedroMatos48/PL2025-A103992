import sys
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NUMBER',
    'PLUS', 'MINUS',
    'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN'
)

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_error(t):
    print(f"Caractere inválido: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'UMINUS')
)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            raise Exception("Erro: divisão por zero.")
        p[0] = p[1] / p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_error(p):
    print("Erro de sintaxe.")

parser = yacc.yacc()

def main():
    if len(sys.argv) < 2:
        print("Uso: python parser.py <expressão matemática>")
        return
    
    expression = sys.argv[1]
    try:
        resultado = parser.parse(expression)
        print(f"{expression} = {resultado}")
    except Exception as e:
        print(f"Erro ao avaliar '{expression}': {e}")

if __name__ == '__main__':
    main()
