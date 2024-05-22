from parser import parser
from lexer import lexer
from ast_printer import print_ast


def test_parser_multiline_function():
    data = """
    FUNCAO soma2(c) :
        c = c + 1 ;
        c + 1 ;
    FIM;
    """

    result = parser.parse(data, lexer=lexer)
    print("AST gerada:")
    if result:
        print_ast(result)
    else:
        print("Erro na geração da AST")


test_parser_multiline_function()
