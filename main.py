import numpy as np

def juego(tablero):
    # Validar caso matriz nula
    if matrizNula(tablero) is True:
        return 'La matriz, es una matriz nula, por lo que ya están todas las luces apagadas.'
    
    # Validar matriz cuadrada
    tamano_tablero = np.shape(tablero)
    if tamano_tablero[0] != tamano_tablero[1]:
        return 'La matriz no es cuadrada.'

    # Se crean las ecuaciones, serán tuplas que en la primer entrada tienen las incógnitas y en el segundo el valor de cada posición del tablero inicial.
    ecuaciones: [([int], int)] = [() for i in range(tamano_tablero[0] ** 2)]

    # Generar las ecuaciones
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            adyacentes = obtenerIndicesAdyancetes(len(tablero), len(tablero[0]), i, j)
            ecuacion: [int] = [0 for i in range(tamano_tablero[0] ** 2)]
            indice_ecuacion: int = indiceVector(len(tablero), i, j)
            ecuacion[indice_ecuacion] = 1
            for row, column in adyacentes:
                indice_elem = indiceVector(tamano_tablero[0], row, column)
                ecuacion[indice_elem] = 1

            luz = tablero[i][j]
            ecuaciones[indice_ecuacion] = (ecuacion, luz)

    lista_ecuaciones = []
    luces = []
    for i in range(len(ecuaciones)):
        eq, val = ecuaciones[i]
        lista_ecuaciones.append(eq)
        luces.append([val])

    A = np.array(lista_ecuaciones)
    b = np.array(luces)
    matrizAmpliada = np.concatenate((A, b), axis=1)
    
    # Devolvemos la solución de esta matriz ampliada calculada con el método de Gauss.
    return metodoGauss(matrizAmpliada)


def obtenerIndicesAdyancetes(filas: int, columnas: int, indice_fila_elem: int, indice_columna_elem: int):
    if (0 > indice_fila_elem > filas - 1) and (0 > indice_columna_elem > columnas - 1):
        return None

    if indice_fila_elem == 0 or indice_fila_elem == filas - 1:
        if indice_columna_elem == 0 or indice_columna_elem == columnas - 1:
            cant_adyacentes = 2
        else:
            cant_adyacentes = 3
    else:
        if indice_columna_elem == 0 or indice_columna_elem == columnas - 1:
            cant_adyacentes = 3
        else:
            cant_adyacentes = 4

    adyacente_posicion: [[int]] = [[0, 0] for i in range(cant_adyacentes)]
    indice_posicion: int = 0
    
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for direction in direcciones:
        i, j = direction
        if 0 <= indice_fila_elem + i < filas and 0 <= indice_columna_elem + j < columnas:
            adyacente_posicion[indice_posicion][0] = indice_fila_elem + i
            adyacente_posicion[indice_posicion][1] = indice_columna_elem + j
            indice_posicion += 1

    return adyacente_posicion


def metodoGauss(matriz):
    tamano = np.shape(matriz)[0]

    for i in range(tamano):
        pivot_fila = -1
        for j in range(i, tamano):
            if matriz[j, i] == 1:
                pivot_fila = j
                break

        if pivot_fila == -1:
            continue
        if pivot_fila != i:
            matriz[[pivot_fila, i]] = matriz[[i, pivot_fila]]

        for j in range(tamano):
            if j != i and matriz[j, i] == 1:
                matriz[j] = matriz[j] ^ matriz[i]

    x = np.zeros(tamano, dtype=int)

    for i in range(tamano - 1, -1, -1):
        x[i] = matriz[i, -1]
        for j in range(i + 1, tamano):
            if matriz[i, j] == 1:
                x[i] = x[i] ^ x[j]

    return np.transpose([x])

def matrizNula(matriz) -> bool:
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] != 0:
                return False
    return True

def indiceVector(tamano_matriz: int, indice_fila_elem: int, indice_columna_elem: int) -> int:
    return tamano_matriz * indice_fila_elem + indice_columna_elem


def generarMatrizAleatoria(n):
    print("Creando matriz de tamaño ", n)
    print("Esta es la matriz:")
    matriz = np.random.randint(2, size=(n, n))
    print(matriz)
    return matriz

def main():
    print("Bienvenido al juego Lights Out.")
    n = int(input("Indique el tamaño de la matriz:"))
    matrizAleatoria = generarMatrizAleatoria(n)
    print("Aqui está el vector con las posiciones que se deben pulsar:")
    print(juego(matrizAleatoria))

main()