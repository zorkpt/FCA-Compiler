import random
from ast_nodes import *

class Interpreter:
    def __init__(self):
        self.symbol_table = {}
        self.functions = {}
        self.call_stack = []

    def interpret(self, node):
        if isinstance(node, ProgramNode):
            for statement in node.statements:
                self.interpret(statement)
        elif isinstance(node, FunctionNode):
            if node.name not in self.functions:
                self.functions[node.name] = []
            self.functions[node.name].append(('normal', node.parameters, node.body))
        elif isinstance(node, BranchNode):
            func_name = node.function_name
            if func_name not in self.functions:
                self.functions[func_name] = []
            self.functions[func_name].append(('branch', node))
        elif isinstance(node, AssignNode):
            value = self.evaluate_expression(node.expression)
            self.symbol_table[node.identifier] = value
        elif isinstance(node, WriteNode):
            value = self.evaluate_expression(node.expression)
            print(f"ESCREVER: {value}")
        elif isinstance(node, ReturnNode):
            return self.evaluate_expression(node.expression)
        elif isinstance(node, FunctionCallNode):
            return self.call_function(node)
        elif isinstance(node, BinOpNode):
            return self.evaluate_expression(node)
        else:
            raise ValueError(f"Unknown statement type: {type(node)}")

    def evaluate_expression(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, int):
            return node
        elif isinstance(node, BinOpNode):
            left = self.evaluate_expression(node.left)
            right = self.evaluate_expression(node.right)
            return self.apply_operator(node.operator, left, right)
        elif isinstance(node, IdentifierNode):
            value = self.symbol_table.get(node.name, None)
            if value is None:
                raise ValueError(f"Variável não encontrada: {node.name}")
            return value
        elif isinstance(node, FunctionCallNode):
            return self.call_function(node)
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, WriteNode):
            return self.evaluate_expression(node.expression)
        elif isinstance(node, InterpolatedStringNode):
            parts = []
            for part in node.parts:
                if isinstance(part, StringNode):
                    parts.append(part.value)
                elif isinstance(part, IdentifierNode):
                    parts.append(str(self.symbol_table.get(part.name, "")))
            return ''.join(parts)
        elif isinstance(node, InputNode):
            return int(input())
        elif isinstance(node, RandomNode):
            return random.randint(0, self.evaluate_expression(node.upper_limit))
        elif isinstance(node, ListNode):
            return [self.evaluate_expression(element) for element in node.elements]
        elif isinstance(node, MapNode):
            list_value = self.evaluate_expression(node.list_node)
            return [self.call_function(FunctionCallNode(node.function, [element])) for element in list_value]
        elif isinstance(node, FoldNode):
            result = self.evaluate_expression(node.initial_value)
            list_value = self.evaluate_expression(node.list_node)
            for element in list_value:
                result = self.call_function(FunctionCallNode(node.function, [result, element]))
            return result
        else:
            raise ValueError(f"Unknown expression type: {type(node)}")

    def call_function(self, node):
        func_list = self.functions.get(node.name)
        if func_list is None:
            raise ValueError(f"Função não definida: {node.name}")

        self.call_stack.append(node.name)
        if len(self.call_stack) > 50:  # Limite arbitrário para a profundidade da recursão
            raise RecursionError(f"Recursion depth exceeded in function {node.name}")

        for func_type, *func_data in func_list:
            if func_type == 'branch':
                branch = func_data[0]
                if self.evaluate_expression(branch.condition) == self.evaluate_expression(node.arguments[0]):
                    result = self.execute_branch_body(branch.body)
                    self.call_stack.pop()
                    return result
            elif func_type == 'normal':
                params, body = func_data
                if len(params) == len(node.arguments):
                    local_env = self.symbol_table.copy()
                    local_env.update({param: self.evaluate_expression(arg) for param, arg in zip(params, node.arguments)})
                    result = self.execute_function_body(body, local_env)
                    self.call_stack.pop()
                    return result
                elif isinstance(params[0], ListPatternNode):
                    if isinstance(node.arguments[0], list):
                        head = node.arguments[0][0] if node.arguments[0] else None
                        tail = node.arguments[0][1:] if len(node.arguments[0]) > 1 else []
                        local_env = self.symbol_table.copy()
                        local_env[params[0].head] = head
                        local_env[params[0].tail] = tail
                        result = self.execute_function_body(body, local_env)
                        self.call_stack.pop()
                        return result

        self.call_stack.pop()
        raise ValueError(f"Função {node.name} com {len(node.arguments)} argumentos e condição correspondente não definida")

    def execute_branch_body(self, body):
        result = None
        for statement in body:
            if isinstance(statement, ReturnNode):
                result = self.evaluate_expression(statement.expression)
                break
        return result

    def execute_function_body(self, body, env):
        old_env = self.symbol_table
        self.symbol_table = env
        result = None
        for statement in body:
            if isinstance(statement, ReturnNode):
                result = self.evaluate_expression(statement.expression)
                break
            elif isinstance(statement, AssignNode):
                value = self.evaluate_expression(statement.expression)
                self.symbol_table[statement.identifier] = value
                env[statement.identifier] = value  # Atualize o ambiente local
            else:
                result = self.interpret(statement)  # Interpret other statements directly
        self.symbol_table = old_env
        return result

    def apply_operator(self, operator, left, right):
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
