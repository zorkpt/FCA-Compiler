import ply.yacc as yacc
from lexer import tokens
from nodes import *

def p_program(p):
    '''program : statements'''
    p[0] = ProgramNode(p[1])
    print(f"ProgramNode criado: {p[0]}")

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
    print(f"Statements: {p[0]}")

def p_statement(p):
    '''statement : atribuicao_statement
                 | funcao_inline
                 | funcao_multiline
                 | expressao_statement
                 | escrever_statement'''
    p[0] = p[1]
    print(f"Statement: {p[0]}")

def p_atribuicao_statement(p):
    '''atribuicao_statement : IDENTIFICADOR ATRIBUICAO expression PONTO_E_VIRGULA'''
    p[0] = AssignNode(p[1], p[3])
    print(f"AssignNode criado: {p[0]}")

def p_funcao_inline(p):
    '''funcao_inline : FUNCAO IDENTIFICADOR PARENTESES_ESQ parametros PARENTESES_DIR VIRGULA DOIS_PONTOS expression PONTO_E_VIRGULA'''
    print(f"Definindo função inline: {p[2]} com parâmetros {p[4]} e corpo {p[8]}")
    p[0] = FunctionDefNode(p[2], p[4], [p[8]])

def p_funcao_multiline(p):
    '''funcao_multiline : FUNCAO IDENTIFICADOR PARENTESES_ESQ parametros PARENTESES_DIR DOIS_PONTOS statements FIM PONTO_E_VIRGULA'''
    print(f"Definindo função multiline: {p[2]} com parâmetros {p[4]} e corpo {p[7]}")
    p[0] = FunctionDefNode(p[2], p[4], p[7])

def p_expressao_statement(p):
    '''expressao_statement : expression PONTO_E_VIRGULA'''
    p[0] = p[1]
    print(f"Expressão statement: {p[0]}")

def p_escrever_statement(p):
    '''escrever_statement : ESCREVER PARENTESES_ESQ expression PARENTESES_DIR PONTO_E_VIRGULA'''
    p[0] = WriteNode(p[3])
    print(f"WriteNode criado: {p[0]}")

def p_parametros(p):
    '''parametros : parametros VIRGULA IDENTIFICADOR
                  | IDENTIFICADOR'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
    print(f"Parâmetros: {p[0]}")

def p_argumentos(p):
    '''argumentos : argumentos VIRGULA expression
                  | expression
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = p[1] + [p[3]]
    print(f"Argumentos: {p[0]}")

def p_expression_binop(p):
    '''expression : expression OPERADOR_ARITMETICO expression
                  | expression OPERADOR_CONCAT expression'''
    p[0] = BinOpNode(p[2], p[1], p[3])
    print(f"Construindo BinOpNode: {p[2]} com expressões {p[1]} e {p[3]}")

def p_expression_group(p):
    '''expression : PARENTESES_ESQ expression PARENTESES_DIR'''
    p[0] = p[2]
    print(f"Expressão em parênteses: {p[0]}")

def p_expression_number(p):
    '''expression : NUMERO'''
    p[0] = NumberNode(p[1])
    print(f"NumberNode: {p[0]}")

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = StringNode(p[1])
    print(f"StringNode: {p[0]}")

def p_expression_identifier(p):
    '''expression : IDENTIFICADOR'''
    p[0] = IdentifierNode(p[1])
    print(f"IdentifierNode: {p[0]}")

def p_expression_funcao(p):
    '''expression : IDENTIFICADOR PARENTESES_ESQ argumentos PARENTESES_DIR'''
    print(f"Construindo FunctionCallNode: {p[1]} com argumentos {p[3]}")
    p[0] = FunctionCallNode(p[1], p[3])

def p_empty(p):
    '''empty :'''
    p[0] = None

def p_error(p):
    if p:
        print(f"Erro de sintaxe: {p}")
    else:
        print("Erro de sintaxe no final do arquivo")

parser = yacc.yacc()
