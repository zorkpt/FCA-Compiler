from ast_nodes import *
import ply.yacc as yacc
from lexer import tokens

# Regra de produção inicial para o programa.
# define a estrutura inicial do programa, que consiste numa lista de instruções.
# é o nó da raiz da árvore ast
def p_programa(p):
    '''programa : lista_instrucoes'''
    p[0] = ProgramNode(p[1])


# Regra de produção para uma lista de instruções.
# Uma lista de instruções pode ser composta por uma única instrução ou por várias instruções.
def p_lista_instrucoes(p):
    '''lista_instrucoes : instrucao
                        | lista_instrucoes instrucao'''
    # Se tiver len de 2 , so tem uma instrucao
    if len(p) == 2:
        p[0] = [p[1]]
    # senao, guardar varias instrucoes
    else:
        p[0] = p[1] + [p[2]]


# Regra de produção para uma declaração de função inline.
# Esta regra define funções que são declaradas numa única linha.
def p_instrucao_funcao_inline(p):
    '''instrucao : FUNCAO IDENTIFICADOR PARENTESES_ESQ parametros PARENTESES_DIR VIRGULA DOIS_PONTOS expressao PONTO_E_VIRGULA'''
    # p[2] : nome da funcao
    # p[4] : parametro da funcao
    # p[8] : expressao de return
    p[0] = FunctionNode(p[2], p[4], [ReturnNode(p[8])])


# Regra de produção para uma declaração de função com padrão de lista inline.
# Define funções inline que utilizam padrões de lista na sua definição.
def p_instrucao_funcao_padrao_lista_inline(p):
    '''instrucao : FUNCAO IDENTIFICADOR PARENTESES_ESQ padrao_lista PARENTESES_DIR VIRGULA DOIS_PONTOS expressao PONTO_E_VIRGULA'''
    # p[2] : nome da funcao (ex: somatorio)
    # p[4] : padrao de lista utilizado como parametro da funcao (ex: x:xs)
    # p[8] : expressao de return (ex: x + somatorio(xs))
    p[0] = FunctionNode(p[2], [p[4]], [ReturnNode(p[8])])

# Exemplo de uso:
# FUNCAO somatorio(x:xs), : x + somatorio(xs);


# Regra de produção para uma função de múltiplas linhas.
# Esta regra define funções que se estendem por várias linhas, permitindo uma lista de instruções como corpo da função.
def p_instrucao_funcao_multilinhas(p):
    '''instrucao : FUNCAO IDENTIFICADOR PARENTESES_ESQ parametros PARENTESES_DIR DOIS_PONTOS lista_instrucoes FIM'''
    # p[2] : nome da funcao (ex: soma)
    # p[4] : parametros da funcao (ex: x, y)
    # p[7] : lista de instrucoes que compõem o corpo da funcao (ex: a = x + y; ESCREVER(a);)
    p[0] = FunctionNode(p[2], p[4], p[7])

# Exemplo:
# FUNCAO soma(x, y):
#     a = x + y;
#     ESCREVER(a);
# FIM


# Regra de produção para uma função de múltiplas linhas com padrão de lista.
# Esta regra define funções de múltiplas linhas que utilizam padrões de lista.
def p_instrucao_funcao_padrao_lista_multilinhas(p):
    '''instrucao : FUNCAO IDENTIFICADOR PARENTESES_ESQ padrao_lista PARENTESES_DIR DOIS_PONTOS lista_instrucoes FIM'''
    # p[2] : nome da funcao (ex: somatorio)
    # p[4] : padrao de lista utilizado como parametro da funcao (ex: x:xs)
    # p[7] : lista de instrucoes que compõem o corpo da funcao (ex: ESCREVER(x); ESCREVER(xs);)
    p[0] = FunctionNode(p[2], [p[4]], p[7])

# Exemplo de uso:
# FUNCAO somatorio( x:xs ),: x + somatorio(xs) ;


# Regra de produção para uma chamada de função.
# Esta regra define a estrutura de uma chamada de função com argumentos.
def p_expressao_chamada_funcao(p):
    '''expressao : IDENTIFICADOR PARENTESES_ESQ argumentos PARENTESES_DIR'''
    # p[1] : nome da função (ex: soma)
    # p[3] : lista de argumentos passados para a função (ex: x, y)
    p[0] = FunctionCallNode(p[1], p[3])


# Regra de produção para uma declaração de função com ramificação.
# Esta regra define funções que incluem ramificações baseadas em expressões ou números.
def p_instrucao_funcao_ramo(p):
    '''instrucao : FUNCAO IDENTIFICADOR PARENTESES_ESQ expressao PARENTESES_DIR VIRGULA DOIS_PONTOS expressao PONTO_E_VIRGULA
                 | FUNCAO IDENTIFICADOR PARENTESES_ESQ NUMERO PARENTESES_DIR VIRGULA DOIS_PONTOS expressao PONTO_E_VIRGULA'''
    nome_funcao = p[2]  # Nome da função (ex: fibonacci)
    # Verifica se a condição é uma lista (padrão de lista) ou um número
    if isinstance(p[4], ListNode):
        condicao = p[4]  # Condição de lista (padrão de lista)
    else:
        condicao = NumberNode(p[4])  # Condição de número
    corpo = [ReturnNode(p[8])]  # Corpo da função (expressão de retorno)
    p[0] = BranchNode(nome_funcao, condicao, corpo)  # criar um nó de ramo

# Exemplo de uso com condição de lista:
# FUNCAO somatorio(x:xs), : x + somatorio(xs);

# Exemplo de uso com condição de número:
# FUNCAO fibonacci(0), : 0;


# Regra de produção para parâmetros.
# Esta regra define a estrutura de parâmetros, incluindo múltiplos, únicos e vazios.
def p_parametros(p):
    '''parametros : parametros VIRGULA IDENTIFICADOR
                  | IDENTIFICADOR
                  | '''
    # Se houver múltiplos parâmetros (parametros, IDENTIFICADOR)
    if len(p) == 4:
        # p[1] : Lista de parâmetros acumulada até agora
        # p[3] : Novo identificador (parâmetro) encontrado após a vírgula
        p[0] = p[1] + [p[3]]  # Adiciona o novo identificador à lista de parâmetros acumulada
    # Se houver um único parâmetro (IDENTIFICADOR)
    elif len(p) == 2:
        # p[1] : Identificador encontrado (parâmetro único)
        p[0] = [p[1]]  # Cria uma lista contendo o identificador como único parâmetro
    # Se não houver parâmetros (vazio)
    else:
        # Não há parâmetros presentes
        p[0] = []  # Cria uma lista vazia para representar a ausência de parâmetros

# Exemplo de uso:
# FUNCAO soma(a, b, c), : a + b + c;
# FUNCAO identidade(x), : x;
# FUNCAO saudacao(), : "Olá!";


# Regra de produção para argumentos.
# Esta regra define a estrutura de argumentos, incluindo múltiplos, únicos e vazios.
def p_argumentos(p):
    '''argumentos : argumentos VIRGULA expressao
                  | expressao
                  | '''
    # Se houver múltiplos argumentos (argumentos, expressao)
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    # Se houver um único argumento (expressao)
    elif len(p) == 2:
        p[0] = [p[1]]
    # Se não houver argumentos (vazio)
    else:
        p[0] = []

# Exemplo de uso:
# soma(1, 2, 3)
# soma(1)
# soma()

# Regra de produção para uma expressão como uma instrução.
# Esta regra define expressões que terminam com ponto e vírgula como instruções.
def p_instrucao_expressao(p):
    '''instrucao : expressao PONTO_E_VIRGULA'''
    # p[1] : Expressão que termina com ponto e vírgula
    p[0] = p[1]  # Atribui a expressão como a instrução


# Regra de produção para a instrução ESCREVER.
# Esta regra define a instrução ESCREVER que imprime uma expressão.
def p_instrucao_escrever(p):
    '''instrucao : ESCREVER PARENTESES_ESQ expressao PARENTESES_DIR PONTO_E_VIRGULA'''
    # p[3] : Expressão a ser impressa
    p[0] = WriteNode(p[3])  # Cria um nó WriteNode com a expressão


# Regra de produção para uma instrução de atribuição.
# Esta regra define a estrutura para a atribuição de valores a variáveis.
def p_instrucao_atribuicao(p):
    '''instrucao : IDENTIFICADOR ATRIBUICAO expressao PONTO_E_VIRGULA'''
    # p[1] : Identificador (variável) à qual o valor será atribuído
    # p[3] : Expressão cujo valor será atribuído à variável
    p[0] = AssignNode(p[1], p[3])  # Cria um nó AssignNode com o identificador e a expressão


# Regra de produção para uma expressão binária.
# Esta regra define expressões binárias que utilizam operadores aritméticos, de concatenação e lógicos.
def p_expressao_binop(p):
    '''expressao : expressao OPERADOR_ARITMETICO expressao
                 | expressao OPERADOR_CONCAT expressao'''

    # Verifica que operador está presente na expressão e cria um nó BinOpNode correspondente.
    # O BinOpNode armazena o operador e as duas sub-expressões (operando esquerdo e direito).
    if p[2] in ['*', '/']:
        # Multiplicação e divisão têm maior precedência
        p[0] = BinOpNode(p[2], p[1], p[3])
    elif p[2] in ['+', '-']:
        # Adição e subtração têm menor precedência
        p[0] = BinOpNode(p[2], p[1], p[3])
    elif p[2] == '<>':
        # Concatenação
        p[0] = BinOpNode(p[2], p[1], p[3])



# Regra de produção para uma expressão agrupada.
# Esta regra define expressões que são agrupadas por parênteses.
def p_expressao_grupo(p):
    '''expressao : PARENTESES_ESQ expressao PARENTESES_DIR'''
    p[0] = p[2]


# Regra de produção para um número.
# Esta regra define a estrutura para representar números.
def p_expressao_numero(p):
    '''expressao : NUMERO'''
    # p[1] : Número identificado
    p[0] = NumberNode(p[1])  # Cria um nó NumberNode com o número encontrado


# Regra de produção para um identificador.
# Esta regra define a estrutura para representar identificadores (variáveis).
def p_expressao_identificador(p):
    '''expressao : IDENTIFICADOR'''
    # p[1] : Identificador (nome da variável)
    p[0] = IdentifierNode(p[1])  # Cria um nó IdentifierNode


# Regra de produção para uma string.
# Esta regra define a estrutura para representar strings.
def p_expressao_string(p):
    '''expressao : STRING'''
    # p[1] : O valor da string reconhecida pelo lexer.
    p[0] = StringNode(p[1])  # Cria um nó de string na AST com o valor da string.



# Regra de produção para uma string interpolada.
# Esta regra define a estrutura para representar strings interpoladas, que podem conter variáveis ou expressões.
def p_expressao_string_interpolada(p):
    '''expressao : INTERPOLATED_STRING'''

    def extrair_partes_interpoladas(string_interpolada):
        """Extrai as partes de uma string interpolada."""
        partes = []
        string_atual = ''
        i = 0
        while i < len(string_interpolada):
            # Verifica se encontrou uma expressão interpolada (#{...})
            if string_interpolada[i] == '#' and string_interpolada[i + 1] == '{':
                if string_atual:
                    partes.append(StringNode(string_atual))
                    string_atual = ''
                i += 2
                nome_variavel = ''
                # Extrai o nome da variável dentro da expressão interpolada
                while string_interpolada[i] != '}':
                    nome_variavel += string_interpolada[i]
                    i += 1
                partes.append(IdentifierNode(nome_variavel))
            else:
                string_atual += string_interpolada[i]
            i += 1
        if string_atual:
            partes.append(StringNode(string_atual))
        return partes

    partes = extrair_partes_interpoladas(p[1])
    p[0] = InterpolatedStringNode(partes)



# Regra de produção para a expressão de entrada.
# Esta regra define a estrutura para representar a entrada do user.
def p_expressao_entrada(p):
    '''expressao : ENTRADA PARENTESES_ESQ PARENTESES_DIR'''
    # Cria um nó InputNode na AST que representa a entrada (input)
    p[0] = InputNode()


# Regra de produção para a expressão de número aleatório.
# Esta regra define a estrutura para gerar números aleatórios dentro de um limite superior.
def p_expressao_aleatorio(p):
    '''expressao : ALEATORIO PARENTESES_ESQ expressao PARENTESES_DIR'''
    # Cria um nó RandomNode na AST que representa a geração de um número aleatório com limite superior p[3]
    p[0] = RandomNode(p[3])


# Função de tratamento de erros de sintaxe.
# Esta função é chamada quando ocorre um erro de sintaxe durante a análise.
def p_error(p):
    print(f"Erro de sintaxe: {p}")


# Regra de produção para uma lista de expressões.
# Esta regra define a estrutura para listas, que podem ser vazias ou conter múltiplas expressões.
def p_expressao_lista(p):
    '''expressao : COLCHETES_ESQ elementos_lista COLCHETES_DIR
                 | COLCHETES_ESQ COLCHETES_DIR'''
    if len(p) == 4:
        # Se a lista contiver elementos
        # p[2] contém a lista de elementos
        p[0] = ListNode(p[2])
    else:
        # Se a lista estiver vazia
        p[0] = ListNode([])


# Regra de produção para elementos de uma lista.
def p_elementos_lista(p):
    '''elementos_lista : elementos_lista VIRGULA expressao
                       | expressao'''
    if len(p) == 4:
        # Caso com múltiplos elementos
        # p[1] contém a lista de elementos acumulada até agora
        # p[3] contém a nova expressão encontrada após a vírgula
        p[0] = p[1] + [p[3]]  # Adiciona a nova expressão à lista acumulada
    else:
        # Caso com um único elemento
        # p[1] contém a única expressão na lista
        p[0] = [p[1]]  # Cria uma lista contendo a expressão


# Regra de produção para a expressão MAP.
def p_expressao_map(p):
    '''expressao : MAP PARENTESES_ESQ IDENTIFICADOR VIRGULA expressao PARENTESES_DIR'''
    # p[3] : identificador da função que será aplicada a cada elemento da lista
    # p[5] : expressão que representa a lista
    p[0] = MapNode(p[3], p[5])  # Cria um nó MapNode com a função e a lista


# Regra de produção para a expressão FOLD.
def p_expressao_fold(p):
    '''expressao : FOLD PARENTESES_ESQ IDENTIFICADOR VIRGULA expressao VIRGULA expressao PARENTESES_DIR'''
    # p[3] : identificador da função acumuladora
    # p[5] : expressão que representa o valor inicial
    # p[7] : expressão que representa a lista
    p[0] = FoldNode(p[3], p[5], p[7])  # Cria um nó FoldNode com a função, o valor inicial e a lista


# Regra de produção para um padrão de lista vazio.
def p_padroes_lista_vazia(p):
    '''padrao_lista : COLCHETES_ESQ COLCHETES_DIR'''
    # p[0]: Define um padrão de lista vazio com head e tail como None
    p[0] = ListPatternNode(None, None)

# Exemplo de uso:
# FUNCAO processar([]), : 0;


# Regra de produção para um padrão de lista com head e tail
def p_padrao_lista_cabeca_cauda(p):
    '''padrao_lista : IDENTIFICADOR DOIS_PONTOS IDENTIFICADOR'''
    # p[1]: Identificador representando a head\inicio da lista
    # p[3]: Identificador representando a tail\fim da lista
    p[0] = ListPatternNode(p[1], p[3])

# Exemplo de uso:
# FUNCAO somatorio(x:xs), : x + somatorio(xs);


# Inicializa o parser
parser = yacc.yacc()
