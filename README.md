# Compilador

Compilador para matéria "Compiladores" da faculdade, contendo:

- Análise léxica;
- Análise sintática;
- Análise semântica;
- Geração de representação intermediária.

## Como executar:

-  Instale o [Python](https://www.python.org/)

-  Execute os comandos abaixo no terminal:

```bash
  #Clona o repositório
  $ git clone https://github.com/zoccalucas/compilador-python.git

  #Acessa o diretório do projeto
  $ cd compilador-python

  #Executa a aplicação
  $ python3 shell.py
```

<<<<<<< HEAD
### Alunos:

- Geovanne Lopes - RA: 
- Guilherme Pereira - RA: 
- Lucas Zocca - RA: 190907
- Rebeca Pedroso - RA: 
=======
## Suporte:
  - Erros demonstrativos: Adiciona setas de posicionamento, linha de ocorrência dos erros e mensagem com o erro;
  - Erros personalizados: 
    - Erro de caractére inválido:
    - Erro de variável não definida:
    - Erro de sintaxe:
    - Erro de tempo de execução:
  - Manipulação Numérica: realiza a manipulação de números para reconhecer pontos flutuantes e inteiros e diferencia-los;
    ```bash
        2.5
    ```
  - Precedência de Parênteses: identifica os parênteses em operações matemática, respeitando a ordem de precedência;
    ```bash
      2 * (2 + 3) = 10
    ```
  
  - Múltiplas variáveis: 
    ```bash
      VAR a = 5
      VAR b = VAR c = 5
      VAR b = VAR c = VAR d (Erro)
      5 + (VAR x = 6)
      5 + VAR x = 6 (Erro)
    ```

  - Soma
    ```bash
      1 + 1 
    ``` 
  - Subtração
    ```bash
      10 - 5
    ```
  - Multiplicação
    ```bash
      3 * 2 = 6
    ```
  - Divisão
    ```bash
      5 / 2
      5/0 (Erro)
      VAR a = 0
      10 / a (Erro)
    ```

  - Potência
    ```bash
      2 ^ 2
    ```

  - Números Negativos
    ```bash
      -2
      --2 (Negativos pares formam números positivos)
    ```
  - Operadores Lógicos 
    ```bash
      1 (Verdadeiro)
      0 (Falso)
      not 0
      not 1
      TRUE
      FALSE
    ```
  - Operadores de Comparação
    ```
    5 == 5
    5 == 5 AND 6==5
    5 < 6
    5 > 6
    ```
  - Estrutura condicional 
    ```
    VAR preco = 100
    VAR compra = IF 5 < 200 THEN 1 ELSE 0
    IF (5 < 200) THEN 1 ELSE 0
    IF 5 == 5 THEN 123 ELSE 234
    VAR result = IF 5 == 5 THEN "Funcionou" ELSE "Não"
    ```

  - Estrutura de repetição
    ```
    VAR result = 1
    FOR i = 1 TO 6 THEN VAR result = result * i
    result
    WHILE TRUE THEN 123 
    VAR i = 0
    WHILE i < 5 THEN VAR i = i + 1
    ```

  - Funções
    ```
    FUN soma (a, b) -> a + b
    soma(5, 2)   
    ```

  - Strings
    ```
    "Texto" 
    "Texto " + "Texto2"
    "Texto " * 3
    ```

  - Listas
    ```
    [1, 2] + 4
    [1, 2] - 1 (Remove o elemento do index 1)
    [1, 2, 3] - -1 (Remove o elemento do último índice)
    [1, 2] - 3 (Erro de index)
    [1, 2] / 0 (Retorno de index)
    [1, 2, 3] / -1
    [1, 2, 3] * [9, 8, 7] (Concatena listas)
    FOR i = 1 TO 9 THEN 2 ^ 2
    ```

  - Funções 
    ```
    MATH_PI
    PRINT("Hello, World!")
    VAR nome = INPUT()
    VAR idade = INPUT_INT()
    IS_NUM(123)
    IS_STR("oi")
    IS_LIST([])
    S_FUN(PRINT)
    VAR list = [1, 2, 3]
    APPEND(list, 4)
    POP(list,3)
    ```

### Alunos:

Geovanne Lopes - 190803
Guilherme Pereira da Silva - 190570
Lucas Henrique Zocca Soares - 190907
Rebeca Pedroso Silva - 190664
>>>>>>> 7db48f72e23a31a0175faba56ecee21e33561e8c
