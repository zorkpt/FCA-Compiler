import argparse
from lexer import lexer
from parser import parser
from code_generator import CodeGenerator
from interpreter import Interpreter

def main():
    # Configurar o parser de argumentos
    arg_parser = argparse.ArgumentParser(description='Interpretador e Gerador de Código C para a linguagem FCA.')
    arg_parser.add_argument('filename', type=str, help='Nome do ficheiro quem contem o código a ser interpretado')

    args = arg_parser.parse_args()

    # Ler o conteúdo do arquivo
    with open(args.filename, 'r') as file:
        data = file.read()

    # Gerar tokens
    lexer.input(data)

    # Guarda a AST gerada
    result = parser.parse(data)

    # Interpretar a AST gerada
    if result is not None:
        interpreter = Interpreter()
        interpreter.interpret(result)

    # Converte para C usando a AST
    if result is not None:
        code_generator = CodeGenerator()
        code_generator.generate(result)
        c_code = code_generator.get_code()

        with open("output.c", "w") as file:
            file.write(c_code)

if __name__ == "__main__":
    main()
