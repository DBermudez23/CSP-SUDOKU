"""
Solucionador de Sudoku Killer basado en Programación de Restricciones
Autores: Daniel Felipe Bermudez Florez y Juan Sebastián Tamayo Cuadrado

Descripción:
Este programa implementa la solución para tableros de Sudoku Killer mediante el uso de programación de restricciones utilizando la librería Z3 Solver. Modela cada celda del tablero como una variable con un dominio restringido y aplica reglas de unicidad y suma para garantizar una solución válida.

Entrada:
El programa acepta una lista de restricciones como entrada. Cada restricción representa:
- Una suma objetivo para un grupo de celdas (jaula).
- Las celdas involucradas en esa suma, definidas mediante coordenadas en el tablero.

Ejemplo de entrada:
```python
restricciones_sudoku = [
    (8, [(1, 1), (2, 1)]),
    (24, [(1, 2), (1, 3), (2, 3)]),
    (9, [(1, 4), (2, 4)])
]

"""

# Importación de la librería z3 para la solución de problemas de restricciones
from z3 import *

# Función para crear una variable entera con restricciones de valor mínimo y máximo
def crear_variable_entera(solver, nombre_variable, valor_minimo, valor_maximo):
    """
    Crea una variable entera dentro del rango dado y la agrega al solucionador.

    :param solver: El solucionador Z3.
    :param nombre_variable: Nombre identificador de la variable.
    :param valor_minimo: Valor mínimo permitido.
    :param valor_maximo: Valor máximo permitido.
    :return: La variable creada.
    """
    variable = Int(nombre_variable)
    solver.add(variable >= valor_minimo, variable <= valor_maximo)
    return variable

# Función para añadir restricciones de suma y unicidad a un grupo de celdas
def agregar_restriccion_jaula(solver, celdas_grupo, suma_objetivo):
    """
    Agrega restricciones para una jaula en el Sudoku Killer:
    - La suma de las celdas debe ser igual a la suma objetivo.
    - Los valores en las celdas deben ser únicos.

    :param solver: El solucionador Z3.
    :param celdas_grupo: Lista de celdas en la jaula.
    :param suma_objetivo: Suma deseada para la jaula.
    """
    solver.add(Sum(celdas_grupo) == suma_objetivo)
    solver.add(Distinct(celdas_grupo))

# Función principal para resolver el Sudoku Killer
def resolver_sudoku_killer(restricciones, dimension_tablero):
    """
    Resuelve un tablero de Sudoku Killer usando Z3 Solver.

    :param restricciones: Lista de restricciones (suma_objetivo, celdas_grupo).
    :param dimension_tablero: Tamaño del tablero (por ejemplo, 9 para un tablero 9x9).
    """
    # Diccionario para almacenar las variables de las celdas
    variables_tablero = {}

    # Inicializar el solucionador Z3
    solucionador = SolverFor("QF_FD")

    # Crear variables para cada celda del tablero
    for fila in range(dimension_tablero):
        for columna in range(dimension_tablero):
            variables_tablero[(fila, columna)] = crear_variable_entera(
                solucionador,
                f"celda[{fila + 1},{columna + 1}]",
                1,
                dimension_tablero
            )

    # Restricciones para filas y columnas (valores únicos)
    for fila in range(dimension_tablero):
        solucionador.add(Distinct([variables_tablero[fila, columna] for columna in range(dimension_tablero)]))
        solucionador.add(Distinct([variables_tablero[columna, fila] for columna in range(dimension_tablero)]))

    # Restricciones para las subcuadrículas (3x3 en un tablero estándar)
    subcuadricula = int(dimension_tablero ** 0.5)
    for fila_inicio in range(0, dimension_tablero, subcuadricula):
        for columna_inicio in range(0, dimension_tablero, subcuadricula):
            solucionador.add(Distinct([
                variables_tablero[fila_inicio + r, columna_inicio + c]
                for r in range(subcuadricula)
                for c in range(subcuadricula)
            ]))

    # Agregar restricciones de jaulas basadas en la entrada
    for suma_objetivo, celdas_grupo in restricciones:
        jaula = [variables_tablero[fila - 1, columna - 1] for fila, columna in celdas_grupo]
        agregar_restriccion_jaula(solucionador, jaula, suma_objetivo)

    # Resolver el problema y contar soluciones
    soluciones_encontradas = 0

    while solucionador.check() == sat:
        soluciones_encontradas += 1
        modelo = solucionador.model()

        # Imprimir la solución actual en formato de tablero
        print(f"Solución {soluciones_encontradas}:")
        for fila in range(dimension_tablero):
            print(" ".join(str(modelo.eval(variables_tablero[fila, columna])) for columna in range(dimension_tablero)))
        print()

        # Agregar una restricción para evitar repetir la solución encontrada
        solucionador.add(Or([
            variables_tablero[fila, columna] != modelo.eval(variables_tablero[fila, columna])
            for fila in range(dimension_tablero)
            for columna in range(dimension_tablero)
        ]))

    # Imprimir el número total de soluciones encontradas
    if soluciones_encontradas == 0:
        print("No se encontraron soluciones.")
    else:
        print(f"Total de soluciones encontradas: {soluciones_encontradas}")

# Restricciones del Sudoku Killer (ejemplo)
restricciones_sudoku = [
    (8, [(1, 1), (2, 1)]),
    (24, [(1, 2), (1, 3), (2, 3)]),
    (9, [(1, 4), (2, 4)]),
    (14, [(1, 5), (1, 6), (1, 7)]),
    (15, [(1, 8), (1, 9), (2, 8), (2, 9)]),
    (6, [(2, 2), (3, 2)]),
    (15, [(2, 5), (2, 6), (2, 7)]),
    (11, [(3, 1), (4, 1), (4, 2)]),
    (16, [(3, 3), (3, 4), (3, 5)]),
    (19, [(3, 6), (3, 7), (3, 8), (4, 6)]),
    (17, [(3, 9), (4, 9)]),
    (23, [(4, 3), (5, 2), (5, 3), (6, 2), (6, 3)]),
    (8, [(4, 4), (5, 4)]),
    (8, [(4, 5), (5, 5)]),
    (19, [(4, 7), (4, 8), (5, 8)]),
    (15, [(5, 1), (6, 1)]),
    (7, [(5, 6), (5, 7)]),
    (7, [(5, 9), (6, 9)]),
    (17, [(6, 4), (6, 5)]),
    (8, [(6, 6), (6, 7)]),
    (14, [(6, 8), (7, 8), (7, 9)]),
    (16, [(7, 1), (8, 1), (8, 2)]),
    (17, [(7, 2), (7, 3), (7, 4)]),
    (10, [(7, 5), (7, 6)]),
    (21, [(7, 7), (8, 7), (8, 8), (8, 9)]),
    (8, [(8, 3), (8, 4), (8, 5)]),
    (22, [(8, 6), (9, 4), (9, 5), (9, 6)]),
    (17, [(9, 1), (9, 2), (9, 3)]),
    (14, [(9, 7), (9, 8), (9, 9)]),
]

# Dimensión estándar del tablero 9x9
dimension = 9

# Llamada a la función para resolver el Sudoku Killer
resolver_sudoku_killer(restricciones_sudoku, dimension)



