import random


def generar_tablero():
    tablero = {
        1: {"color": "b", "movimientos": [2, 5, 6]},
        2: {"color": "n", "movimientos": [1, 3, 5, 6, 7]},
        3: {"color": "b", "movimientos": [2, 4, 6, 7, 8]},
        4: {"color": "n", "movimientos": [3, 7, 8]},
        5: {"color": "n", "movimientos": [1, 2, 6, 9, 10]},
        6: {"color": "b", "movimientos": [1, 2, 3, 5, 7, 9, 10, 11]},
        7: {"color": "n", "movimientos": [2, 3, 4, 6, 8, 10, 11, 12]},
        8: {"color": "b", "movimientos": [3, 4, 7, 11, 12]},
        9: {"color": "b", "movimientos": [5, 6, 10, 13, 14]},
        10: {"color": "n", "movimientos": [5, 6, 7, 9, 11, 13, 14, 15]},
        11: {"color": "b", "movimientos": [6, 7, 8, 10, 12, 14, 15, 16]},
        12: {"color": "n", "movimientos": [7, 8, 11, 15, 16]},
        13: {"color": "n", "movimientos": [9, 10, 14]},
        14: {"color": "b", "movimientos": [9, 10, 11, 13, 15]},
        15: {"color": "n", "movimientos": [10, 11, 12, 14, 16]},
        16: {"color": "b", "movimientos": [11, 12, 15]}
    }
    return tablero


def guardar_resultados(tablero, secuencia, inicio=4):
    with open("caminos2.txt", "w") as f_cam, open("ganadores2.txt", "w") as f_gan:
        def backtrack(pos, index, ruta):
            if index == len(secuencia):
                ruta_str = f"{ruta}\n"
                f_cam.write(ruta_str)
                if pos == 13:  # Posición final
                    f_cam.write("GANADOR!\n")
                    f_gan.write(ruta_str)
                return
            opciones = [m for m in tablero[pos]["movimientos"] if tablero[m]["color"] == secuencia[index]]

            if not opciones:
                print(f"No hay movimientos válidos desde {pos} con color {secuencia[index]}")  # Depuración

            for next_pos in opciones:
                backtrack(next_pos, index + 1, ruta + [next_pos])

        backtrack(inicio, 0, [inicio])


def generar_secuencia_aleatoria(longitud, letras):
    secuencia = random.choices(letras, k=longitud) + ["n"]
    with open("secuencia2.txt", "w") as f_secu:
        secu = f"{secuencia}\n"
        f_secu.write(secu)
    return secuencia


# Inicializar tablero y ejecutar
"""if __name__ == "__main__":
    tablero = generar_tablero()
    movimientos = 5
    secuencia2 = generar_secuencia_aleatoria(movimientos-1, ["b", "n"])
    guardar_resultados(tablero, secuencia2)"""