class ASTNode:
    pass


class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class AssignNode(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression


class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name


class BinOpNode(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value


class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value


class FunctionDefNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class FunctionCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args


class WriteNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression


class InterpolatedStringNode(ASTNode):
    def __init__(self, parts):
        self.parts = parts


class InputNode(ASTNode):
    pass


class RandomNode(ASTNode):
    def __init__(self, upper_limit):
        self.upper_limit = upper_limit
