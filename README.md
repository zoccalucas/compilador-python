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

  - Erros demonstrativos: Adiciona setas de posicionamento e linha de ocorrência dos erros;
  - Manipulação Numérica: realiza a manipulação de números para reconhecer pontos flutuantes e inteiros e diferencia-los;
  - Precedência de Parênteses: identifica os parênteses em operações matemática, respeitando a ordem de precedência;
    ```bash
      2 * (2 + 3) = 10
    ```
  - Erros personalizados: 
    - Erro de caractére inválido;
    - Erro de sintaxe;
    - Erro de tempo de execução
  - Múltiplas variáveis: 
    ```bash
      VAR a = 5
      VAR b = VAR c = VAR d
      5 + (VAR x = 6)
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

### Alunos:

- Geovanne Lopes - RA: 
- Guilherme Pereira - RA: 
- Lucas Zocca - RA: 
- Rebeca Pedroso - RA: