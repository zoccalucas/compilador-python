#######################################
# Erro
#######################################

class Error:
    def __init__(self, nome_erro, detalhes):
        self.nome_erro = nome_erro
        self.detalhes = detalhes

    def __str__(self):
        return f'{self.nome_erro}: {self.detalhes}'


class CaractereInvalidoError(Error):
    def __init__(self, detalhes):
        super().__init__('Caractere Inválido', detalhes)

#######################################
# Constantes
#######################################


DIGITOS = '0123456789'

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
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.caractere_atual = None
        self.avanca()

    def avanca(self):
        self.pos += 1
        self.caractere_atual = self.text[self.pos] if self.pos < len(
            self.text) else None

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
                caractere = self.caractere_atual
                self.avanca()
                return [], CaractereInvalidoError("'" + caractere + "'")

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


def executa(text):
    lexer = Lexer(text)
    tokens, error = lexer.cria_tokens()

    return tokens, error
