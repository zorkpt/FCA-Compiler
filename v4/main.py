import argparse
from lexer import lexer
from parser import parser
from code_generator import CodeGenerator
from interpreter import Interpreter

def main():
    # Configurar o parser de argumentos
    arg_parser = argparse.ArgumentParser(description='Interpretador e Gerador de Código C para a linguagem FCA.')
    arg_parser.add_argument('filename', type=str, help='Nome do arquivo contendo o código a ser interpretado')

    args = arg_parser.parse_args()

    # Ler o conteúdo do arquivo
    with open(args.filename, 'r') as file:
        data = file.read()

    # Imprimir tokens gerados
    lexer.input(data)
    print("Tokens gerados:")
    for token in lexer:
        print(token)

    # Resetar o lexer para o parser
    lexer.input(data)
    result = parser.parse(data)
    print(result)

    # Testar o intérprete com a AST gerada
    print("\nInterpretação do código:")
    if result is not None:
        interpreter = Interpreter()
        interpreter.interpret(result)

    # Testar o gerador de código C com a AST gerada
    print("\nCódigo C gerado:")
    if result is not None:
        code_generator = CodeGenerator()
        code_generator.generate(result)
        print(code_generator.get_code())


if __name__ == "__main__":
    main()
