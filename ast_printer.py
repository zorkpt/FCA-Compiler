from nodes import ProgramNode, FunctionDefNode, AssignNode, BinOpNode, NumberNode, IdentifierNode, StringNode, FunctionCallNode, WriteNode
from parser import parser
from lexer import lexer

def print_ast(node, indent=0):
    prefix = "  " * indent
    if isinstance(node, ProgramNode):
        print(f"{prefix}ProgramNode:")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    elif isinstance(node, FunctionDefNode):
        print(f"{prefix}FunctionDefNode: {node.name} ({', '.join(node.params)})")
        for stmt in node.body:
            print_ast(stmt, indent + 1)
    elif isinstance(node, AssignNode):
        print(f"{prefix}AssignNode: {node.name}")
        print_ast(node.expression, indent + 1)
    elif isinstance(node, BinOpNode):
        print(f"{prefix}BinOpNode: {node.op}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, NumberNode):
        print(f"{prefix}NumberNode: {node.value}")
    elif isinstance(node, IdentifierNode):
        print(f"{prefix}IdentifierNode: {node.value}")
    elif isinstance(node, FunctionCallNode):
        print(f"{prefix}FunctionCallNode: {node.name}")
        for arg in node.args:
            print_ast(arg, indent + 1)
    elif isinstance(node, StringNode):
        print(f"{prefix}StringNode: {node.value}")
    elif isinstance(node, WriteNode):
        print(f"{prefix}WriteNode:")
        print_ast(node.expression, indent + 1)
    else:
        print(f"{prefix}Node desconhecido: {node}")

def test_parser_multiline_function():
    data = """
    FUNCAO soma2(c) :
        c = c + 1 ;
        c + 1 ;
    FIM;
    """

    result = parser.parse(data, lexer=lexer)
    print("AST gerada:")
    if result:
        print_ast(result)
    else:
        print("Erro na geração da AST")

test_parser_multiline_function()
