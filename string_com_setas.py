def string_com_setas(texto, pos_inicio, pos_fim):
    res = ''

    index_inicio = max(texto.rfind('\n', 0, pos_inicio.indice), 0)
    index_fim = texto.find('\n', index_inicio + 1)
    if index_fim < 0:
        index_fim = len(texto)

    contagem_de_linhas = pos_fim.linha - pos_inicio.linha + 1
    for i in range(contagem_de_linhas):
        line = texto[index_inicio:index_fim]
        col_inicio = pos_inicio.coluna if i == 0 else 0
        col_fim = pos_fim.coluna if i == contagem_de_linhas - 1 else len(line) - 1

        res += line + '\n'
        res += ' ' * col_inicio + '^' * (col_fim - col_inicio)

        index_inicio = index_fim
        index_fim = texto.find('\n', index_inicio + 1)
        if index_fim < 0:
            index_fim = len(texto)

    return res.replace('\t', '')
