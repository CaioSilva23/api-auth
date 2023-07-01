# ARRAY
array = [3, 37, 33, 23, 13, 0, 49, 47, 34, 45, 5, 8, 23, 17, 36, 39, 21, 7, 26, 13]  # noqa: E501


# BUSCA LINEAR
# posicao_resultado = -1
# valor = int(input('Digite o valor a ser pesquisado:  '))
# for i, v in enumerate(array):
#     if v == valor:
#         posicao_resultado = i
#         break

# if posicao_resultado < 0:
#     print('Elemento não encontrado!')
# else:
#     print('Elemento encontrado na posição', posicao_resultado)
# # FIM BUSCA LINEAR

# SELECTION SORT
# print(array)
# tamanho = len(array)
# [5, 1, 6, 9, 15]
# for i in range(tamanho):  # começa com indice 0
#     indice_menor = i  # indice do primeiro valor
#     for j in range(i+1, tamanho):  # começa contar do indice 1
#         if array[j] < array[indice_menor]:
#             indice_menor = j
#     temp = array[indice_menor]  # armazena o menor valor
#     array[indice_menor] = array[i]  # troca
#     array[i] = temp  # troca
# print(array)
# FIM SELECTION SORT
