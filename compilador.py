#######################################
# Erro
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
        return result


class CaractereInvalidoError(Error):
    def __init__(self, pos_inicio, pos_fim, detalhes):
        super().__init__(pos_inicio, pos_fim, 'Caractere Inválido', detalhes + '\n')

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

    def avanca(self, caractere_atual):
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


ML_INT = 'INTEIRO'
ML_FLOAT = 'FLUTUANTE'
ML_PLUS = 'SOMA'
ML_MINUS = 'SUBTRAI'
ML_MUL = 'MULTIPLICA'
ML_DIV = 'DIVIDE'
ML_LPAREN = 'ESQUERDA_PARENTESES'
ML_RPAREN = 'DIREITA_PARENTESES'


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# Analisador Léxico
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
                tokens.append(Token(ML_PLUS))
                self.avanca()
            elif self.caractere_atual == '-':
                tokens.append(Token(ML_MINUS))
                self.avanca()
            elif self.caractere_atual == '*':
                tokens.append(Token(ML_MUL))
                self.avanca()
            elif self.caractere_atual == '/':
                tokens.append(Token(ML_DIV))
                self.avanca()
            elif self.caractere_atual == '(':
                tokens.append(Token(ML_LPAREN))
                self.avanca()
            elif self.caractere_atual == ')':
                tokens.append(Token(ML_RPAREN))
                self.avanca()
            else:
                pos_inicio = self.pos.copia()
                caractere = self.caractere_atual
                self.avanca()
                return [], CaractereInvalidoError(pos_inicio, self.pos, "'" + caractere + "'")

        return tokens, None

    def cria_num(self):
        num_str = ''
        dot_count = 0

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
            return Token(ML_INT, int(num_str))
        else:
            return Token(ML_FLOAT, float(num_str))

#######################################
# Executa o código
#######################################


def executa(arquivo, texto):
    lexer = Lexer(arquivo, texto)
    tokens, error = lexer.cria_tokens()

    return tokens, error
