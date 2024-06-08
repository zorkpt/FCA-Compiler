# Decidimos criar uma classe para cada tipo de nó, pois isso facilita a organização e a manipulação da AST.
# Cada tipo de nó na árvore corresponde a uma construção sintática na linguagem de programação.
# A utilização de uma AST permite a análise e a transformação do código de forma estruturada e modular.
# Cada nó na AST possui atributos que representam os seus componentes (por exemplo, expressões, operadores, etc.)

# estamos basicamente a criar instancias destas classes e a agrupa-las no programnode, o ASTNode serve de base
# assim vai ser mais facil de usar on interpretador, e gerador de codigo c.


# Classe Base
class ASTNode:
    def __init__(self, node_type: str):
        """
        Inicializa um nó da AST (Abstract Syntax Tree).
        é uma classe base para os outros nós da ast
        :param node_type: Tipo do nó, representado como uma string.
        """
        self.node_type: str = node_type


# Classe que representa o nó do programa na AST
# Armazena todos os nós de instruções que compõem o programa.
# Essencialmente, ela coleta e organiza todas as instruções
class ProgramNode(ASTNode):
    def __init__(self, statements: list):
        super().__init__(
            'ProgramNode')  # aqui estamos a chamar o construtor da classe base (ASTNode) para definir o type.
        self.statements: list = statements


# Classe base para todos os nós de declaração (StatementNode) na árvore de sintaxe abstrata (AST).
class StatementNode(ASTNode):
    def __init__(self, statement_type: str):
        super().__init__('StatementNode')
        self.statement_type: str = statement_type


# Classe que representa um nó de função na árvore de sintaxe abstrata (AST)
class FunctionNode(StatementNode):
    def __init__(self, name: str, parameters: list, body: list):
        """
        Inicializa um nó de função.

        :param name: O nome da função.
        :param parameters: A lista de parâmetros da função.
        :param body: A lista de instruções que compõem o corpo da função.
        """
        super().__init__('FunctionNode')
        self.name: str = name
        self.parameters: list = parameters
        self.body: list = body


class WriteNode(StatementNode):
    def __init__(self, expression):
        super().__init__('WriteNode')
        self.expression = expression


class AssignNode(StatementNode):
    def __init__(self, identifier, expression):
        super().__init__('AssignNode')
        self.identifier = identifier
        self.expression = expression


class ReturnNode(StatementNode):
    def __init__(self, expression):
        super().__init__('ReturnNode')
        self.expression = expression


# representa um nó de ramificação na AST.
# Utilizado para definir funções que possuem ramos
class BranchNode(ASTNode):
    def __init__(self, function_name: str, condition: 'ExpressionNode', body: list):
        """
        Inicializa um nó de ramificação.

        :param function_name: O nome da função que contém a ramificação.
        :param condition: A condição que define a ramificação (pode ser uma expressão ou um número).
        :param body: O corpo da função que será executado se a condição for satisfeita.
        """
        super().__init__('BranchNode')  # Chama o construtor da classe base (ASTNode) para definir o tipo.
        self.function_name: str = function_name
        self.condition: 'ExpressionNode' = condition
        self.body: list = body


class BranchFunctionNode(StatementNode):
    def __init__(self, name, branches):
        super().__init__('BranchFunctionNode')
        self.name = name
        self.branches = branches


class ExpressionNode(ASTNode):
    def __init__(self, expression_type):
        super().__init__('ExpressionNode')
        self.expression_type = expression_type


class BinOpNode(ExpressionNode):
    def __init__(self, operator, left, right):
        super().__init__('BinOpNode')
        self.operator = operator
        self.left = left
        self.right = right


class NumberNode(ExpressionNode):
    def __init__(self, value):
        super().__init__('NumberNode')
        self.value = value


class IdentifierNode(ExpressionNode):
    def __init__(self, name):
        super().__init__('IdentifierNode')
        self.name = name


class StringNode(ExpressionNode):
    def __init__(self, value):
        super().__init__('StringNode')
        self.value = value


class InterpolatedStringNode(ExpressionNode):
    def __init__(self, parts):
        super().__init__('InterpolatedStringNode')
        self.parts = parts


class InputNode(ExpressionNode):
    def __init__(self):
        super().__init__('InputNode')


class RandomNode(ExpressionNode):
    def __init__(self, upper_limit):
        super().__init__('RandomNode')
        self.upper_limit = upper_limit


class FunctionCallNode(ExpressionNode):
    def __init__(self, name, arguments):
        super().__init__('FunctionCallNode')
        self.name = name
        self.arguments = arguments


class ListNode(ExpressionNode):
    def __init__(self, elements):
        super().__init__('ListNode')
        self.elements = elements


class ListPatternNode(ASTNode):
    def __init__(self, head, tail):
        super().__init__('ListPatternNode')
        self.head = head
        self.tail = tail


class MapNode(ExpressionNode):
    def __init__(self, function, list_node):
        super().__init__('MapNode')
        self.function = function
        self.list_node = list_node


class FoldNode(ExpressionNode):
    def __init__(self, function, list_node, initial_value):
        super().__init__('FoldNode')
        self.function = function
        self.list_node = list_node
        self.initial_value = initial_value
