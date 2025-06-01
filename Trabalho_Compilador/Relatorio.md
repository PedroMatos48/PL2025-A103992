# Projeto de Processamento de Linguagens
2025-06-01 João Brito, Tomás Oliveira, Pedro Matos

## Introdução

O objetivo deste projeto é desenvolver um compilador Pascal standard em Python. Fomos encarregados de implementar o analisador léxico e sintático, além de verificar a semântica, gerar o código (e opcionalmente otimizá-lo) e validar o seu resultado de execução. Na geração de código, optamos por gerar uma representação intermédia do programa para depois gerar o código da máquina virtual numa travessia sobre essa representação.

Neste relatório, descreveremos o processo de implementação e as decisões tomadas no projeto. 

## Análise Léxica

Para a análise léxica, como pedido, utilizamos a ferramenta "ply.lex". Definimos uma série de tokens que condizem com as construções Pascal, bem como as expressões regulares que permitem a sua identificação.

- Palavras-chave: `program`, `var`, `begin`, `end`, `if`, `then`, `else`, `for`, `while`, etc.
- Operadores: `+`, `-`, `*`, `/`, `div`, `mod`, lógicos (`and`, `or`, `not`), relacionais (`=`, `<>`, `<`, `<=`, `>`, `>=`)
- Pontuação: `;`, `:`, `.`, `,`, `()`, `[]`
- Tipos: `integer`, `real`, `boolean`, `char`, `string` (identificam variáveis de acordo com o seu tipo)
- Funções: `write`, `writeln`, `read`, `readln`, `length`
- Literais: `TINTEGER`, `TREAL`, `TBOOLEAN`, `TCHAR`, `TSTRING` (identificam as declarações de tipos)

Como o Pascal é uma linguagem _case-insensitive_, utilizamos a flag `IGNORECASE` do módulo "re", permitindo a identificação independente de maiúsculas e minúsculas. Além disso, ignoramos os comentários através do token `COMMENT`. 

Usamos regras de regex para distinguir entre carácteres singulares e strings.  Para garantir que um caractere individual fosse reconhecido corretamente como char e não confundido com uma string, definimos a regra de char antes da regra de string, assegurando assim a sua prioridade na análise léxica.

Devido a dificuldades na implementação, optamos por não incluir as funcionalidades opcionais de `function` e `procedure`, pelo que não possuem tokens correspondentes.

## Análise Sintática

A análise sintática é realizada através do "ply.yacc". Estruturamos portanto uma gramática que consegue representar a estrutura de blocos da linguagem Pascal, começando com a declaração `program`, passando pelas declarações de variáveis e finalmente o bloco `begin ... end.`. 

Tratamos as regras de forma a incluir atribuições de variáveis, loops (`if`, `for`, `while`), operações de input e output e expressões (operações binárias, comparações, etc.), além de declarações de arrays e suporte para os tipos standard em Pascal (e.g. integer, real, boolean). Utilizamos uma hierarquia de precedência para garantir que as expressões são lidas na ordem correta, evitando conflitos de _shift/reduce_. Por exemplo, as operações de multiplicação tem precedência à esquerda. 

Implementamos regras recursivas para as sequências de instruções, através das regras de produção de `statement_seq`, lidando assim com as estruturas aninhadas. Particularmente, lidamos então com blocos de `begin ... end` e ramos opcionais `else`, com cuidado de prevenir conflitos _reduce/reduce_ em casos de `if ... then ... else`. No entanto, esses casos em específico apresentam o único conflito de _shift/reduce_ na nossa solução, resultando do _dangling else problem_ em que um `else` após dois `if`_statements_ causa ambiguidade. Utilizamos a precedência "nonassoc" para `else`, instruindo o _parser_ a preferir _shift_ quando esse caso ocorre (dando prioridade ao `if` "de dentro"). 

Decidimos realizar uma representação intermédia do código antes de convertê-lo para código máquina. Assim, cada regra de produção constrói uma representação em Abstract Syntax Tree (AST) do código Pascal, que é submetida à análise semântica e posteriormente utilizada para a geração de código suportado pela EWVM. 

Por fim, apresentamos a gramática desenvolvida para esta solução, em formato BNF:

```
start          → PROGRAM identifier ';' main '.'`

main           → const_list var_list statement_list

const_list     → CONST const_decls
               | ε

const_decls    → const_decls const_decl
               | const_decl

const_decl     → identifier '=' INTEGER ';'
               | identifier '=' STRING ';'
               | identifier '=' REAL ';'
               | identifier '=' BOOLEAN ';

var_list       → VAR var_decls
               | ε

var_decls      → var_decls var_decl
               | var_decl

var_decl       → ident_list ':' type_decl ';'

ident_list     → identifier ',' ident_list
               | identifier

type_decl      → ARRAY '[' INTEGER '..' INTEGER ']' OF type
               | ARRAY '[' identifier '..' identifier ']' OF type
               | ARRAY '[' INTEGER '..' identifier ']' OF type
               | ARRAY '[' identifier '..' INTEGER ']' OF type
               | type

type           → IDENTIFIER | TREAL | TINTEGER | TSTRING | TCHAR | TBOOLEAN

identifier     → IDENTIFIER '[' expression ']'
               | IDENTIFIER

statement_list → BEGIN statement_seq END

statement_seq  → statement_seq ';' statement
               | statement_seq ';'
               | statement

statement      → writeln
               | write
               | readln
               | read
               | assign
               | if_stmt
               | for_loop
               | while_loop
               | statement_list

assign         → identifier ASSIGN expression

if_stmt        → IF expression THEN statement
               | IF expression THEN statement ELSE statement

for_loop       → FOR identifier ASSIGN expression TO expression DO statement
               | FOR identifier ASSIGN expression DOWNTO expression DO statement

while_loop     → WHILE expression DO statement

writeln        → WRITELN '(' phrase ')'
               | WRITELN

write          → WRITE '(' phrase ')'

readln         → READLN '(' identifier ')'
               | READLN

read           → READ '(' identifier ')'

phrase         → phrase_list

phrase_list    → phrase_list ',' phrase_item
               | phrase_item

phrase_item    → STRING | CHAR | identifier | INTEGER | REAL

length         → LENGTH '(' identifier ')'

expression     → expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
               | expression DIV expression
               | expression MOD expression
               | expression '=' expression
               | expression '<>' expression
               | expression '<' expression
               | expression '>' expression
               | expression '<=' expression
               | expression '>=' expression
               | expression AND expression
               | expression OR expression
               | NOT expression
               | '(' expression ')'
               | length
               | identifier
               | INTEGER | REAL | CHAR | STRING | BOOLEAN
```

## Análise Semântica

Durante a análise semântica, o nosso interpretador realiza uma série de validações para garantir a integridade e a coerência das instruções enquanto gera o código. Nós verificamos cada uma através de condições resultando em exceções se existir erros na lógica do código.

A seguir, estão os principais tipos de erros detectados:

Declaração de Constantes:

- Identificação de múltiplas declarações com o mesmo identificador, evitando redefinições.

- Verificação para evitar definições de constantes dependentes de variáveis.

- Verificação para evitar atribuições de valores a constantes após a definição inicial.

Declaração de Variáveis:

- Verificação para evitar declarações duplicadas de variáveis.

Validação específica para arrays:

- Garantia de que os limites (índices) sejam constantes válidas e do tipo inteiro.

- Confirmação de que os limites estejam em ordem lógica (início ≤ fim).

- Validação do tipo base do array para assegurar compatibilidade.

Atribuições:

- Garantia de que a variável ou array de destino esteja previamente declarado.

- Bloqueio da atribuição a constantes.

- Verificação da compatibilidade de tipos entre a variável destino e o valor atribuído.

Expressões:

- Validação dos índices utilizados para acesso a arrays.

- Verificação da compatibilidade de tipos entre as 2 variáveis.

## Geração de Código

Para fazer a geração do código que é utilizado na máquina virtual disponibilizada pelos docentes, temos o ficheiro `ASTInterpreter.py` que tal como o nome implica, traz a árvore AST gerada com o yacc e transforma esta em comandos válidos para a VM.

Cada variável requer que sejam guardadas diferentes informações e por isso definimos a classe VarInfo que define as informações de cada variável, como tipo, posição na memória, tamanho (em caso de arrays), e se é um array ou não.

Dividimos os diferentes tipos de ações possiveís nos seguintes métodos:

- interpret(self, node): Este é o ponto de entrada para interpretar a AST. Espera um nó com a estrutura ('program', ('MAIN', vars, statements)).

- _handle_commands(self, node): Esta função recebe o primeiro elemento do nodo da árvore AST que normalmente é algo do estilo IF, FOR, READ, WRITE, etc. e chama a função correta para lidar com a informação no resto do nodo.

- _handle_read(self, node) e _handle_readln(self,node): Estes dois métodos servem para interpretar o input do utilizador através do comando READ, mas também cuidam de algum parsing básico da informação obtida através de comandos como ATOI e ATOF se forem necessários. Finalmente, guarda os dados obtidos com STOREG ou STOREN.

- _handle_vars(self, node): Processa a declaração de variáveis e arrays, e gera instruções para alocar memória.

- _eval_expr(self, expr): Avalia expressões (como aritméticas, booleanas e de acesso a arrays) e gera as instruções correspondentes.

    Trata de diferentes tipos de expressões:
    
    1. Constantes literais:
        
        Strings: "abc" → gera PUSHS "abc"
        
        Caracteres únicos: 'a' → gera PUSHS "a" seguido por CHRCODE
        
        Números inteiros: 42 → gera PUSHI 42
        
        Booleanos: true / false → gera PUSHI 1 ou PUSHI 0

    2. Variáveis simples:
        
        x → gera PUSHG <posição> (carrega o valor da memória global)
            
    3. Acesso a arrays e strings:
        
        Calcula o índice correto considerando o deslocamento (begin do VarInfo)
        
        Gera instruções como PUSHG, ADD, LOADN (ou CHARAT no caso de strings)

    4. Expressões compostas (operações aritméticas e lógicas):
        
        Exemplo: ('ADD', 'x', 'y') → traduz para:
        ```
        PUSHG x
        
        PUSHG y
        
        ADD
        ```
        
        Operadores suportados: ADD, SUB, MUL, DIV, MOD, AND, OR, =, <>, <, >, <=, >=, NOT, LENGTH

- _handle_assign, _handle_if, _handle_while, _handle_for, etc.: Implementam o comportamento de estruturas de controlo e comandos da linguagem.
            
    1. _handle_assign(self, node) (responsável por atribuições)
        
        Armazena o valor da variável ou posição de array através de comandos como STOREG ou STOREN.

    2. _handle_if(self, node):
        
        Avalia a condição de um if e gera saltos condicionais (JZ, JUMP) e rótulos como L1ELSE, L1END para criar uma lógica que simula o efeito de um if else em Pascal.

    3. _handle_while(self, node):
        
        Cria uma label de início e fim (L2START, L2END) para funcionar como o `begin` e `end` de pascal. 
        
        Depois avalia a condição e executa o corpo enquanto for verdadeira e utiliza JZ, JUMP, etc. para fazer os ciclos rodarem o código de novo.
            
    
    4. _handle_for(self, node) e _handle_for_downto(self, node) - (Traduzem a lógica de um for ... to ... e for ... downto ...)
        
        Cria uma label de início e fim (L2FOR, L2ENDFOR) para funcionar como o `begin` e `end` de pascal. 
        
        Avalia limites de início e fim e gera verificação com INFEQ (para `to`) ou SUPEQ (para `downto`)
        
        Incrementa ou decrementa com ADD / SUB para percorrer o `for`.

- _handle_write e _handle_writeln: Estes dois métodos tratam de imprimir o que lhe é pedido no terminal através dos comandos WRITEI, WRITEF, WRITES e WRITELN dependendo do caso de ser um int, float, string ou o fim de um comando writeln.

- _handle_const: Processa a criação das variáveis constantes. Elas são guardadas na lista de variáveis vars junto com o seu valor, e sempre que chamadas são colocadas diretamente na VM. Assim evita-se o perigo de guardar um apontador que poderá ser modificado.

## Testes

O programa neste momento devolve a árvore AST gerada e os comandos que são utilizados na VM. Guardamos os diferentes resultados obtidos por exemplos de programas na pasta src/testResults.

## Avaliação de Desempenho e Conclusão

O nosso compilador atende aos principais critérios de avaliação definidos para o projeto. Em termos de correção, ele é capaz de processar e interpretar corretamente programas escritos em Pascal standard, analisando a estrutura sintática e gerando o código intermediário esperado.

No que diz respeito à funcionalidade, o compilador oferece suporte a diversas construções essenciais da linguagem, como declarações de variáveis, operações aritméticas e booleanas, controle de fluxo com estruturas como if, while, for e for downto, além de comandos de entrada/saída como read, readln, write e writeln. Apesar disso, não implementamos as funcionalidades de function e procedure.

Por fim, fizemos uma série de testes de desempenho do compilador. Usamos uma script para avalia-los 3 vezes e fazer uma média de cada um dos exemplos. Abaixo mostramos os resultados do tempo médio de compilação do código e a memória utilizada no processo, compilando os mesmos casos de teste com a nossa solução e com o Free Pascal Compiler:

Tabela com valores de desempenho do nosso compilador:

| Exemplo | Tempo Médio | Utilização de Memória | 
| ------- | ----------- | --------------------- |
| 1  | 1ms|1 KB
| 2 | 1ms | 13 KB
| 3  | 1ms | 20 KB
| 8 | 1ms | 20 KB
| 9  | 1ms | 40 KB
| 10 | 1,2ms | 1,3 KB
 
Tabela com valores de desempenho do compilador FPC (Free Pascal Compiler):

| Exemplo | Tempo Médio | Utilização de Memória | 
| ------- | ----------- | --------------------- |
| 1  |  39,8ms  | 5893 KB        
| 2 |   37,1ms  | 5889 KB
| 3  |  37,2ms  | 5891 KB
| 8 | 35,4ms | 5892 KB
| 9  | 35,1ms | 5889 KB
| 10 | 37,1ms | 5888 KB

Podemos ver que os valores, tanto para o tempo médio de compilação quanto para a memória utilizada, são mais baixos no nosso compilador. Acreditamos que tal resulta do FPC compilar para assembly diretamente, conter maiores otimizações e maior número de verificações semânticas, e ter suporte para a totalidade das funcionalidades em Pascal, como _functions_, _procedures_, apontadores, etc.
 