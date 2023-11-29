import interpretador

while True:
    text = input('interpretador > ')
    result, error = interpretador.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)
