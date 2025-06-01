import ply.lex as lex
import re

from test import ex1, ex2, ex3, ex4, ex5, ex6, ex7 

tokens = (
	'IDENTIFIER', # nome de variável / função
	'ASSIGN', # :=
	'SEMICOLON', # ;
	'COLON', # :
	'COMMA', # ,
	'COMMENT', # comentário
	'PROGRAM', 
	'DOT', # .
	'VAR',
	'BEGIN', 
	'END', 
	'IF',
	'THEN', 
	'ELSE',
	'FOR',
	'WHILE',
	'DO',
	'TO',
    'DOWNTO',
	'AND',
	'OR', 
	'NOT',
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVISION', # /
	'DIV', # div
	'MOD',
	'EQUAL', # =
	'DIFFERENT', # <>
	'LESS', # <
	'GREATER', # >
	'LEQ', # <=
	'GEQ', # >=
	'LPAR', # (
	'RPAR', # )
    'LBRACKET', # [
    'RBRACKET', # ]
	'REAL', 
	'INTEGER',
	'STRING',
	'CHAR',
    'BOOLEAN',
	'TREAL',
	'TINTEGER',
	'TSTRING',
	'TCHAR',
    'TBOOLEAN',
    'WRITELN',
    'WRITE',
	'READ',
    'READLN',
    'ARRAY',
    'OF',
    'LENGTH',
    'CONST'
)

t_DOT = r"\."

t_ASSIGN = r":="
t_SEMICOLON = r";"
t_COLON	= r":"
t_COMMA	= r","

t_PLUS	= r"\+"
t_MINUS	= r"\-"
t_TIMES	= r"\*"
t_DIVISION = r"\/"


t_EQUAL = r"\="
t_DIFFERENT = r"\<\>"
t_LESS = r"\<"
t_GREATER = r"\>"
t_LEQ = r"\<\="
t_GEQ = r"\>\="

t_LPAR = r"\("
t_RPAR = r"\)"
t_LBRACKET = r"\[" 
t_RBRACKET = r"\]"

t_REAL = r"(\-)*[0-9]+\.[0-9]+"
t_INTEGER = r"(\-)*[0-9]+"

def t_PROGRAM(t):
    r'program'
    return t

def t_VAR(t):
    r'var'
    return t

def t_BEGIN(t):
    r'begin'
    return t

def t_END(t):
    r'end'
    return t

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FOR(t):
    r'for'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DOWNTO(t):
    r'downto'
    return t

def t_DO(t):
    r'do'
    return t

def t_TO(t):
    r'to'
    return t

def t_AND(t):
    r'and'
    return t

def t_OR(t):
    r'or'
    return t

def t_NOT(t):
    r'not'
    return t

def t_DIV(t):
    r'div'
    return t

def t_MOD(t):
    r'mod'
    return t

def t_TREAL(t):
    r'real'
    return t

def t_TINTEGER(t):
    r'integer'
    return t

def t_TSTRING(t):
    r'string'
    return t

def t_TCHAR(t):
    r'char'
    return t

def t_TBOOLEAN(t):
    r'boolean'
    return t

def t_ARRAY(t):
    r'array'
    return t

def t_OF(t):
    r'of'
    return t

def t_WRITELN(t):
    r'writeln'
    return t

def t_WRITE(t):
    r'write'
    return t

def t_READLN(t):
    r'readln'
    return t

def t_LENGTH(t):
    r'length'
    return t

def t_CONST(t):
    r'const'
    return t


t_IDENTIFIER = r"[a-zA-Z]([a-zA-Z0-9])*"

def t_CHAR(t):
	r"(\'([^\\\'])\')|(\"([^\\\"])\")"
	return t

def t_STRING(t): 
    r"(\"([^\\\"]|(\\.))*\")|(\'([^\\\']|(\\.))*\')"
    escaped = 0 
    str = t.value[1:-1] 
    new_str = "" 
    for i in range(0, len(str)): 
        c = str[i] 
        if escaped: 
            if c == "n": 
                c = "\n" 
            elif c == "t": 
                c = "\t" 
            new_str += c 
            escaped = 0 
        else: 
            if c == "\\": 
                escaped = 1 
            else: 
                new_str += c 
    t.value = new_str 
    return t

def t_BOOLEAN(t):
    r"true|false"
    return t

def t_COMMENT(t):
	r"{[^}]*}"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Carácter inválido '%s'" % t.value[0])
    
lexer = lex.lex(reflags=re.IGNORECASE) 

#lexer.input(ex7)

#with open("output/output.txt", "w", encoding="utf-8") as file:
#for token in lexer:
#    print(f"{token}")
    
lexer.lineno = 1
