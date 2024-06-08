import random
from ast_nodes import *

class Interpreter:
    def __init__(self):
        # Tabela de símbolos para armazenar variáveis globais
        self.global_env: dict = {}
        # Dicionário de funções definidas
        self.functions: dict = {}

    def interpret(self, node: ASTNode, env: dict = None) -> any:
        """
        Interpreta o nó fornecido na AST.

        :param node: O nó da AST a ser interpretado.
        :param env: O ambiente (contexto) de execução atual.
        :return: O valor retornado, se houver.
        """
        if env is None:
            env = self.global_env

        if isinstance(node, ProgramNode):
            for statement in node.statements:
                self.interpret(statement, env)

        elif isinstance(node, FunctionNode):
            func_name: str = node.name
            param_count: int = len(node.parameters)
            if func_name not in self.functions:
                self.functions[node.name] = []

            # Remover qualquer definição normal anterior que tenha o mesmo número de parâmetros que esta
            new_function_list: list = []
            for entry in self.functions[func_name]:
                entry_type, entry_params, _ = entry
                if not (entry_type == 'normal' and len(entry_params) == param_count):
                    new_function_list.append(entry)

            self.functions[func_name] = new_function_list

            # Adicionar ou substituir a definição normal da função
            self.functions[func_name].append(('normal', node.parameters, node.body))

        elif isinstance(node, BranchNode):
            func_name: str = node.function_name
            if func_name not in self.functions:
                self.functions[func_name] = []
            self.functions[func_name].append(('branch', node.condition, node.body))

        elif isinstance(node, AssignNode):
            value: any = self.evaluate_expression(node.expression, env)
            env[node.identifier] = value

        elif isinstance(node, WriteNode):
            value: any = self.evaluate_expression(node.expression, env)
            # Print para a consola
            print(value)

        elif isinstance(node, ReturnNode):
            return self.evaluate_expression(node.expression, env)

        elif isinstance(node, FunctionCallNode):
            return self.call_function(node, env)

        elif isinstance(node, BinOpNode):
            return self.evaluate_expression(node, env)

        else:
            raise ValueError(f"Tipo desconhecido: {type(node)}")

    def evaluate_expression(self, node: ASTNode, env: dict) -> any:
        """
        Avalia a expressão fornecida.

        :param node: O nó da expressão a ser avaliada.
        :param env: O ambiente (contexto) de execução atual.
        :return: O valor da expressão avaliada.
        """
        if isinstance(node, NumberNode):
            return node.value

        elif isinstance(node, int):
            return node

        elif isinstance(node, BinOpNode):
            left: any = self.evaluate_expression(node.left, env)
            right: any = self.evaluate_expression(node.right, env)
            result: any = self.apply_operator(node.operator, left, right)
            return result

        elif isinstance(node, IdentifierNode):
            value: any = env.get(node.name, None)
            if value is None:
                raise ValueError(f"Variável não encontrada: {node.name}")
            return value

        elif isinstance(node, FunctionCallNode):
            return self.call_function(node, env)

        elif isinstance(node, StringNode):
            return node.value

        elif isinstance(node, WriteNode):
            return self.evaluate_expression(node.expression, env)

        elif isinstance(node, InterpolatedStringNode):
            parts: list = []
            for part in node.parts:
                if isinstance(part, StringNode):
                    parts.append(part.value)
                elif isinstance(part, IdentifierNode):
                    parts.append(str(env.get(part.name, "")))
            return ''.join(parts)

        elif isinstance(node, InputNode):
            user_input: str = input()
            if user_input.isnumeric():
                return int(user_input)
            return user_input

        elif isinstance(node, RandomNode):
            return random.randint(0, self.evaluate_expression(node.upper_limit, env))

        elif isinstance(node, ListNode):
            return [self.evaluate_expression(element, env) for element in node.elements]

        elif isinstance(node, MapNode):
            list_value: list = self.evaluate_expression(node.list_node, env)
            return [self.call_function(FunctionCallNode(node.function, [element]), env) for element in list_value]

        elif isinstance(node, FoldNode):
            result: any = self.evaluate_expression(node.initial_value, env)
            list_value: list = self.evaluate_expression(node.list_node, env)
            for element in list_value:
                result = self.call_function(FunctionCallNode(node.function, [result, element]), env)
            return result

        else:
            raise ValueError(f"Unknown expression type: {type(node)}")

    def call_function(self, node: FunctionCallNode, env: dict) -> any:
        """
        Chama a função com o nome e argumentos fornecidos.

        :param node: O nó da chamada de função.
        :param env: O ambiente (contexto) de execução atual.
        :return: O valor retornado pela função.
        """
        func_list: list = self.functions.get(node.name)
        if func_list is None:
            raise ValueError(f"Função não definida: {node.name}")

        # Verificar ramos (BranchNode) primeiro
        if isinstance(func_list, list) and len(func_list) > 0:
            for func_data in func_list:
                func_type: str = func_data[0]
                if func_type == 'branch':
                    condition: ASTNode = func_data[1]
                    body: list = func_data[2]
                    arg_value: any = self.evaluate_expression(node.arguments[0], env)

                    # Verificar se o padrão de lista condiz com o argumento
                    if isinstance(condition, ListNode):
                        if not condition.elements and isinstance(arg_value, list) and not arg_value:
                            # Caso da lista vazia
                            local_env: dict = env.copy()
                            result: any = self.execute_function_body(body, local_env)
                            return result
                        elif arg_value == [self.evaluate_expression(e, env) for e in condition.elements]:
                            # Caso de listas iguais
                            local_env: dict = env.copy()
                            result: any = self.execute_function_body(body, local_env)
                            return result

                    elif isinstance(condition, NumberNode) and isinstance(arg_value, int):
                        if condition.value == arg_value:
                            local_env: dict = self.create_local_env([condition], [arg_value], env)
                            result: any = self.execute_function_body(body, local_env)
                            return result

        # Verificar a função normal
        for func_type, params, body in func_list:
            if func_type == 'normal':
                if self.match_normal_function(params, node.arguments):
                    local_env: dict = self.create_local_env(params, node.arguments, env)
                    result: any = self.execute_function_body(body, local_env)
                    return result

        raise ValueError(f"Função {node.name} com {len(node.arguments)} argumentos e condição correspondente não definida")

    def match_normal_function(self, params: list, arguments: list) -> bool:
        """
        Verifica se a função normal pode ser chamada com os argumentos fornecidos.

        :param params: Lista de parâmetros da função.
        :param arguments: Lista de argumentos fornecidos na chamada da função.
        :return: True se o número de parâmetros e argumentos coincidir, caso contrário False.
        """
        return len(params) == len(arguments)

    def create_local_env(self, params: list, arguments: list, env: dict) -> dict:
        """
        Cria um ambiente local para a função chamada.

        :param params: Lista de parâmetros da função.
        :param arguments: Lista de argumentos fornecidos na chamada da função.
        :param env: O ambiente (contexto) de execução atual.
        :return: O ambiente local criado.
        """
        local_env: dict = env.copy()
        for param, arg in zip(params, arguments):
            if isinstance(param, ListPatternNode):
                # Avaliar o argumento para garantir que é uma lista
                arg_value: list = self.evaluate_expression(arg, local_env)
                if isinstance(arg_value, list):
                    if arg_value:  # Verifica se a lista não está vazia
                        # Extrai o valor da cabeça e da cauda da lista
                        head_val: any = arg_value[0]
                        tail_val: list = arg_value[1:] if len(arg_value) > 1 else []
                    else:
                        # Se a lista estiver vazia, atribui valores apropriados
                        head_val: any = None
                        tail_val: list = []
                    # Atribui os valores ao ambiente local
                    local_env[param.head] = head_val
                    local_env[param.tail] = tail_val
                else:
                    raise ValueError(f"Argumento para ListPatternNode não é uma lista: {arg_value}")
            else:
                # Atribui o valor do argumento ao parâmetro correspondente
                local_env[param] = self.evaluate_expression(arg, local_env)
        return local_env

    def execute_function_body(self, body: list, env: dict) -> any:
        """
        Executa o corpo da função.

        :param body: Lista de instruções no corpo da função.
        :param env: O ambiente (contexto) de execução atual.
        :return: O resultado da execução do corpo da função.
        """
        result: any = None

        # Itera sobre cada instrução no corpo da função
        for statement in body:
            # Se a instrução for um ReturnNode, avalia a expressão e retorna o valor
            if isinstance(statement, ReturnNode):
                result = self.evaluate_expression(statement.expression, env)
                return result

            elif isinstance(statement, AssignNode):
                self.interpret(statement, env)

            elif isinstance(statement, BinOpNode):
                result = self.evaluate_expression(statement, env)

            elif isinstance(statement, WriteNode):
                self.interpret(statement, env)

            elif isinstance(statement, FunctionCallNode):
                result = self.call_function(statement, env)

        # Retorna o resultado da função (se nenhum ReturnNode foi encontrado)
        return result

    def apply_operator(self, operator: str, left: any, right: any) -> any:
        """
        Aplica o operador fornecido aos operandos esquerdo e direito.

        :param operator: O operador (ex: +, -, *, /, <>).
        :param left: Operando esquerdo.
        :param right: Operando direito.
        :return: O resultado da operação.
        """
        operators: dict = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': self.safe_divide,
            '<>': lambda x, y: str(x) + str(y)
        }

        if operator in operators:
            return operators[operator](left, right)
        else:
            raise ValueError(f"Operador desconhecido: {operator}")

    def safe_divide(self, left: any, right: any) -> float:
        """
        Realiza a divisão segura dos operandos.

        :param left: Operando esquerdo.
        :param right: Operando direito.
        :return: O resultado da divisão se o divisor não for zero.
        :raise ValueError: Se o divisor for zero.
        """
        if right == 0:
            raise ValueError("Erro: Divisão por zero.")
        return left / right
