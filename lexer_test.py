from lexer import lexer


def test_lexer():
    data = """
    FUNCAO soma(a,b): a+b ;
    FUNCAO soma2(c) :
        c = c+1 ;
        c+1 ;
    FIM
    seis = soma(4,2);
    oito = soma2(seis);
    """
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value))

    expected_tokens = [
        ('FUNCAO', 'FUNCAO'),
        ('IDENTIFICADOR', 'soma'),
        ('PARENTESES_ESQ', '('),
        ('IDENTIFICADOR', 'a'),
        ('VIRGULA', ','),
        ('IDENTIFICADOR', 'b'),
        ('PARENTESES_DIR', ')'),
        ('DOIS_PONTOS', ':'),
        ('IDENTIFICADOR', 'a'),
        ('OPERADOR_ARITMETICO', '+'),
        ('IDENTIFICADOR', 'b'),
        ('PONTO_E_VIRGULA', ';'),
        ('FUNCAO', 'FUNCAO'),
        ('IDENTIFICADOR', 'soma2'),
        ('PARENTESES_ESQ', '('),
        ('IDENTIFICADOR', 'c'),
        ('PARENTESES_DIR', ')'),
        ('DOIS_PONTOS', ':'),
        ('IDENTIFICADOR', 'c'),
        ('ATRIBUICAO', '='),
        ('IDENTIFICADOR', 'c'),
        ('OPERADOR_ARITMETICO', '+'),
        ('NUMERO', 1),
        ('PONTO_E_VIRGULA', ';'),
        ('IDENTIFICADOR', 'c'),
        ('OPERADOR_ARITMETICO', '+'),
        ('NUMERO', 1),
        ('PONTO_E_VIRGULA', ';'),
        ('FIM', 'FIM'),
        ('IDENTIFICADOR', 'seis'),
        ('ATRIBUICAO', '='),
        ('IDENTIFICADOR', 'soma'),
        ('PARENTESES_ESQ', '('),
        ('NUMERO', 4),
        ('VIRGULA', ','),
        ('NUMERO', 2),
        ('PARENTESES_DIR', ')'),
        ('PONTO_E_VIRGULA', ';'),
        ('IDENTIFICADOR', 'oito'),
        ('ATRIBUICAO', '='),
        ('IDENTIFICADOR', 'soma2'),
        ('PARENTESES_ESQ', '('),
        ('IDENTIFICADOR', 'seis'),
        ('PARENTESES_DIR', ')'),
        ('PONTO_E_VIRGULA', ';')
    ]

    assert tokens == expected_tokens, f"Expected {expected_tokens}, but got {tokens}"


test_lexer()
