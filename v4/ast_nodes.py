# Definição das classes da AST com métodos de impressão

# Classes Base

class ASTNode:
    def __init__(self, node_type):
        self.node_type = node_type

    def __repr__(self):
        return f"{self.node_type}()"


# FIM CATEGORIA

# Estrutura do Programa

class ProgramNode(ASTNode):
    def __init__(self, statements):
        super().__init__('ProgramNode')
        self.statements = statements

    def __repr__(self):
        return f"{self.node_type}({self.statements})"


# FIM CATEGORIA

# Declarações (Statements)

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


class ReturnNode(StatementNode):
    def __init__(self, expression):
        super().__init__('ReturnNode')
        self.expression = expression

    def __repr__(self):
        return f"{self.statement_type}({self.expression})"


class FunctionNode(StatementNode):
    def __init__(self, name, parameters, body):
        super().__init__('FunctionNode')
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"{self.statement_type}({self.name}, {self.parameters}, {self.body})"


class BranchNode(ASTNode):
    def __init__(self, function_name, condition, body):
        super().__init__('BranchNode')
        self.function_name = function_name
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"{self.node_type}({self.function_name}, {self.condition}, {self.body})"


class BranchFunctionNode(StatementNode):
    def __init__(self, name, branches):
        super().__init__('BranchFunctionNode')
        self.name = name
        self.branches = branches

    def __repr__(self):
        return f"{self.statement_type}({self.name}, {self.branches})"


class IfNode(StatementNode):
    def __init__(self, condition, body):
        super().__init__('IfNode')
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"IfNode(condition={self.condition}, body={self.body})"


# FIM CATEGORIA

# Expressões (Expressions)

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


class FunctionCallNode(ExpressionNode):
    def __init__(self, name, arguments):
        super().__init__('FunctionCallNode')
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"{self.expression_type}({self.name}, {self.arguments})"


# FIM CATEGORIA

# Listas e Operações em Listas

class ListNode(ExpressionNode):
    def __init__(self, elements):
        super().__init__('ListNode')
        self.elements = elements

    def __repr__(self):
        return f"{self.expression_type}({self.elements})"


class ListPatternNode(ASTNode):
    def __init__(self, head, tail):
        super().__init__('ListPatternNode')
        self.head = head
        self.tail = tail

    def __repr__(self):
        return f"{self.node_type}({self.head}, {self.tail})"


class MapNode(ExpressionNode):
    def __init__(self, function, list_node):
        super().__init__('MapNode')
        self.function = function
        self.list_node = list_node

    def __repr__(self):
        return f"{self.expression_type}({self.function}, {self.list_node})"


class FoldNode(ExpressionNode):
    def __init__(self, function, list_node, initial_value):
        super().__init__('FoldNode')
        self.function = function
        self.list_node = list_node
        self.initial_value = initial_value

    def __repr__(self):
        return f"{self.expression_type}({self.function}, {self.list_node}, {self.initial_value})"

# FIM CATEGORIA
