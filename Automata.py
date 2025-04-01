import random

def es_casilla_blanca(x, y):
    return (x + y) % 2 == 0

def movimientos_posibles(x, y):
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    return [(x + dx, y + dy) for dx, dy in direcciones if 0 <= x + dx < 4 and 0 <= y + dy < 4]

def guardar_resultados(secuencia, x=0, y=0):
    with open("caminos.txt", "w") as f_cam, open("ganadores.txt", "w") as f_gan:
        def backtrack(cx, cy, index, ruta):
            if index == len(secuencia):
                ruta_str = f"{ruta}\n"
                f_cam.write(ruta_str)  # Escribir en caminos.txt
                if ruta[-1] == (3, 3):  # Si es una ruta ganadora
                    f_cam.write("GANADOR!\n")  # También marcar en caminos.txt
                    f_gan.write(ruta_str)  # Guardar en ganadores.txt
                return

            opciones = [m for m in movimientos_posibles(cx, cy) if es_casilla_blanca(*m) == (secuencia[index] == "B")]
            for nx, ny in opciones:
                backtrack(nx, ny, index + 1, ruta + [(nx, ny)])

        backtrack(x, y, 0, [(x, y)])

def generar_secuencia_aleatoria(longitud, letras):
    return random.choices(letras, k=longitud)

# Ejecutar con una secuencia larga sin problemas de RAM
secuencia2 = generar_secuencia_aleatoria(15, ["B", "N"])
secuencia2.append("B")
guardar_resultados(secuencia2)