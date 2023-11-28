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

  OBS: Erros demonstrativos: Esse compilador adiciona "arrows", posicionamento dos erros erros personalizados para melhor visibilidade do usuário

  - Operações matemáticas respeitando a ordem de precedência: 
  ```bash
  1 + 1 = 2 -> Soma

  10 - 5 = 5 -> Subtração

  3 * 2 = 6 -> Multiplicação  

  5 / 2 = 2.5 -> Divisão

  2 * (2 + 3) = 10 -> Precedência de Parênteses

  10 / 0 -> Erro na execução: Divisão por zero 

  2 ^ 2 = 4 -> Potência

  -2 = -2 -> Número negativo

  --2 = 2 -> Negativos pares formam números positivos
  ```  

### Alunos:

- Geovanne Lopes - RA: 
- Guilherme Pereira - RA: 
- Lucas Zocca - RA: 
- Rebeca Pedroso - RA: