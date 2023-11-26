import compilador

while True:
    text = input('compilador > ')
    resultado, error = compilador.executa(text)

    if error:
        print(error.__str__())
    else:
        print(resultado)
