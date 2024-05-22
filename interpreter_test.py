
from ast_printer import print_ast

from parser import parser
from lexer import lexer
from interpreter import Interpreter


def test_interpreter():
    data = """
    FUNCAO soma(a,b): a+b ;
    FUNCAO soma2(c) :
        c = c+1 ;
        c+1 ;
    FIM
    seis = soma(4,2);
    oito = soma2(seis);
    """

    result = parser.parse(data, lexer=lexer)
    print("AST gerada:")
    print_ast(result)

    interpreter = Interpreter()
    interpreter.interpret(result)

    # Verifique se as funções foram armazenadas corretamente
    assert "soma" in interpreter.functions
    assert "soma2" in interpreter.functions
    print(f"Funções armazenadas: {interpreter.functions}")

    # Verifique se as variáveis foram calculadas corretamente
    assert interpreter.variables["seis"] == 6
    assert interpreter.variables["oito"] == 8
    print(f"Variáveis armazenadas: {interpreter.variables}")


test_interpreter()
