from ast_nodes import *
import ply.yacc as yacc
from lexer import tokens

# Precedência dos operadores
precedence = (
    ('left', 'OPERADOR_CONCAT'),
    ('left', 'OPERADOR_ARITMETICO'),
    ('left', 'OPERADOR_LOGICO'),
)

"""
Regra de produção inicial para o programa.
"""
def p_program(p):
    '''program : statement_list'''
    p[0] = ProgramNode(p[1])  # Cria um nó de AST para o programa contendo a lista de instruções


"""
Regra de produção para uma lista de instruções.

Uma lista de instruções pode ser:
- Uma única instrução
- Uma lista de instruções seguida por uma instrução adicional
"""
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:  # Se a lista contém apenas uma instrução, cria uma lista com essa instrução
        p[0] = [p[1]]
    else:  # Se a lista contém múltiplas instruções, concatena a nova instrução à lista existente
        p[0] = p[1] + [p[2]]


"""
Regra de produção para uma declaração de função inline.

Uma função inline é definida em uma única linha e possui a estrutura:
FUNCAO IDENTIFICADOR (parameters) , : expression ;
"""
def p_statement_function_inline(p):
    '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR VIRGULA DOIS_PONTOS expression PONTO_E_VIRGULA'''
    if all(isinstance(param, NumberNode) for param in p[4]):  # Verifica se todos os parâmetros são números
        p[0] = FunctionNode(p[2], [], [ReturnNode(p[8])])  # Cria um nó de função com uma lista vazia de parâmetros e a expressão como corpo
    else:
        p[0] = FunctionNode(p[2], p[4], [ReturnNode(p[8])])  # Cria um nó de função com os parâmetros fornecidos e a expressão como corpo


"""
Regra de produção para uma declaração de função por ramos.

Uma função por ramos é definida em uma única linha e possui a estrutura:
FUNCAO IDENTIFICADOR (NUMERO) , : expression ;
"""
def p_statement_function_branch(p):
    '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ NUMERO PARENTESES_DIR VIRGULA DOIS_PONTOS expression PONTO_E_VIRGULA'''
    function_name = p[2]
    condition = NumberNode(p[4])
    body = [ReturnNode(p[8])]
    p[0] = BranchNode(function_name, condition, body)


"""
Regra de produção para uma ramificação.

Uma ramificação possui a estrutura:
NUMERO : statement_list
"""
def p_branch(p):
    '''branch : NUMERO DOIS_PONTOS statement_list'''
    function_name = p[-4]  # Assume que o nome da função foi passado anteriormente no contexto
    p[0] = BranchNode(function_name, NumberNode(p[1]), p[3])


"""
Regra de produção para uma função de múltiplas linhas.

Uma função de múltiplas linhas possui a estrutura:
FUNCAO IDENTIFICADOR (parameters) : statement_list FIM
"""
def p_statement_function_multiline(p):
    '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR DOIS_PONTOS statement_list FIM'''
    p[0] = FunctionNode(p[2], p[4], p[7])


"""
Regra de produção para uma lista opcional de instruções.

Uma lista opcional de instruções pode ser:
- Uma lista de instruções
- Vazia
"""
def p_optional_statement_list(p):
    '''optional_statement_list : statement_list
                               | empty'''
    p[0] = p[1]


"""
Regra de produção para um conteúdo vazio.
"""
def p_empty(p):
    '''empty :'''
    p[0] = []


"""
Regra de produção para múltiplos parâmetros.

Múltiplos parâmetros possuem a estrutura:
parameters , IDENTIFICADOR
"""
def p_parameters_multiple(p):
    '''parameters : parameters VIRGULA IDENTIFICADOR'''
    p[0] = p[1] + [p[3]]


"""
Regra de produção para um único parâmetro.

Um único parâmetro é simplesmente um IDENTIFICADOR.
"""
def p_parameters_single(p):
    '''parameters : IDENTIFICADOR'''
    p[0] = [p[1]]


"""
Regra de produção para parâmetros vazios.
"""
def p_parameters_empty(p):
    '''parameters : '''
    p[0] = []


"""
Regra de produção para uma chamada de função.

Uma chamada de função possui a estrutura:
IDENTIFICADOR (arguments)
"""
def p_expression_function_call(p):
    '''expression : IDENTIFICADOR PARENTESES_ESQ arguments PARENTESES_DIR'''
    p[0] = FunctionCallNode(p[1], p[3])


"""
Regra de produção para múltiplos argumentos.

Múltiplos argumentos possuem a estrutura:
arguments , expression
"""
def p_arguments_multiple(p):
    '''arguments : arguments VIRGULA expression'''
    p[0] = p[1] + [p[3]]


"""
Regra de produção para um único argumento.

Um único argumento é simplesmente uma expression.
"""
def p_arguments_single(p):
    '''arguments : expression'''
    p[0] = [p[1]]


"""
Regra de produção para argumentos vazios.
"""
def p_arguments_empty(p):
    '''arguments : '''
    p[0] = []


"""
Regra de produção para uma expressão como uma instrução.

Uma expressão como uma instrução possui a estrutura:
expression ;
"""
def p_statement_expression(p):
    '''statement : expression PONTO_E_VIRGULA'''
    p[0] = p[1]


"""
Regra de produção para uma única instrução.

Uma única instrução é simplesmente uma statement.
"""
def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]


"""
Regra de produção para a instrução ESCREVER.

A instrução ESCREVER possui a estrutura:
ESCREVER (expression) ;
"""
def p_statement_escrever(p):
    '''statement : ESCREVER PARENTESES_ESQ expression PARENTESES_DIR PONTO_E_VIRGULA'''
    p[0] = WriteNode(p[3])


"""
Regra de produção para uma instrução de atribuição.

A instrução de atribuição possui a estrutura:
IDENTIFICADOR = expression ;
"""
def p_statement_atribuicao(p):
    '''statement : IDENTIFICADOR ATRIBUICAO expression PONTO_E_VIRGULA'''
    if isinstance(p[3], FunctionCallNode):
        p[0] = AssignNode(p[1], p[3])
    else:
        p[0] = AssignNode(p[1], p[3])


"""
Regra de produção para uma expressão binária.

Uma expressão binária possui a estrutura:
expression OPERADOR_ARITMETICO expression
"""
def p_expression_binop(p):
    '''expression : expression OPERADOR_ARITMETICO expression'''
    p[0] = BinOpNode(p[2], p[1], p[3])


"""
Regra de produção para uma expressão de concatenação.

Uma expressão de concatenação possui a estrutura:
expression OPERADOR_CONCAT expression
"""
def p_expression_concat(p):
    '''expression : expression OPERADOR_CONCAT expression'''
    p[0] = BinOpNode(p[2], p[1], p[3])


"""
Regra de produção para uma expressão agrupada.

Uma expressão agrupada possui a estrutura:
(expression)
"""
def p_expression_group(p):
    '''expression : PARENTESES_ESQ expression PARENTESES_DIR'''
    p[0] = p[2]


"""
Regra de produção para um número.

Um número é simplesmente um NUMERO.
"""
def p_expression_number(p):
    '''expression : NUMERO'''
    p[0] = NumberNode(p[1])


"""
Regra de produção para um identificador.

Um identificador é simplesmente um IDENTIFICADOR.
"""
def p_expression_identificador(p):
    '''expression : IDENTIFICADOR'''
    p[0] = IdentifierNode(p[1])


"""
Regra de produção para uma string.

Uma string é simplesmente um STRING.
"""
def p_expression_string(p):
    '''expression : STRING'''
    p[0] = StringNode(p[1])


"""
Regra de produção para uma string interpolada.

Uma string interpolada possui a estrutura:
INTERPOLATED_STRING
"""
def p_expression_interpolated_string(p):
    '''expression : INTERPOLATED_STRING'''
    parts = []
    current_str = ''
    i = 0
    while i < len(p[1]):
        if p[1][i] == '#' and p[1][i + 1] == '{':
            if current_str:
                parts.append(StringNode(current_str))
                current_str = ''
            i += 2
            var_name = ''
            while p[1][i] != '}':
                var_name += p[1][i]
                i += 1
            parts.append(IdentifierNode(var_name))
        else:
            current_str += p[1][i]
        i += 1
    if current_str:
        parts.append(StringNode(current_str))
    p[0] = InterpolatedStringNode(parts)


"""
Regra de produção para a expressão de entrada.
A expressão de entrada possui a estrutura:
ENTRADA()
"""
def p_expression_input(p):
    '''expression : ENTRADA PARENTESES_ESQ PARENTESES_DIR'''
    p[0] = InputNode()


"""
Regra de produção para a expressão de número aleatório.

A expressão de número aleatório possui a estrutura:
ALEATORIO(expression)
"""
def p_expression_random(p):
    '''expression : ALEATORIO PARENTESES_ESQ expression PARENTESES_DIR'''
    p[0] = RandomNode(p[3])


"""
Função de tratamento de erros de sintaxe.
"""
def p_error(p):
    print(f"Erro de sintaxe: {p}")


"""
Regra de produção para uma lista de expressões.

Uma lista de expressões possui a estrutura:
[ list_elements ]
"""
def p_expression_list(p):
    '''expression : COLCHETES_ESQ list_elements COLCHETES_DIR
                  | COLCHETES_ESQ COLCHETES_DIR'''
    if len(p) == 4:
        p[0] = ListNode(p[2])
    else:
        p[0] = ListNode([])


"""
Regra de produção para elementos de uma lista.

Os elementos de uma lista podem ser:
- Uma única expressão
- Uma lista de expressões seguida por uma expressão adicional
"""
def p_list_elements(p):
    '''list_elements : list_elements VIRGULA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


"""
Regra de produção para a expressão MAP.

A expressão MAP possui a estrutura:
MAP(IDENTIFICADOR, expression)
"""
def p_expression_map(p):
    '''expression : MAP PARENTESES_ESQ IDENTIFICADOR VIRGULA expression PARENTESES_DIR'''
    p[0] = MapNode(p[3], p[5])


"""
Regra de produção para a expressão FOLD.

A expressão FOLD possui a estrutura:
FOLD(IDENTIFICADOR, expression, expression)
"""
def p_expression_fold(p):
    '''expression : FOLD PARENTESES_ESQ IDENTIFICADOR VIRGULA expression VIRGULA expression PARENTESES_DIR'''
    p[0] = FoldNode(p[3], p[5], p[7])


"""
Regra de produção para definição de função com padrão de lista.

A definição de função com padrão de lista possui a estrutura:
FUNCAO IDENTIFICADOR (list_pattern) , : expression ;
"""
def p_function_definition_list_pattern(p):
    '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ list_pattern PARENTESES_DIR VIRGULA DOIS_PONTOS expression PONTO_E_VIRGULA'''
    p[0] = FunctionNode(p[2], [p[4]], [ReturnNode(p[8])])


"""
Regra de produção para um padrão de lista vazio.

Um padrão de lista vazio possui a estrutura:
[]
"""
def p_list_pattern_empty(p):
    '''list_pattern : COLCHETES_ESQ COLCHETES_DIR'''
    p[0] = ListPatternNode(None, None)


"""
Regra de produção para um padrão de lista com cabeça e cauda.

Um padrão de lista com cabeça e cauda possui a estrutura:
IDENTIFICADOR : IDENTIFICADOR
"""
def p_list_pattern_head_tail(p):
    '''list_pattern : IDENTIFICADOR DOIS_PONTOS IDENTIFICADOR'''
    p[0] = ListPatternNode(p[1], p[3])


# Inicializa o parser
parser = yacc.yacc()
