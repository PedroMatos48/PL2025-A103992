import ply.lex as lex

tokens = (
    "SEL",
    "WHERE",
    "LIMIT", 
    "VAR", 
    "URI", 
    "STRING", 
    "NUMBER", 
    "SHRT",
    "LANG",
    "AC",
    "FC"
)

reserved = {
    '?s': 'SEL',
    '?w': 'WHERE'
}

def t_SEL(t):
    r'select|\?s'
    t.type = reserved.get(t.value, 'SEL')
    return t

def t_WHERE(t):
    r'where|\?w'
    t.type = reserved.get(t.value, 'WHERE')
    return t

t_LIMIT = r'LIMIT'
t_VAR = r'\?[a-zA-Z_][a-zA-Z0-9_]*'
t_URI = r'[a-zA-Z_]+:[a-zA-Z_]+'
t_STRING = r'\".*?\"([a-zA-Z]+)?'
t_NUMBER = r'\d+'
t_SHRT = r'\b[a-z]\b'
t_LANG = r'@[a-zA-Z]+'
t_AC = r"{"
t_FC = r"}"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t \.'

def t_error(t):
    print(f"Símbolo inválido na linha {t.lineno}: {t.value[0]}")
    t.lexer.skip(1)
    pass

lexer = lex.lex()

query = '''select ?nome ?desc where {
    ?s a dbo:MusicalArtist. 
    ?s foaf:name "Chuck Berry"@en . 
    ?w dbo:artist ?s. 
    ?w foaf:name ?nome. 
    ?w dbo:abstract ?desc 
} LIMIT 1000'''

lexer.input(query)
while r := lexer.token():
    print(r)
