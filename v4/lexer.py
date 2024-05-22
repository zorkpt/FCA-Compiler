import ply.lex as lex

# Definição de Tokens
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
    'MAP',
    'FOLD'
)

# Definição dos Tokens Simples
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


# Palavras reservadas
reserved = {
    'map': 'MAP',
    'fold': 'FOLD'
}


# Expressão regular que reconhece strings interpoladas.
# As strings interpoladas são delimitadas por aspas duplas e contêm expressões
# ou variáveis entre `#{}` que devem ser avaliadas e substituídas pelo seu valor.
# Expressão regular:
# ".*?\#\{.*?\}.*?"
# - "      : Inicia a string com aspas
# - .*?    : Combina qualquer sequência de caracteres
# - \#\{   : Literalmente combina a sequência "#{"
# - .*?    : Combina qualquer sequência de caracteres dentro de "#{...}"
# - \}     : Combina com "}"
# - .*?    : Combina qualquer sequência de caracteres
# - "      : Fecha a string com uma aspa dupla
def t_INTERPOLATED_STRING(t):
    r'".*?\#\{.*?\}.*?"'
    t.value = t.value[1:-1]  # Remove as aspas da string reconhecida
    return t


# Expressão regular que reconhece strings simples.
# Expressão regular:
# ".*?"
# - "      : Inicia a string aspas
# - .*?    : Combina qualquer sequência de caracteres
# - "      : Fecha a string com uma aspas
def t_STRING(t):
    r'".*?"'
    t.value = t.value[1:-1]  # Remove as aspas da string reconhecida
    return t


# Expressão regular que reconhece identificadores, variaveis, funções , etc.
# Identificadores começam com uma letra ou underscore, seguidos por qualquer combinação
# de letras, dígitos e underscores. Podem terminar com um ponto de interrogação ou um sinal
# de exclamação.
# Expressão regular:
# [a-zA-Z_]       : Inicia com uma letra (maiúscula ou minúscula) ou um underscore
# [a-zA-Z0-9_]*   : Seguido por zero ou mais letras, dígitos ou underscores
# [!?]?           : Opcionalmente termina com um ponto de interrogação ou um sinal de exclamação
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*[!?]?'
    if t.value.upper() in tokens:
        t.type = t.value.upper()  # Ajusta o tipo do token para a palavra reservada
    return t


# Expressão regular que reconhece números inteiros.
# Expressão regular:
# \d+ : Combina uma ou mais ocorrências de dígitos
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)  # Converte o valor do token para um inteiro
    return t


# Expressão regular que reconhece novas linhas.
# Expressão regular:
# \n+ : Combina uma ou mais ocorrências do caractere de nova linha (\n)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')  # Conta e atualiza o número de linhas


# Expressão regular que reconhece comentários.
# Esta função é usada para ignorar comentários. Existem dois tipos:
# - Comentários de uma linha iniciados por `--`
# - Comentários de múltiplas linhas delimitados por `{` e `}`
# Exemplo de comentário de uma linha: -- isto é um comentário
# Exemplo de comentário de múltiplas linhas: {- isto é um comentário -}
# Expressão regular:
# \-\-.*      : Combina duas hifens seguidas de qualquer sequência de caracteres (comentário de uma linha)
# |           : OU
# {-.+?-}     : Combina a sequência `{-` qualquer caracter `-}`
def t_COMENTARIO(t):
    r'\-\-.*|{-.+?-}'
    pass  # Ignora comentários (não faz nada)


# Função de tratamento de erros para caracteres ilegais.
# Basicamente tudo que não é apanhado em cima, cai aqui.
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")  # Mostra uma mensagem de erro
    t.lexer.skip(1)  # Ignora o caractere ilegal e avança para o próximo caractere


# Inicializa o lexer
lexer = lex.lex()
