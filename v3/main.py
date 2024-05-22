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


## NODES DE FUNCOES

class FunctionNode(StatementNode):
    def __init__(self, name, parameters, body, condition=None):
        super().__init__('FunctionNode')
        self.name = name
        self.parameters = parameters
        self.body = body
        self.condition = condition

    def __repr__(self):
        return f"{self.statement_type}({self.name}, {self.parameters}, {self.body}, {self.condition})"


class FunctionCallNode(ExpressionNode):
    def __init__(self, name, arguments):
        super().__init__('FunctionCallNode')
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"{self.expression_type}({self.name}, {self.arguments})"


class ReturnNode(StatementNode):
    def __init__(self, expression):
        super().__init__('ReturnNode')
        self.expression = expression

    def __repr__(self):
        return f"{self.statement_type}({self.expression})"


## FIM NODES DE FUNCOES

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
    '''program : statement_list'''
    p[0] = ProgramNode(p[1])


# def p_statements_multiple(p):
#     '''statements : statements statement'''
#     p[0] = p[1] + [p[2]]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


## REGRAS DE PRODUCAO PARA FUNCOES
# def p_statement_function_multiline(p):
#     '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR DOIS_PONTOS optional_statement_list FIM'''
#     p[0] = FunctionNode(p[2], p[4], p[7])

# def p_statement_function_multiline(p):
#     '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR DOIS_PONTOS statement_list FIM'''
#     p[0] = FunctionNode(p[2], p[4], p[7])


# Código do Parser para diferenciar funções de ramificação
def p_statement_function_inline(p):
    '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR VIRGULA DOIS_PONTOS expression PONTO_E_VIRGULA'''
    if all(isinstance(param, NumberNode) for param in p[4]):
        condition = [param.value for param in p[4]]  # Usar os parâmetros como condição
        p[0] = FunctionNode(p[2], [], [ReturnNode(p[8])], condition)
    else:
        p[0] = FunctionNode(p[2], p[4], [ReturnNode(p[8])], None)


def p_statement_function_branch(p):
    '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ NUMBER PARENTESES_DIR VIRGULA DOIS_PONTOS expression PONTO_E_VIRGULA'''
    p[0] = FunctionNode(p[2], [], [ReturnNode(p[8])], [p[4]])


def p_statement_function_multiline(p):
    '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR DOIS_PONTOS statement_list FIM'''
    p[0] = FunctionNode(p[2], p[4], p[7], None)



def p_optional_statement_list(p):
    '''optional_statement_list : statement_list
                               | empty'''
    p[0] = p[1]


def p_empty(p):
    '''empty :'''
    p[0] = []


# def p_statement_function_inline(p):
#     '''statement : FUNCAO IDENTIFICADOR PARENTESES_ESQ parameters PARENTESES_DIR VIRGULA DOIS_PONTOS expression PONTO_E_VIRGULA'''
#     p[0] = FunctionNode(p[2], p[4], [ReturnNode(p[8])], condition=p[4])


def p_parameters_multiple(p):
    '''parameters : parameters VIRGULA IDENTIFICADOR'''
    p[0] = p[1] + [p[3]]


def p_parameters_single(p):
    '''parameters : IDENTIFICADOR'''
    p[0] = [p[1]]


def p_parameters_empty(p):
    '''parameters : '''
    p[0] = []


def p_expression_function_call(p):
    '''expression : IDENTIFICADOR PARENTESES_ESQ arguments PARENTESES_DIR'''
    p[0] = FunctionCallNode(p[1], p[3])


def p_arguments_multiple(p):
    '''arguments : arguments VIRGULA expression'''
    p[0] = p[1] + [p[3]]


def p_arguments_single(p):
    '''arguments : expression'''
    p[0] = [p[1]]


def p_arguments_empty(p):
    '''arguments : '''
    p[0] = []


### FIM REGRAS FUNCOES

# Diretamente retornando a expressão como uma instrução válida se terminar em ;
def p_statement_expression(p):
    '''statement : expression PONTO_E_VIRGULA'''
    p[0] = p[1]


def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]


def p_statement_escrever(p):
    '''statement : ESCREVER PARENTESES_ESQ expression PARENTESES_DIR PONTO_E_VIRGULA'''
    p[0] = WriteNode(p[3])


def p_statement_atribuicao(p):
    '''statement : IDENTIFICADOR ATRIBUICAO expression PONTO_E_VIRGULA'''
    if isinstance(p[3], FunctionCallNode):
        p[0] = AssignNode(p[1], p[3])
    else:
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
        self.symbol_table = {}
        self.functions = {}
        self.call_stack = []  # Adiciona uma pilha de chamadas para rastrear a profundidade da recursão

    def interpret(self, node):
        print(f"Interpretando nó: {node}")
        if isinstance(node, ProgramNode):
            for statement in node.statements:
                self.interpret(statement)
        elif isinstance(node, FunctionNode):
            if node.name not in self.functions:
                self.functions[node.name] = []
            self.functions[node.name].append((node.parameters, node.body, node.condition))
            print(f"Função registrada: {node.name} com parâmetros {node.parameters} e condição {node.condition}")
        elif isinstance(node, AssignNode):
            value = self.evaluate_expression(node.expression)
            self.symbol_table[node.identifier] = value
            print(f"Variável {node.identifier} atribuída com valor: {value}")
        elif isinstance(node, WriteNode):
            value = self.evaluate_expression(node.expression)
            print(f"ESCREVER: {value}")
        elif isinstance(node, NumberNode):
            value = node.value
        else:
            raise ValueError(f"Unknown statement type: {type(node)}")

    def apply_operator(self, operator, left, right):
        print(f"Aplicando operador: {operator} com operandos: {left}, {right}")
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left / right
        elif operator == '<>':
            return str(left) + str(right)
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def evaluate_expression(self, node):
        print(f"Avaliando expressão: {node}")
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, BinOpNode):
            left = self.evaluate_expression(node.left)
            right = self.evaluate_expression(node.right)
            return self.apply_operator(node.operator, left, right)
        elif isinstance(node, IdentifierNode):
            value = self.symbol_table.get(node.name, None)
            print(f"Valor do identificador {node.name}: {value}")
            return value
        elif isinstance(node, FunctionCallNode):
            return self.call_function(node)
        elif isinstance(node, StringNode):
            return node.value
        else:
            raise ValueError(f"Unknown expression type: {type(node)}")

    def call_function(self, node):
        print(f"Chamando função: {node.name} com argumentos: {node.arguments}")
        func_list = self.functions.get(node.name)
        if func_list is None:
            raise ValueError(f"Função não definida: {node.name}")

        self.call_stack.append(node.name)
        if len(self.call_stack) > 50:  # Limite arbitrário para a profundidade da recursão
            raise RecursionError(f"Recursion depth exceeded in function {node.name}")

        for params, body, condition in func_list:
            if condition is not None:
                print(f"Verificando função: {node.name} com condição: {condition}")
                if all(self.evaluate_expression(arg) == cond for arg, cond in zip(node.arguments, condition)):
                    local_env = {param: self.evaluate_expression(arg) for param, arg in zip(params, node.arguments)}
                    result = self.execute_function_body(body, local_env)
                    self.call_stack.pop()
                    return result
            else:
                print(f"Verificando função: {node.name} com parâmetros: {params}")
                if len(params) == len(node.arguments):
                    local_env = {param: self.evaluate_expression(arg) for param, arg in zip(params, node.arguments)}
                    result = self.execute_function_body(body, local_env)
                    self.call_stack.pop()
                    return result

        self.call_stack.pop()
        raise ValueError(
            f"Função {node.name} com {len(node.arguments)} argumentos e condição correspondente não definida")

    def execute_function_body(self, body, env):
        print(f"Executando corpo da função com ambiente: {env}")
        old_env = self.symbol_table.copy()  # Usar cópia para preservar o ambiente global
        self.symbol_table.update(env)
        result = None
        for statement in body:
            print(f"Executando statement: {statement}")
            if isinstance(statement, ReturnNode):
                result = self.evaluate_expression(statement.expression)
                break
            elif isinstance(statement, AssignNode):
                self.interpret(statement)
            else:
                result = self.evaluate_expression(statement)  # Aqui lidamos com BinOpNode e outros nós de expressão
        self.symbol_table = old_env  # Restaurar o ambiente global
        print(f"Resultado da execução do corpo da função: {result}")
        return result

# Classe Gerador de Código C
class CodeGenerator:
    def __init__(self):
        self.code = []
        self.functions = []

    def generate(self, node):
        if isinstance(node, ProgramNode):
            self.code.append("#include <stdio.h>")
            self.code.append("#include <stdlib.h>")
            for statement in node.statements:
                if isinstance(statement, FunctionNode):
                    self.generate(statement)  # Gerar função antes do main
            self.code.append("int main() {")
            for statement in node.statements:
                if not isinstance(statement, FunctionNode):
                    self.generate(statement)  # Gerar outras instruções no main
            self.code.append("return 0;")
            self.code.append("}")
        elif isinstance(node, FunctionNode):
            params = ', '.join(f'int {param}' for param in node.parameters)
            body = ' '.join([self.generate_statement(s) for s in node.body])
            self.functions.append(f"int {node.name}({params}) {{ {body} }}")
        elif isinstance(node, AssignNode):
            value = self.generate_expression(node.expression)
            self.code.append(f'int {node.identifier} = {value};')
        elif isinstance(node, WriteNode):
            format_str, args = self.generate_printf_args(node.expression)
            self.code.append(f'printf("{format_str}\\n"{", " + args if args else ""});')
        elif isinstance(node, FunctionCallNode):  # Handle FunctionCallNode
            function_call = self.generate_expression(node)
            self.code.append(f"{function_call};")
        else:
            raise ValueError(f"Unknown statement type: {type(node)}")

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
            return "scanf(\"%d\", &input)"
        elif isinstance(node, StringNode):
            return f'"{node.value}"'
        elif isinstance(node, FunctionCallNode):
            args = ', '.join(self.generate_expression(arg) for arg in node.arguments)
            return f"{node.name}({args})"
        else:
            raise ValueError(f"Unknown expression type: {type(node)}")

    def generate_statement(self, node):
        if isinstance(node, AssignNode):
            return f"{node.identifier} = {self.generate_expression(node.expression)};"
        elif isinstance(node, ReturnNode):
            return f"return {self.generate_expression(node.expression)};"
        else:
            return self.generate_expression(node)

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
            return "%d", node.name
        elif isinstance(node, NumberNode):
            return "%d", str(node.value)
        else:
            expr = self.generate_expression(node)
            return "%s", expr

    def get_code(self):
        return '\n'.join(self.code[:2] + self.functions + self.code[2:])


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
