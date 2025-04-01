import random

def es_casilla_blanca(x, y):
    return (x + y) % 2 == 0

def movimientos_posibles(x, y):
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    return [(x + dx, y + dy) for dx, dy in direcciones if 0 <= x + dx < 4 and 0 <= y + dy < 4]

def guardar_resultados(secuencia, x=3, y=0):  # Nueva posición inicial
    with open("caminos2.txt", "w") as f:
        def backtrack(cx, cy, index, ruta):
            if index == len(secuencia):
                f.write(f"{ruta}\n")
                if ruta[-1] == (0, 3):  # Nueva condición de victoria
                    f.write("GANADOR!\n")
                return

            opciones = [m for m in movimientos_posibles(cx, cy) if es_casilla_blanca(*m) == (secuencia[index] == "B")]
            for nx, ny in opciones:
                backtrack(nx, ny, index + 1, ruta + [(nx, ny)])

        backtrack(x, y, 0, [(x, y)])

def generar_secuencia_aleatoria(longitud, letras):
    return random.choices(letras, k=longitud)

# Ejecutar con una secuencia larga sin problemas de RAM
secuencia2 = generar_secuencia_aleatoria(15, ["B", "N"])
secuencia2.append("N")  # Se mantiene el mismo comportamiento
guardar_resultados(secuencia2)