# Projeto: Interpretador e Gerador de Código C para a Linguagem FCA
### Visão Geral

Este projeto consiste num interpretador e gerador de código C para uma linguagem de programação FCA. O sistema lê código escrito em FCA, interpreta e executa esse código, e também gera código C equivalente.

### Estrutura do Projeto

    Lexer: Responsável por analisar o texto de entrada e transformá-lo em tokens.
    Parser: Constrói a árvore de sintaxe abstrata (AST) a partir dos tokens gerados pelo lexer.
    AST Nodes: Define as classes de nós da AST, representando as diferentes construções sintáticas da linguagem FCA.
    Interpreter: Interpreta e executa a AST.
    Code Generator: Gera código C a partir da AST.
    Main: Ponto de entrada do programa, que coordena o fluxo entre lexer, parser, interpretador e gerador de código.

### Requisitos

Bibliotecas externas:
- PLY (Python Lex-Yacc)

### Instalação

Clonar o repositório:

```bash
git clone https://github.com/zorkpt/FCA-Compiler.git
cd FCA-Compiler
```

### Criar um ambiente virtual e instalar as dependências:

```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
```

### Uso

1. Escrever código FCA num ficheiro de texto, por exemplo, exemplo.fca:
    
```fca
FUNCAO soma(x, y), : x + y ;
resultado = soma(2, 3);
ESCREVER(resultado);
```

2. Execute o interpretador e gerador de código C com o arquivo de código FCA:

```bash
    python main.py exemplo.fca
```

3. Output:

        A interpretação do código será mostrada na consola.
        O código C gerado é guardado em output.c.

### Exemplo de ficheiro exemplo.fca

```fca
FUNCAO fib(0), : 0 ;
FUNCAO fib(1), : 1 ;
FUNCAO fib(n):
    a = fib(n-1);
    b = fib(n-2);
    a + b;
FIM
fib5 = fib(5);
ESCREVER(fib5);
```

### Testes

No diretório exemplos/, há vários exemplos de ficheiros .fca que podem ser usados para testar o interpretador e o gerador de código C.

### Testes Automatizados

Há também um script tests.py que executa todos os arquivos .fca no diretório exemplos/ e guarda os resultados no diretório outputs/. Para correr os testes, usar:

```bash
python tests.py
```