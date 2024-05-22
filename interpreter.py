from nodes import *

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def interpret(self, node):
        if isinstance(node, ProgramNode):
            for statement in node.statements:
                self.interpret(statement)
        elif isinstance(node, FunctionDefNode):
            self.functions[node.name] = node
        elif isinstance(node, AssignNode):
            value = self.evaluate_expression(node.expression)
            self.variables[node.name] = value
        elif isinstance(node, BinOpNode):
            self.evaluate_expression(node)
        elif isinstance(node, WriteNode):
            value = self.evaluate_expression(node.expression)
            print(value)
        else:
            raise ValueError(f"Node desconhecido: {node}")

    def evaluate_expression(self, node):
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            if node.value in self.variables:
                return self.variables[node.value]
            else:
                raise ValueError(f"Variável não definida: {node.value}")
        elif isinstance(node, BinOpNode):
            left_val = self.evaluate_expression(node.left)
            right_val = self.evaluate_expression(node.right)
            if node.op == '+':
                return left_val + right_val
            elif node.op == '-':
                return left_val - right_val
            elif node.op == '*':
                return left_val * right_val
            elif node.op == '/':
                return left_val / right_val
        elif isinstance(node, FunctionCallNode):
            if node.name in self.functions:
                func = self.functions[node.name]
                local_vars = {param: self.evaluate_expression(arg) for param, arg in zip(func.params, node.args)}
                self.variables.update(local_vars)
                for statement in func.body:
                    self.interpret(statement)
                return self.evaluate_expression(func.body[-1].expression)
            else:
                raise ValueError(f"Função não definida: {node.name}")
        else:
            raise ValueError(f"Expressão desconhecida: {node}")



# Certifique-se de que todas as classes de nó (Node) estão definidas corretamente em nodes.py
