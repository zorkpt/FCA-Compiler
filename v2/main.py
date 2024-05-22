import ply.lex as lex
import ply.yacc as yacc
import argparse

# Definição das classes da AST com métodos de impressão
class ASTNode:
    def __init__(self, node_type):
        self.node_type = node_type

    def __repr__(self):
        return f"{self.node_type}()"

class ProgramNode(ASTNode):
    def __init__(self, statements):
        super().__init__('ProgramNode')
        self.statements = statements

    def __repr__(self):
        return f"{self.node_type}({self.statements})"

class StatementNode(ASTNode):
    def __init__(self, statement_type):
        super().__init__('StatementNode')
        self.statement_type = statement_type

    def __repr__(self):
        return f"{self.statement_type}()"

class WriteNode(StatementNode):
    def __init__(self, expression):
        super().__init__('WriteNode')
        self.expression = expression

    def __repr__(self):
        return f"{self.statement_type}({self.expression})"

class AssignNode(StatementNode):
    def __init__(self, identifier, expression):
        super().__init__('AssignNode')
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"{self.statement_type}({self.identifier}, {self.expression})"

class ExpressionNode(ASTNode):
    def __init__(self, expression_type):
        super().__init__('ExpressionNode')
        self.expression_type = expression_type

    def __repr__(self):
        return f"{self.expression_type}()"

class BinOpNode(ExpressionNode):
    def __init__(self, operator, left, right):
        super().__init__('BinOpNode')
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.expression_type}({self.operator}, {self.left}, {self.right})"

class NumberNode(ExpressionNode):
    def __init__(self, value):
        super().__init__('NumberNode')
        self.value = value

    def __repr__(self):
        return f"{self.expression_type}({self.value})"

class IdentifierNode(ExpressionNode):
    def __init__(self, name):
        super().__init__('IdentifierNode')
        self.name = name

    def __repr__(self):
        return f"{self.expression_type}({self.name})"

class StringNode(ExpressionNode):
    def __init__(self, value):
        super().__init__('StringNode')
        self.value = value

    def __repr__(self):
        return f"{self.expression_type}({self.value})"

class InterpolatedStringNode(ExpressionNode):
    def __init__(self, parts):
        super().__init__('InterpolatedStringNode')
        self.parts = parts

    def __repr__(self):
        return f"{self.expression_type}({self.parts})"

class InputNode(ExpressionNode):
    def __init__(self):
        super().__init__('InputNode')

    def __repr__(self):
        return f"{self.expression_type}()"

class RandomNode(ExpressionNode):
    def __init__(self, upper_limit):
        super().__init__('RandomNode')
        self.upper_limit = upper_limit

    def __repr__(self):
        return f"{self.expression_type}({self.upper_limit})"

class FunctionNode(ASTNode):
    def __init__(self, name, parameters, body):
        super().__init__('FunctionNode')
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"{self.node_type}({self.name}, {self.parameters}, {self.body})"

class FunctionCallNode(ExpressionNode):
    def __init__(self, name, arguments):
        super().__init__('FunctionCallNode')
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"{self.expression_type}({self.name}, {self.arguments})"


# Definição do lexer
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

# Definição do parser
precedence = (
    ('left', 'OPERADOR_CONCAT'),
    ('left', 'OPERADOR_ARITMETICO'),
    ('left', 'OPERADOR_LOGICO'),
)

def p_program(p):
    '''program : statements'''
    p[0] = ProgramNode(p[1])

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_function_definition(p):
    '''function_definition : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameter_list PARENTESES_DIR DOIS_PONTOS statements FIM'''
    p[0] = FunctionNode(p[2], p[4], p[7])

def p_statement(p):
    '''statement : function_definition
                 | ESCREVER PARENTESES_ESQ expression PARENTESES_DIR PONTO_E_VIRGULA
                 | IDENTIFICADOR ATRIBUICAO expression PONTO_E_VIRGULA'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == 'ESCREVER':
        p[0] = WriteNode(p[3])
    else:
        p[0] = AssignNode(p[1], p[3])

def p_function_call(p):
    '''expression : IDENTIFICADOR PARENTESES_ESQ argument_list PARENTESES_DIR'''
    p[0] = FunctionCallNode(p[1], p[3])

def p_parameter_list(p):
    '''parameter_list : parameter_list VIRGULA IDENTIFICADOR
                       | IDENTIFICADOR
                       | empty'''
    # Lógica para construir a lista de parâmetros

def p_argument_list(p):
    '''argument_list : argument_list VIRGULA expression
                      | expression
                      | empty'''
    # Lógica para construir a lista de argumentos

def p_statement_escrever(p):
    '''statement : ESCREVER PARENTESES_ESQ expression PARENTESES_DIR PONTO_E_VIRGULA'''
    p[0] = WriteNode(p[3])

def p_statement_atribuicao(p):
    '''statement : IDENTIFICADOR ATRIBUICAO expression PONTO_E_VIRGULA'''
    p[0] = AssignNode(p[1], p[3])

def p_expression_binop(p):
    '''expression : expression OPERADOR_ARITMETICO expression'''
    p[0] = BinOpNode(p[2], p[1], p[3])

def p_expression_concat(p):
    '''expression : expression OPERADOR_CONCAT expression'''
    p[0] = BinOpNode(p[2], p[1], p[3])

def p_expression_group(p):
    '''expression : PARENTESES_ESQ expression PARENTESES_DIR'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMERO'''
    p[0] = NumberNode(p[1])

def p_expression_identificador(p):
    '''expression : IDENTIFICADOR'''
    p[0] = IdentifierNode(p[1])

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = StringNode(p[1])

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

def p_expression_input(p):
    '''expression : ENTRADA PARENTESES_ESQ PARENTESES_DIR'''
    p[0] = InputNode()

def p_expression_random(p):
    '''expression : ALEATORIO PARENTESES_ESQ expression PARENTESES_DIR'''
    p[0] = RandomNode(p[3])

def p_error(p):
    print(f"Erro de sintaxe: {p}")

parser = yacc.yacc()

# Classe Intérprete
class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def interpret(self, node):
        if isinstance(node, ProgramNode):
            for statement in node.statements:
                self.interpret(statement)
        elif isinstance(node, FunctionNode):
            self.store_function(node)
        elif isinstance(node, WriteNode):
            value = self.evaluate_expression(node.expression)
            print(value)
        elif isinstance(node, AssignNode):
            value = self.evaluate_expression(node.expression)
            self.variables[node.identifier] = value
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def store_function(self, node):
        self.functions[node.name] = (node.parameters, node.body)

    def evaluate_expression(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            return self.variables.get(node.name, 0)
        elif isinstance(node, BinOpNode):
            left_value = self.evaluate_expression(node.left)
            right_value = self.evaluate_expression(node.right)
            if node.operator == '+':
                return left_value + right_value
            elif node.operator == '-':
                return left_value - right_value
            elif node.operator == '*':
                return left_value * right_value
            elif node.operator == '/':
                return left_value // right_value  # Usar divisão inteira
            elif node.operator == '<>':
                return str(left_value) + str(right_value)  # Concatenação de strings
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, InterpolatedStringNode):
            result = ''
            for part in node.parts:
                if isinstance(part, StringNode):
                    result += part.value
                elif isinstance(part, IdentifierNode):
                    result += str(self.variables.get(part.name, ''))
            return result
        elif isinstance(node, InputNode):
            return int(input("Entrada: "))
        elif isinstance(node, RandomNode):
            import random
            return random.randint(0, self.evaluate_expression(node.upper_limit))
        elif isinstance(node, FunctionCallNode):
            function_def = self.functions.get(node.name)
            if function_def is None:
                raise ValueError(f"Função não definida: {node.name}")
            params, body = function_def
            local_vars = self.variables.copy()
            for param, arg in zip(params, node.arguments):
                local_vars[param] = self.evaluate_expression(arg)
            return self.execute_function_body(body, local_vars)
        else:
            raise ValueError(f"Unknown expression type: {type(node)}")

    def execute_function_body(self, body, local_vars):
        if isinstance(body, list):  # Função multiline
            result = None
            for statement in body:
                if isinstance(statement, AssignNode):
                    value = self.evaluate_expression(statement.expression, local_vars)
                    local_vars[statement.identifier] = value
                result = value  # Atualiza o resultado com o último valor calculado
            return result
        else:  # Função inline
            return self.evaluate_expression(body, local_vars)

# Classe Gerador de Código C
class CodeGenerator:
    def __init__(self):
        self.code = []

    def generate(self, node):
        if isinstance(node, ProgramNode):
            self.code.append("#include <stdio.h>")
            self.code.append("#include <stdlib.h>")
            self.code.append("int main() {")
            for statement in node.statements:
                self.generate(statement)
            self.code.append("return 0;")
            self.code.append("}")
        elif isinstance(node, WriteNode):
            format_str, args = self.generate_printf_args(node.expression)
            self.code.append(f'printf("{format_str}\\n"{", " + args if args else ""});')
        elif isinstance(node, AssignNode):
            value = self.generate_expression(node.expression)
            if isinstance(node.expression, StringNode):
                self.code.append(f'char {node.identifier}[] = "{value}";')
            elif isinstance(node.expression, InputNode):
                self.code.append(f'int {node.identifier};')
                self.code.append(f'scanf("%d", &{node.identifier});')
            elif isinstance(node.expression, RandomNode):
                self.code.append(f'int {node.identifier} = rand() % ({value} + 1);')
            else:
                self.code.append(f'int {node.identifier} = {value};')
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def generate_expression(self, node):
        if isinstance(node, NumberNode):
            return str(node.value)
        elif isinstance(node, IdentifierNode):
            return node.name
        elif isinstance(node, BinOpNode):
            left_value = self.generate_expression(node.left)
            right_value = self.generate_expression(node.right)
            if node.operator == '<>':
                return f'{left_value} {right_value}'  # Concatenação de strings
            else:
                return f"({left_value} {node.operator} {right_value})"
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, InterpolatedStringNode):
            format_str = ''
            args = []
            for part in node.parts:
                if isinstance(part, StringNode):
                    format_str += part.value
                elif isinstance(part, IdentifierNode):
                    format_str += '%s'
                    args.append(part.name)
            return format_str, ', '.join(args)
        elif isinstance(node, InputNode):
            return "scanf(\"%d\", &input)"  # Note que a implementação completa de entrada requer mais
        elif isinstance(node, RandomNode):
            return self.generate_expression(node.upper_limit)
        else:
            raise ValueError(f"Unknown expression type: {type(node)}")

    def generate_printf_args(self, node):
        if isinstance(node, BinOpNode) and node.operator == '<>':
            left_str, left_args = self.generate_printf_args(node.left)
            right_str, right_args = self.generate_printf_args(node.right)
            format_str = f"{left_str}{right_str}"
            args = f"{left_args}, {right_args}".strip(", ")
            return format_str, args
        elif isinstance(node, StringNode):
            return node.value, ""
        elif isinstance(node, IdentifierNode):
            return "%s", node.name
        elif isinstance(node, NumberNode):
            return "%d", str(node.value)
        elif isinstance(node, InterpolatedStringNode):
            return self.generate_expression(node)
        else:
            # Fallback to a general expression
            expr = self.generate_expression(node)
            return "%s", expr

    def get_code(self):
        return "\n".join(self.code)

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
    result = parser.parse(data, lexer=lexer)
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
