from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.functions = []
        self.branch_conditions = {}

    def generate(self, node):
        if isinstance(node, ProgramNode):
            self.code.append("#include <stdio.h>")
            self.code.append("#include <stdlib.h>")
            self.add_map_function()
            self.add_fold_function()
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
            if isinstance(node.parameters[0], ListPatternNode):
                param_str = f"int {node.parameters[0].head}, int* {node.parameters[0].tail}, int size"
            else:
                params = ', '.join(f'int {param}' for param in node.parameters)
                param_str = f"{params}"
            body = ' '.join([self.generate_statement(s) for s in node.body])
            if node.name in self.branch_conditions:
                branches = ' '.join(self.branch_conditions[node.name])
                body = f"{branches} {body}"
            self.functions.append(f"int {node.name}({param_str}) {{ {body} return -1; }}")
        elif isinstance(node, BranchNode):
            condition = f"if (n == {node.condition.value})"
            body = ' '.join([self.generate_statement(s) for s in node.body])
            if node.function_name not in self.branch_conditions:
                self.branch_conditions[node.function_name] = []
            self.branch_conditions[node.function_name].append(f"{condition} {{ {body} }}")
        elif isinstance(node, AssignNode):
            value = self.generate_expression(node.expression)
            if isinstance(node.expression, ListNode):
                self.code.append(f'int {node.identifier}[] = {value};')
            elif isinstance(node.expression, StringNode):
                self.code.append(f'const char* {node.identifier} = {value};')
            else:
                self.code.append(f'int {node.identifier} = {value};')
        elif isinstance(node, WriteNode):
            format_str, args = self.generate_printf_args(node.expression)
            if args:
                self.code.append(f'printf("{format_str}\\n", {args});')
            else:
                self.code.append(f'printf("{format_str}\\n");')
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
            args = ', '.join(self.generate_expression(arg) for arg in node.arguments)
            return f"{node.name}({args})"
        elif isinstance(node, WriteNode):
            format_str, args = self.generate_printf_args(node.expression)
            return format_str, args
        elif isinstance(node, ListNode):
            elements = ', '.join(self.generate_expression(element) for element in node.elements)
            return f'{{ {elements} }}'
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
        else:
            expr = self.generate_expression(node)
            return "%s", expr

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
        return '\n'.join(self.code[:3] + self.functions + self.code[3:])
