from typing import List, Dict

from ast_nodes import *


class CodeGenerator:
    def __init__(self):
        self.code: List[str] = []
        self.functions: List[str] = []
        self.branch_conditions: Dict[str, List[str]] = {}
        self.function_parameters: Dict[str, str] = {}
        self.map_used: bool = False
        self.fold_used: bool = False

    def generate(self, node: ASTNode):
        if isinstance(node, ProgramNode):
            self.code.append("#include <stdio.h>")
            self.code.append("#include <stdlib.h>")

            # Primeiro, armazena os nomes e parâmetros das funções
            for statement in node.statements:
                if isinstance(statement, FunctionNode):
                    self.store_function_parameters(statement)

            # Depois processa todos os BranchNode
            for statement in node.statements:
                if isinstance(statement, BranchNode):
                    self.generate(statement)

            # Depois geramos as funções normais
            for statement in node.statements:
                if isinstance(statement, FunctionNode):
                    self.generate(statement)

            # Verifica se 'map' ou 'fold' foram usados e adiciona as funções
            if self.map_used:
                self.add_map_function()
            if self.fold_used:
                self.add_fold_function()

            self.code.append("int main() {")
            for statement in node.statements:
                if not isinstance(statement, FunctionNode) and not isinstance(statement, BranchNode):
                    self.generate(statement)  # Gerar outras instruções no main
            self.code.append("return 0;")
            self.code.append("}")

            if self.map_used:
                self.add_map_function()
            if self.fold_used:
                self.add_fold_function()

        elif isinstance(node, FunctionNode):
            # Gera a definição da função
            params = ', '.join(f'int {param}' for param in node.parameters)
            param_str = f"{params}"

            # Gera o corpo da função
            body_parts: list = []
            # usando o enumerate temos acesso ao index do loop (i)
            for i, s in enumerate(node.body):
                # para vermos se estamos na ultima instrucao comparamos o i com o tamanho do body-1
                is_last: bool = (i == len(node.body) - 1)

                # Geramos o código C para este s. Passamos o boolean para adicionarmos return ou nao.
                body_parts.append(self.generate_statement(s, is_last=is_last))

            # Juntamos as body parts ao body com ' '
            body = ' '.join(body_parts)

            # Adiciona condições de ramos, se houver
            if node.name in self.branch_conditions:
                branches = ' '.join(self.branch_conditions[node.name])
                body = f"{branches} {body}"

            # Gera o nome da função
            function_name = f"{node.name}_{len(node.parameters)}"

            # Adiciona a definição da função gerada à lista de funções
            self.functions.append(f"int {function_name}({param_str}) {{ {body} }}")

        elif isinstance(node, BranchNode):

            # Buscar o nome do parâmetro da função original
            func_name = node.function_name
            if func_name not in self.function_parameters:
                raise ValueError(f"Parâmetro não encontrado para a função {func_name}")
            param_name = self.function_parameters[func_name]

            # Gera a condição do ramo
            condition = f"if ({param_name} == {node.condition.value})"
            body = ' '.join([self.generate_statement(s) for s in node.body])
            if node.function_name not in self.branch_conditions:
                self.branch_conditions[node.function_name] = []
            self.branch_conditions[node.function_name].append(f"{condition} {{ {body} }}")

        elif isinstance(node, AssignNode):
            value = self.generate_expression(node.expression)
            if isinstance(node.expression, ListNode):
                self.code.append(f'int {node.identifier}[] = {value};')
            elif isinstance(node.expression, StringNode):
                self.code.append(f'const char* {self.normalize_identifier(node.identifier)} = {value};')
            else:
                self.code.append(f'int {self.normalize_identifier(node.identifier)} = {value};')

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

    def store_function_parameters(self, node: FunctionNode):
        """
        Armazena o nome do parâmetro da função para uso posterior em BranchNode.
        """
        if node.parameters:
            self.function_parameters[node.name] = node.parameters[0]

    def generate_expression(self, node: ASTNode) -> str:
        """
        Gera a expressão correspondente ao nó fornecido na AST.

        :param node: O nó da AST a ser convertido em código C.
        :return: Uma string contendo a expressão gerada em código C.
        """
        if isinstance(node, NumberNode):
            return str(node.value)  # Retorna o valor do nó numérico como string

        elif isinstance(node, IdentifierNode):
            return self.normalize_identifier(node.name)  # Normaliza e retorna o identificador

        elif isinstance(node, BinOpNode):
            left_value: str = self.generate_expression(node.left)  # Gera a expressão do operando esquerdo
            right_value: str = self.generate_expression(node.right)  # Gera a expressão do operando direito
            if node.operator == '<>':
                return f'{left_value} {right_value}'  # Concatenação de strings
            else:
                return f"({left_value} {node.operator} {right_value})"  # Operação binária

        elif isinstance(node, InterpolatedStringNode):
            format_str: str = ''
            args: List[str] = []
            for part in node.parts:
                if isinstance(part, StringNode):
                    format_str += part.value  # Adiciona parte da string ao formato
                elif isinstance(part, IdentifierNode):
                    format_str += '%s'  # Adiciona marcador de string
                    args.append(self.normalize_identifier(part.name))  # Adiciona identificador à lista de argumentos
            return format_str, ', '.join(args)  # Retorna a string formatada e os argumentos

        elif isinstance(node, InputNode):
            return "scanf(\"%d\", &input)"  # Gera código de entrada do usuário

        elif isinstance(node, StringNode):
            return f'"{node.value}"'  # Retorna a string com aspas

        elif isinstance(node, FunctionCallNode):
            if node.name == "map":
                self.map_used = True  # Marca que a função map foi usada
            elif node.name == "fold":
                self.fold_used = True  # Marca que a função fold foi usada
            args: str = ', '.join(self.generate_expression(arg) for arg in node.arguments)  # Gera os argumentos
            function_name: str = f"{node.name}_{len(node.arguments)}"  # Gera o nome da função com o número de argumentos
            return f"{function_name}({args})"  # Retorna a chamada da função

        elif isinstance(node, WriteNode):
            format_str, args = self.generate_printf_args(node.expression)
            if args:
                self.code.append(f'printf("{format_str}\\n", {args});')  # Gera código printf com argumentos
            else:
                self.code.append(f'printf("{format_str}\\n");')  # Gera código printf sem argumentos

        elif isinstance(node, ListNode):
            elements: str = ', '.join(
                self.generate_expression(element) for element in node.elements)  # Gera elementos da lista
            return f'{{ {elements} }}'  # Retorna a lista formatada

        elif isinstance(node, RandomNode):
            return f"rand() % {self.generate_expression(node.upper_limit)}"  # Gera código para número aleatório

        elif isinstance(node, MapNode):
            # Gerar código para chamada de função 'map'
            function = self.generate_expression(node.function)
            list_expr = self.generate_expression(node.list_node)
            size_expr = f"sizeof({list_expr}) / sizeof({list_expr}[0])"
            return f"map({function}, {list_expr}, {size_expr})"

        elif isinstance(node, FoldNode):
            # Gerar código para chamada de função 'fold'
            function = self.generate_expression(node.function)
            list_expr = self.generate_expression(node.list_node)
            initial_expr = self.generate_expression(node.initial_value)
            size_expr = f"sizeof({list_expr}) / sizeof({list_expr}[0])"
            return f"fold({function}, {list_expr}, {size_expr}, {initial_expr})"

        else:
            raise ValueError(f"Unknown expression type: {type(node)}")  # Exceção para tipos desconhecidos

    def generate_statement(self, node: ASTNode, is_last: bool = False) -> str:
        """
        Gera a instrução correspondente ao nó fornecido na AST.

        :param node: O nó da AST a ser convertido em código C.
        :param is_last: Indica se esta é a última instrução na função.
        :return: Uma string contendo a instrução gerada em código C.
        """
        if isinstance(node, AssignNode):
            # Gera uma declaração de variável e atribuição
            stmt: str = f"int {self.normalize_identifier(node.identifier)} = {self.generate_expression(node.expression)};"

        elif isinstance(node, ReturnNode):
            # Gera uma instrução de retorno
            stmt: str = f"return {self.generate_expression(node.expression)};"

        elif isinstance(node, FunctionCallNode):
            # Gera uma chamada de função
            stmt: str = f"{self.generate_expression(node)};"

        elif isinstance(node, BinOpNode):
            # Gera uma expressão binária
            stmt: str = self.generate_expression(node)

        elif isinstance(node, MapNode):
            # Gerar a chamada da função map
            stmt = self.generate_expression(node)

        elif isinstance(node, FoldNode):
            # Gerar a chamada da função fold
            stmt = self.generate_expression(node)

        else:
            # Gera outras expressões
            stmt: str = self.generate_expression(node)

        # Adiciona um "return" se esta for a última instrução e não for um retorno
        if is_last and not stmt.startswith("return"):
            stmt = f"return {stmt};"
        # Adiciona ponto e vírgula para outras instruções que não sejam "return"
        elif not stmt.startswith("return"):
            stmt = f"{stmt};"

        return stmt  # Retorna a instrução gerada

    def generate_printf_args(self, node: ASTNode) -> tuple:
        """
        Gera os argumentos para a função printf em C com base no nó fornecido na AST.

        :param node: O nó da AST a ser convertido em argumentos de printf.
        :return: Uma tupla contendo a string de formato e os argumentos para printf.
        """
        if isinstance(node, BinOpNode) and node.operator == '<>':
            # Concatenação de strings
            left_str, left_args = self.generate_printf_args(node.left)
            right_str, right_args = self.generate_printf_args(node.right)
            format_str: str = f"{left_str}{right_str}"
            args: str = f"{left_args}, {right_args}".strip(", ")
            return format_str, args

        elif isinstance(node, InterpolatedStringNode):
            # String interpolada
            format_str: str = ''
            args: list[str] = []
            for part in node.parts:
                if isinstance(part, StringNode):
                    format_str += part.value
                elif isinstance(part, IdentifierNode):
                    format_str += '%s'
                    args.append(self.normalize_identifier(part.name))
            return format_str, ', '.join(args)

        elif isinstance(node, StringNode):
            # String simples
            return node.value, ""

        elif isinstance(node, IdentifierNode):
            # Identificador
            normalized_name: str = self.normalize_identifier(node.name)
            if self.is_string_identifier(normalized_name):
                return "%s", normalized_name
            else:
                return "%d", normalized_name

        elif isinstance(node, NumberNode):
            # Número
            return "%d", str(node.value)

        elif isinstance(node, RandomNode):
            # Número aleatório
            return "%d", self.generate_expression(node)

        elif isinstance(node, BinOpNode):
            # Expressão binária
            return "%d", self.generate_expression(node)

        else:
            # Expressão genérica
            expr: str = self.generate_expression(node)
            return "%s", expr

    def is_string_identifier(self, name: str) -> bool:
        """
        Verifica se o identificador é tratado como uma string com base na sua declaração.
        """
        for stmt in self.code:
            if f'const char* {name}' in stmt:
                return True
        return False

    def is_string_function(self, name: str) -> bool:
        """
        Verifica se a função retorna uma string com base na sua definição.
        """
        for func in self.functions:
            if f'const char* {name}' in func:
                return True
        return False

    def normalize_identifier(self, name: str) -> str:
        """
        Normaliza os identificadores para remover caracteres inválidos para C.
        """
        return name.replace('!', 'PontExcl').replace('?', 'PontInter')

    def add_map_function(self):
        """
        Adiciona a função 'map' ao código gerado.
        A função 'map' aplica uma função a cada elemento de uma lista.
        """
        map_function_code: list[str] = [
            'void map(int (*func)(int), int *arr, int size) {',
            '    for (int i = 0; i < size; i++) {',
            '        arr[i] = func(arr[i]);',
            '    }',
            '}'
        ]
        # Adiciona a função 'map' ao início do código (antes do 'main')
        self.code = map_function_code + self.code

    def add_fold_function(self):
        """
        Adiciona a função 'fold' ao código gerado.
        A função 'fold' reduz uma lista a um único valor usando uma função acumuladora.
        """
        fold_function_code: list[str] = [
            'int fold(int (*func)(int, int), int *arr, int size, int initial) {',
            '    int result = initial;',
            '    for (int i = 0; i < size; i++) {',
            '        result = func(result, arr[i]);',
            '    }',
            '    return result;',
            '}'
        ]
        # Adiciona a função 'fold' ao início do código (antes do 'main')
        self.code = fold_function_code + self.code

    def get_code(self) -> str:
        """
        Combina as funções geradas e o código principal em uma string única.

        Retorna:
            str: Código C completo gerado.
        """
        # Junta as primeiras 3 linhas de código (importações), as funções geradas e o restante do código principal.
        # A estrutura é:
        # - self.code[:3]: Importações do cabeçalho (por exemplo, #include <stdio.h>, etc.)
        # - self.functions: Funções definidas (por exemplo, int soma(int a, int b) { ... })
        # - self.code[3:]: Restante do código principal (corpo da função main)
        return '\n'.join(self.code[:3] + self.functions + self.code[3:])

