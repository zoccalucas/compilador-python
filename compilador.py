#######################################
# Imports
#######################################

from string_com_setas import *


#######################################
# Erros
#######################################


class Error:
    def __init__(self, pos_inicio, pos_fim, nome_erro, detalhes):
        self.pos_inicio = pos_inicio
        self.pos_fim = pos_fim
        self.nome_erro = nome_erro
        self.detalhes = detalhes

    def __str__(self):
        result = f'{self.nome_erro}: {self.detalhes}'
        result += f'Arquivo {self.pos_inicio.arquivo}, linha {self.pos_inicio.linha + 1}'
        result += '\n\n' + string_com_setas(
            self.pos_inicio.texto, self.pos_inicio, self.pos_fim)
        return result


class CaractereInvalidoError(Error):
    def __init__(self, pos_inicio, pos_fim, detalhes):
        super().__init__(pos_inicio, pos_fim, 'Caractere Inválido', detalhes + '\n')


class SintaxeInvalidaError(Error):
    def __init__(self, pos_inicio, pos_fim, detalhes=''):
        super().__init__(pos_inicio, pos_fim, 'Sintáxe Inválida', detalhes + '\n')

#######################################
# Constantes
#######################################


DIGITOS = '0123456789'


#######################################
# Posições
#######################################

class Posicao:
    def __init__(self, indice, linha, coluna, arquivo, texto):
        self.indice = indice
        self.linha = linha
        self.coluna = coluna
        self.arquivo = arquivo
        self.texto = texto

    def avanca(self, caractere_atual=None):
        self.indice += 1
        self.coluna += 1

        if caractere_atual == '\n':
            self.linha += 1
            self.coluna = 0

        return self

    def copia(self):
        return Posicao(self.indice, self.linha, self.coluna, self.arquivo, self.texto)

#######################################
# Tokens
#######################################


ML_INT = 'INTE'
ML_FLOAT = 'FLUT'
ML_PLUS = 'SOMA'
ML_MINUS = 'SUBT'
ML_MUL = 'MULT'
ML_DIV = 'DIVI'
ML_LPAREN = 'ESQD_PAREN'
ML_RPAREN = 'DIRT_PAREN'
ML_EOF = 'EOF'


class Token:
    def __init__(self, type, value=None, pos_inicio=None, pos_fim=None):
        self.type = type
        self.value = value

        if pos_inicio:
            self.pos_inicio = pos_inicio.copia()
            self.pos_fim = pos_inicio.copia()
            self.pos_fim.avanca()

        if pos_fim:
            self.pos_fim = pos_fim

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# Lexer - Analisador Léxico
#######################################


class Lexer:
    def __init__(self, arquivo, texto):
        self.arquivo = arquivo
        self.texto = texto
        self.pos = Posicao(-1, 0, -1, arquivo, texto)
        self.caractere_atual = None
        self.avanca()

    def avanca(self):
        self.pos.avanca(self.caractere_atual)
        self.caractere_atual = self.texto[self.pos.indice] if self.pos.indice < len(
            self.texto) else None

    def cria_tokens(self):
        tokens = []

        while self.caractere_atual != None:
            if self.caractere_atual in ' \t':
                self.avanca()
            elif self.caractere_atual in DIGITOS:
                tokens.append(self.cria_num())
            elif self.caractere_atual == '+':
                tokens.append(Token(ML_PLUS, pos_inicio=self.pos))
                self.avanca()
            elif self.caractere_atual == '-':
                tokens.append(Token(ML_MINUS, pos_inicio=self.pos))
                self.avanca()
            elif self.caractere_atual == '*':
                tokens.append(Token(ML_MUL, pos_inicio=self.pos))
                self.avanca()
            elif self.caractere_atual == '/':
                tokens.append(Token(ML_DIV, pos_inicio=self.pos))
                self.avanca()
            elif self.caractere_atual == '(':
                tokens.append(Token(ML_LPAREN, pos_inicio=self.pos))
                self.avanca()
            elif self.caractere_atual == ')':
                tokens.append(Token(ML_RPAREN, pos_inicio=self.pos))
                self.avanca()
            else:
                pos_inicio = self.pos.copia()
                caractere = self.caractere_atual
                self.avanca()
                return [], CaractereInvalidoError(pos_inicio, self.pos, "'" + caractere + "'")

        tokens.append(Token(ML_EOF, pos_inicio=self.pos))
        return tokens, None

    def cria_num(self):
        num_str = ''
        dot_count = 0
        pos_inicio = self.pos.copia()

        while self.caractere_atual != None and self.caractere_atual in DIGITOS + '.':
            if self.caractere_atual == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.caractere_atual
            self.avanca()

        if dot_count == 0:
            return Token(ML_INT, int(num_str), pos_inicio, self.pos)
        else:
            return Token(ML_FLOAT, float(num_str), pos_inicio, self.pos)

#######################################
# Nós
#######################################


class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'


class BinOpNode:
    def __init__(self, esquerda, op_token, direita):
        self.esquerda = esquerda
        self.op_token = op_token
        self.direita = direita

    def __repr__(self):
        return f'({self.esquerda}, {self.op_token}, {self.direita})'


class UnOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'({self.op_token}, {self.node})'


#######################################
# Resultado do Analisador Sintático
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def registro(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

        return res

    def sucesso(self, node):
        self.node = node
        return self

    def falha(self, error):
        self.error = error
        return self


#######################################
# Parser - Analisador Sintático
#######################################


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_indice = -1
        self.avanca()

    def avanca(self):
        self.token_indice += 1
        if self.token_indice < len(self.tokens):
            self.token_atual = self.tokens[self.token_indice]
        return self.token_atual

    def parse(self):
        res = self.expr()
        if not res.error and self.token_atual.type != ML_EOF:
            return res.falha(SintaxeInvalidaError(
                self.token_atual.pos_inicio, self.token_atual.pos_fim,
                "Esperado '+', '-', '*' ou '/'"
            ))
        return res

    #######################################

    def factor(self):
        res = ParseResult()
        token = self.token_atual

        if token.type in (ML_PLUS, ML_MINUS):
            res.registro(self.avanca())
            factor = res.registro(self.factor())
            if res.error:
                return res
            return res.sucesso(UnOpNode(token, factor))

        elif token.type in (ML_INT, ML_FLOAT):
            res.registro(self.avanca())
            return res.sucesso(NumberNode(token))
        
        elif token.type == ML_LPAREN:
            res.registro(self.avanca())
            expr = res.registro(self.expr())
            if res.error:
                return res
            if self.token_atual.type == ML_RPAREN:
                res.registro(self.avanca())
                return res.sucesso(expr)
            else:
                return res.falha(SintaxeInvalidaError(
                    self.token_atual.pos_inicio, self.token_atual.pos_fim,
                    "Esperado ')'"
                ))

        return res.falha(SintaxeInvalidaError(
            token.pos_inicio, token.pos_fim,
            "Número inteiro ou decimal esperado"
        ))

    def term(self):
        return self.bin_op(self.factor, (ML_MUL, ML_DIV))

    def expr(self):
        return self.bin_op(self.term, (ML_PLUS, ML_MINUS))

    #######################################

    def bin_op(self, func, ops):
        res = ParseResult()
        esquerda = res.registro(func())
        if res.error:
            return res

        while self.token_atual.type in ops:
            op_token = self.token_atual
            res.registro(self.avanca())
            direita = res.registro(func())
            if res.error:
                return res
            esquerda = BinOpNode(esquerda, op_token, direita)

        return res.sucesso(esquerda)


#######################################
# Executa o código
#######################################


def executa(arquivo, texto):
    # Gera de Tokens
    lexer = Lexer(arquivo, texto)
    tokens, error = lexer.cria_tokens()
    if error:
        return None, error

    # Gera Árvore Sintática Abstrata
    parser = Parser(tokens)
    arvore_sintatica = parser.parse()

    return arvore_sintatica.node, arvore_sintatica.error
