import ply.lex as lex

tokens = (
    'IDENTIFICADOR',
    'NUMERO',
    'STRING',
    'INTERPOLATED_STRING',
    'ATRIBUICAO',
    'ESCREVER',
    'ENTRADA',
    'ALEATORIO',
    'FUNCAO',
    'FIM',
    'OPERADOR_ARITMETICO',
    'PONTO_E_VIRGULA',
    'VIRGULA',
    'DOIS_PONTOS',
    'PARENTESES_ESQ',
    'PARENTESES_DIR',
    'COLCHETES_ESQ',
    'COLCHETES_DIR',
    'OPERADOR_CONCAT',
    'OPERADOR_LOGICO',
)

t_ATRIBUICAO = r'='
t_ESCREVER = r'ESCREVER'
t_ENTRADA = r'ENTRADA'
t_ALEATORIO = r'ALEATORIO'
t_FUNCAO = r'FUNCAO'
t_FIM = r'FIM'
t_OPERADOR_ARITMETICO = r'\+|-|\*|/'
t_PONTO_E_VIRGULA = r';'
t_VIRGULA = r','
t_DOIS_PONTOS = r':'
t_PARENTESES_ESQ = r'\('
t_PARENTESES_DIR = r'\)'
t_COLCHETES_ESQ = r'\['
t_COLCHETES_DIR = r'\]'
t_OPERADOR_CONCAT = r'<>'
t_OPERADOR_LOGICO = r'/\\|\\/|NEG'

t_ignore = ' \t'

def t_INTERPOLATED_STRING(t):
    r'".*?\#\{.*?\}.*?"'
    t.value = t.value[1:-1]
    return t

def t_STRING(t):
    r'".*?"'
    t.value = t.value[1:-1]
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*[!?]?'
    if t.value.upper() in tokens:
        t.type = t.value.upper()
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMENTARIO(t):
    r'\-\-.*|{-.+?-}'
    pass  # Ignorar comentários

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
