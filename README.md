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

## Suporte:
  - Erros demonstrativos: Adiciona setas de posicionamento, linha de ocorrência dos erros e mensagem com o erro;
  - Erros personalizados: 
    - Erro de caractére inválido:
    ```bash
        d
    ```
    - Erro de variável não definida:
    ```bash
        d
    ```
    - Erro de sintaxe:
    ```bash
        d
    ```
    - Erro de tempo de execução:
    ```bash
        d
    ```
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
  - Operações matemáticas: 
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
      5 == 5
      5 == 5 AND 6==5
      5 < 6
      5 > 6
    ```

### Alunos:

- Geovanne Lopes - RA: 
- Guilherme Pereira - RA: 
- Lucas Zocca - RA: 
- Rebeca Pedroso - RA: