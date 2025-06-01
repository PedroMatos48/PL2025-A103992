import ply.yacc as yacc
from PascalLex import tokens
import re
import pprint
from test import ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10 

variables = {}
last_type = ""

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'DIFFERENT', 'LESS', 'GREATER', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVISION', 'DIV', 'MOD'),
    ('right', 'NOT'),
    ('nonassoc', 'ELSE')
)

def p_start(p):
    """start : PROGRAM identifier SEMICOLON main DOT"""
    p[0] = (p[2], p[4])

def p_main(p):
    """main : const_list var_list statement_list"""
    p[0] = ("MAIN", p[1], p[2], p[3])

def p_const_list(p):
    """const_list : CONST const_decls
                  | empty"""
    if len(p) == 3:
        p[0] = ("CONST", p[2])
    else:
        p[0] = ("CONST", [])

def p_const_decls(p):
    """const_decls : const_decls const_decl
                   | const_decl"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_const_decl(p):
    """const_decl : identifier EQUAL INTEGER SEMICOLON
                  | identifier EQUAL STRING SEMICOLON
                  | identifier EQUAL REAL SEMICOLON
                  | identifier EQUAL BOOLEAN SEMICOLON"""
                  
    p[0] = (p[1], p[3])



def p_var_list(p):
    """var_list : VAR var_decls
                | empty"""
    if len(p) == 3:
        p[0] = ("VARS", p[2])
    else:
        p[0] = ("VARS", [])

def p_var_decls(p):
    """var_decls : var_decls var_decl
                 | var_decl"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_var_decl(p):
    """var_decl : ident_list COLON type_decl SEMICOLON"""
    p[0] = (p[3], p[1])

def p_ident_list(p):
    """ident_list : identifier COMMA ident_list
                  | identifier"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_type_decl(p):
    """type_decl : ARRAY LBRACKET INTEGER DOT DOT INTEGER RBRACKET OF type
                 | ARRAY LBRACKET identifier DOT DOT identifier RBRACKET OF type
                 | ARRAY LBRACKET INTEGER DOT DOT identifier RBRACKET OF type
                 | ARRAY LBRACKET identifier DOT DOT INTEGER RBRACKET OF type
                 | type"""
    if len(p) == 10:
        p[0] = ("ARRAY", p[3], p[6], p[9])
    else:
        p[0] = p[1]

def p_type(p):
    """type : IDENTIFIER
            | TREAL
            | TINTEGER
            | TSTRING
            | TCHAR
            | TBOOLEAN"""
    p[0] = p[1]

def p_identifier(p):
    """identifier : IDENTIFIER LBRACKET expression RBRACKET
                  | IDENTIFIER"""
    if len(p) == 5:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

def p_statement_list(p):
    "statement_list : BEGIN statement_seq END"
    p[0] = ("STATEMENT_LIST", p[2])

def p_statement_seq(p):
    """statement_seq : statement_seq SEMICOLON statement
                     | statement_seq SEMICOLON
                     | statement"""
    if len(p) == 4:
        p[0] = p[1] + p[3]
    elif len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = p[1]

def p_statement(p):
    """statement : writeln
                 | write
                 | readln
                 | read
                 | assign
                 | if_stmt
                 | for_loop
                 | while_loop
                 | statement_list"""
    p[0] = [p[1]]

def p_assign(p):
    """assign : identifier ASSIGN expression"""
    p[0] = ("ASSIGN", p[1], p[3])

def p_expression_binop(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVISION expression
                  | expression DIV expression
                  | expression MOD expression"""
    token_map = {
        'PLUS': 'ADD',
        'MINUS': 'SUB',
        'TIMES': 'MUL',
        'DIVISION': 'RDIV',
        'DIV': 'DIV',
        'MOD': 'MOD'
    }
    p[0] = (token_map[p.slice[2].type], p[1], p[3])

def p_expression_comparison(p):
    """expression : expression EQUAL expression
                  | expression DIFFERENT expression
                  | expression LESS expression
                  | expression GREATER expression
                  | expression LEQ expression
                  | expression GEQ expression"""
    p[0] = (p[2], p[1], p[3])

def p_expression_logic(p):
    """expression : expression AND expression
                  | expression OR expression"""
    p[0] = (p[2].upper(), p[1], p[3])

def p_expression_not(p):
    """expression : NOT expression"""
    p[0] = ("NOT", p[2])

def p_expression_paren(p):
    """expression : LPAR expression RPAR"""
    p[0] = p[2]

def p_expression_atomic(p):
    """expression : length
                  | identifier
                  | INTEGER
                  | REAL
                  | CHAR
                  | STRING
                  | BOOLEAN"""
    p[0] = p[1]

def p_if_stmt(p):
    """if_stmt : IF expression THEN statement
               | IF expression THEN statement ELSE statement"""
    if len(p) == 5:
        p[0] = ("IF", p[2], p[4])
    else:
        p[0] = ("IF", p[2], p[4], "ELSE", p[6])

def p_for_loop(p):
    """for_loop : FOR identifier ASSIGN expression TO expression DO statement
                | FOR identifier ASSIGN expression DOWNTO expression DO statement"""
    direction = "FOR" if p[5].lower() == "to" else "FOR_D"
    p[0] = (direction, p[2], p[4], p[6], p[8])

def p_while_loop(p):
    """while_loop : WHILE expression DO statement"""
    p[0] = ("WHILE", p[2], p[4])

def p_writeln(p):
    """writeln : WRITELN LPAR phrase RPAR
               | WRITELN """
    if len(p) == 2:
       p[0] = ("WRITELN", "") 
    else:
       p[0] = ("WRITELN", p[3])

def p_write(p):
    """write : WRITE LPAR phrase RPAR"""
    p[0] = ("WRITE", p[3])

def p_phrase(p):
    """phrase : phrase_list"""
    p[0] = p[1]

def p_phrase_list(p):
    """phrase_list : phrase_list COMMA phrase_item
                   | phrase_item"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_phrase_item_string(p):
    """phrase_item : STRING
                   | CHAR """
    p[0] = ("STRING", p[1])

def p_phrase_item_var(p):
    """phrase_item : identifier"""
    p[0] = ("VAR", p[1])

def p_phrase_item_int(p):
    """phrase_item : INTEGER"""
    p[0] = ("integer", p[1])

def p_phrase_item_real(p):
    """phrase_item : REAL"""
    p[0] = ("real", p[1])

def p_read(p):
    """read : READ LPAR identifier RPAR"""
    p[0] = ("READ", p[3])

def p_readln(p):
    """readln : READLN LPAR identifier RPAR
              | READLN"""
    if len(p) == 2:
        p[0] = ("READLN", None)
    else:
        p[0] = ("READLN", p[3])

def p_length(p):
    """length : LENGTH LPAR identifier RPAR"""
    p[0] = ("LENGTH", p[3])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (type {p.type}) on line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc(debug=True, write_tables=True)

r = parser.parse(ex6)
print("Árvore:")
pprint.pprint(r, width=80, sort_dicts=False)