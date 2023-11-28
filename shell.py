import compilador

while True:
    text = input('compilador > ')
    resultado, error = compilador.run('<stdin>', text)

    if error:
        print(error.__str__())
    else:
        print(resultado)
