from ast_nodes import *


class CodeGenerator:
    def __init__(self):
        self.code = []
        self.functions = []
        self.branch_conditions = {}
        self.map_used = False
        self.fold_used = False

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

            if self.map_used:
                self.add_map_function()
            if self.fold_used:
                self.add_fold_function()

        elif isinstance(node, FunctionNode):
            if isinstance(node.parameters[0], ListPatternNode):
                param_str = f"int {node.parameters[0].head}, int* {node.parameters[0].tail}, int size"
            else:
                params = ', '.join(f'int {param}' for param in node.parameters)
                param_str = f"{params}"
            body = ' '.join(
                [self.generate_statement(s, is_last=(i == len(node.body) - 1)) for i, s in enumerate(node.body)])
            if node.name in self.branch_conditions:
                branches = ' '.join(self.branch_conditions[node.name])
                body = f"{branches} {body}"
            self.functions.append(f"int {node.name}({param_str}) {{ {body} }}")

        elif isinstance(node, BranchNode):
            condition = f"if (n == {node.condition.value})"
            body = ' '.join([self.generate_statement(s) for s in node.body])
            if node.function_name not in self.branch_conditions:
                self.branch_conditions[node.function_name] = []
            self.branch_conditions[node.function_name].append(f"{condition} {{ {body} }}")

        elif isinstance(node, AssignNode):
            identifier = self.normalize_identifier(node.identifier)
            if isinstance(node.expression, InputNode):
                self.code.append(f'int {identifier};')
                self.code.append(f'scanf("%d", &{identifier});')
            else:
                value = self.generate_expression(node.expression)
                if isinstance(node.expression, ListNode):
                    self.code.append(f'int {identifier}[] = {value};')
                elif isinstance(node.expression, StringNode):
                    self.code.append(f'const char* {identifier} = {value};')
                else:
                    self.code.append(f'int {identifier} = {value};')

        elif isinstance(node, WriteNode):
            format_str, args = self.generate_printf_args(node.expression)
            if args:
                self.code.append(f'printf("{format_str}\\n", {args});')
            else:
                self.code.append(f'printf("{format_str}\\n");')

        elif isinstance(node, FunctionCallNode):
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
                return f'{left_value} {right_value}'
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
            if node.name == "map":
                self.map_used = True
            elif node.name == "fold":
                self.fold_used = True
            args = ', '.join(self.generate_expression(arg) for arg in node.arguments)
            return f"{node.name}({args})"
        elif isinstance(node, WriteNode):
            format_str, args = self.generate_printf_args(node.expression)
            if args:
                self.code.append(f'printf("{format_str}\\n", {args});')
            else:
                self.code.append(f'printf("{format_str}\\n");')
        elif isinstance(node, ListNode):
            elements = ', '.join(self.generate_expression(element) for element in node.elements)
            return f'{{ {elements} }}'
        elif isinstance(node, RandomNode):
            return f"rand() % {self.generate_expression(node.upper_limit)}"
        else:
            raise ValueError(f"Unknown expression type: {type(node)}")

    def generate_statement(self, node, is_last=False):
        if isinstance(node, AssignNode):
            stmt = f"{node.identifier} = {self.generate_expression(node.expression)};"
        elif isinstance(node, ReturnNode):
            stmt = f"return {self.generate_expression(node.expression)};"
        elif isinstance(node, FunctionCallNode):
            stmt = f"{self.generate_expression(node)};"
        elif isinstance(node, BinOpNode):
            stmt = self.generate_expression(node)
        else:
            stmt = self.generate_expression(node)

        if is_last and not stmt.startswith("return"):
            stmt = f"return {stmt};"
        elif not stmt.startswith("return"):
            stmt = f"{stmt};"

        return stmt

    def generate_printf_args(self, node):
        if isinstance(node, BinOpNode) and node.operator == '<>':
            left_str, left_args = self.generate_printf_args(node.left)
            right_str, right_args = self.generate_printf_args(node.right)
            format_str = f"{left_str}{right_str}"
            args = f"{left_args}, {right_args}".strip(", ")
            return format_str, args
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
        elif isinstance(node, StringNode):
            return node.value, ""
        elif isinstance(node, RandomNode):
            return "%d", self.generate_expression(node)
        elif isinstance(node, BinOpNode):
            return "%d", self.generate_expression(node)
        elif isinstance(node, IdentifierNode):
            normalized_name = self.normalize_identifier(node.name)
            if self.is_string_identifier(normalized_name):
                return "%s", normalized_name
            else:
                return "%d", normalized_name
        elif isinstance(node, NumberNode):
            return "%d", str(node.value)
        else:
            expr = self.generate_expression(node)
            return "%s", expr

    def is_string_identifier(self, name):
        """
        Verifica se o identificador é tratado como uma string com base na sua declaração.
        """
        for stmt in self.code:
            if f'const char* {name}' in stmt:
                return True
        return False

    def is_string_function(self, name):
        """
        Verifica se a função retorna uma string com base na sua definição.
        """
        for func in self.functions:
            if f'const char* {name}' in func:
                return True
        return False

    def add_map_function(self):
        self.code.append('void map(int (*func)(int), int *arr, int size) {')
        self.code.append('    for (int i = 0; i < size; i++) {')
        self.code.append('        arr[i] = func(arr[i]);')
        self.code.append('    }')
        self.code.append('}')

    def add_fold_function(self):
        self.code.append('int fold(int (*func)(int, int), int *arr, int size, int initial) {')
        self.code.append('    int result = initial;')
        self.code.append('    for (int i = 0; i < size; i++) {')
        self.code.append('        result = func(result, arr[i]);')
        self.code.append('    }')
        self.code.append('    return result;')
        self.code.append('}')

    def get_code(self):
        # Combinar as funções geradas e o código principal
        return '\n'.join(self.code[:3] + self.functions + self.code[3:])

    def normalize_identifier(self, name):
        return name.replace('?', 'PontInter').replace('!', 'PontExcl')
