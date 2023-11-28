#######################################
# Imports
#######################################

from string_com_setas import string_com_setas


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
    def __init__(self, pos_inicio, pos_fim, detalhes):
        super().__init__(pos_inicio, pos_fim, 'Sintáxe Inválida', detalhes + '\n')


class RuntimeError(Error):
    def __init__(self, pos_inicio, pos_fim, detalhes, context):
        super().__init__(pos_inicio, pos_fim, 'Erro na execução', detalhes + '\n')
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.nome_erro}: {self.detalhes}'
        result += '\n\n' + \
            string_com_setas(self.pos_inicio.texto,
                             self.pos_inicio, self.pos_fim)
        return result

    def generate_traceback(self):
        resultado = ''
        pos = self.pos_inicio
        ctx = self.context

        while ctx:
            resultado = f'  Arquivo {pos.arquivo}, line {str(pos.linha + 1)}, in {ctx.display_name}\n' + resultado
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

            return 'Traceback (most recent call last):\n' + resultado

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
ML_POW = 'POTE'


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
            elif self.caractere_atual == '^':
                tokens.append(Token(ML_POW, pos_inicio=self.pos))
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

        self.pos_inicio = self.token.pos_inicio
        self.pos_fim = self.token.pos_fim

    def __repr__(self):
        return f'{self.token}'


class BinOpNode:
    def __init__(self, esquerda, op_token, direita):
        self.esquerda = esquerda
        self.op_token = op_token
        self.direita = direita

        self.pos_inicio = self.esquerda.pos_inicio
        self.pos_fim = self.direita.pos_fim

    def __repr__(self):
        return f'({self.esquerda}, {self.op_token}, {self.direita})'


class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

        self.pos_inicio = self.op_token.pos_inicio
        self.pos_fim = self.op_token.pos_fim

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

    def atom(self):
        res = ParseResult()
        token = self.token_atual

        if token.type in (ML_INT, ML_FLOAT):
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
            "Expected int, float, '+', '-' or '('"
        ))

    def power(self):
        return self.bin_op(self.atom, (ML_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        token = self.token_atual

        if token.type in (ML_PLUS, ML_MINUS):
            res.registro(self.avanca())
            factor = res.registro(self.factor())
            if res.error:
                return res
            return res.sucesso(UnaryOpNode(token, factor))
        
        return self.power()

    def term(self):
        return self.bin_op(self.factor, (ML_MUL, ML_DIV))

    def expr(self):
        return self.bin_op(self.term, (ML_PLUS, ML_MINUS))

    #######################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        esquerda = res.registro(func_a())
        if res.error:
            return res

        while self.token_atual.type in ops:
            op_token = self.token_atual
            res.registro(self.avanca())
            direita = res.registro(func_b())
            if res.error:
                return res
            esquerda = BinOpNode(esquerda, op_token, direita)

        return res.sucesso(esquerda)


#######################################
# Runtime Result
#######################################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def registro(self, res):
        if res.error:
            self.error = res.error
        return res.value

    def sucesso(self, value):
        self.value = value
        return self

    def falha(self, error):
        self.error = error
        return self


#######################################
# Valores
#######################################

class Numero:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_inicio=None, pos_fim=None):
        self.pos_inicio = pos_inicio
        self.pos_fim = pos_fim
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Numero):
            return Numero(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Numero):
            if other.value == 0:
                return None, RuntimeError(
                    other.pos_inicio, other.pos_fim,
                    'Divisão por zero',
                    self.context
                )

            return Numero(self.value / other.value).set_context(self.context), None

    def powed_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value ** other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)


#######################################
# Contexto
#######################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos


#######################################
# Interpretador
#######################################


class Interpretador:
    def visita(self, node, context):
        metodo_nome = f'visit_{type(node).__name__}'
        metodo = getattr(self, metodo_nome, self.no_visit_method)
        return metodo(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'visit_{type(node).__name__} método indefinido')

    def visit_NumberNode(self, node, context):
        return RTResult().sucesso(
            Numero(node.token.value).set_context(
                context).set_pos(node.pos_inicio, node.pos_fim)
        )

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        esquerda = res.registro(self.visita(node.esquerda, context))
        if res.error:
            return res
        direita = res.registro(self.visita(node.direita, context))
        if res.error:
            return res

        if node.op_token.type == ML_PLUS:
            resultado, error = esquerda.added_to(direita)
        elif node.op_token.type == ML_MINUS:
            resultado, error = esquerda.subbed_by(direita)
        elif node.op_token.type == ML_MUL:
            resultado, error = esquerda.multed_by(direita)
        elif node.op_token.type == ML_DIV:
            resultado, error = esquerda.dived_by(direita)
        elif node.op_token.type == ML_POW:
            resultado, error = esquerda.powed_by(direita)

        if error:
            return res.falha(error)
        else:
            return res.sucesso(resultado.set_pos(node.pos_inicio, node.pos_fim))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        numero = res.registro(self.visita(node.node, context))
        if res.error:
            return res

        error = None

        if node.op_token.type == ML_MINUS:
            numero = numero.multed_by(Numero(-1))

        if error:
            return res.falha(error)
        else:
            return res.sucesso(numero.set_pos(node.pos_inicio, node.pos_fim))

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
    if arvore_sintatica.error:
        return None, arvore_sintatica.error

    # Roda o programa
    interpretador = Interpretador()
    contexto = Context('<program>')
    resultado = interpretador.visita(arvore_sintatica.node, contexto)

    return resultado.value, resultado.error
