from parser import *

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.functions = []

    def generate(self, node):
        if isinstance(node, ProgramNode):
            self.code.append("#include <stdio.h>")
            self.code.append("#include <stdlib.h>")
            for statement in node.statements:
                if isinstance(statement, FunctionNode) or isinstance(statement, BranchFunctionNode):
                    self.generate(statement)  # Gerar função antes do main
            self.code.append("int main() {")
            for statement in node.statements:
                if not isinstance(statement, FunctionNode) and not isinstance(statement, BranchFunctionNode):
                    self.generate(statement)  # Gerar outras instruções no main
            self.code.append("return 0;")
            self.code.append("}")
        elif isinstance(node, FunctionNode):
            params = ', '.join(f'int {param}' for param in node.parameters)
            body = ' '.join([self.generate_statement(s) for s in node.body])
            self.functions.append(f"int {node.name}({params}) {{ {body} }}")
        elif isinstance(node, BranchFunctionNode):
            branches = ' '.join([self.generate_branch(b) for b in node.branches])
            self.functions.append(f"int {node.name}(int n) {{ {branches} }}")
        elif isinstance(node, BranchNode):
            # Para BranchNode, vamos gerar como if dentro da função principal
            condition = f"if (n == {node.condition.value})"
            body = ' '.join([self.generate_statement(s) for s in node.body])
            self.functions.append(f"int {node.function_name}(int n) {{ {condition} {{ {body} }} else {{ return -1; }} }}")  # Retorno de -1 caso nenhuma condição seja satisfeita
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
        elif isinstance(node, WriteNode):
            format_str, args = self.generate_printf_args(node.expression)
            return f'printf("{format_str}\\n"{", " + args if args else ""});'
        else:
            raise ValueError(f"Unknown expression type: {type(node)}")

    def generate_statement(self, node):
        if isinstance(node, AssignNode):
            return f"{node.identifier} = {self.generate_expression(node.expression)};"
        elif isinstance(node, ReturnNode):
            return f"return {self.generate_expression(node.expression)};"
        elif isinstance(node, FunctionCallNode):
            return f"{self.generate_expression(node)};"
        elif isinstance(node, BinOpNode):
            return self.generate_expression(node)
        else:
            return self.generate_expression(node)

    def generate_branch(self, node):
        condition = f"if (n == {node.condition.value})"
        body = ' '.join([self.generate_statement(s) for s in node.body])
        return f"{condition} {{ {body} }}"

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
