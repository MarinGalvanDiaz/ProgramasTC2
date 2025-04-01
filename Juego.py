import random


def leer_rutas(archivo):
    with open(archivo, "r") as f:
        return [eval(f.readline().strip())]  # Leer solo la primera ruta


def jugar(rutas_a, rutas_b):
    pos_a, pos_b = rutas_a[0][0], rutas_b[0][0]  # Posiciones iniciales

    index_a, index_b = 0, 0  # Índices en las rutas
    turno = random.choice(["A", "B"])  # Elegir quién empieza

    print(f"Rutas elegidas:\nA: {rutas_a[0]}\nB: {rutas_b[0]}\n")

    while pos_a != 16 and pos_b != 13:  # A gana al llegar a 16, B a 13
        print(pos_a, pos_b)
        if turno == "A":
            # Intentar moverse a la siguiente posición en la ruta de A
            if index_a + 1 < len(rutas_a[0]):
                nueva_pos = rutas_a[0][index_a + 1]
                print(f"A intenta moverse de {pos_a} a {nueva_pos}")
                if nueva_pos != pos_b:  # Verificar que la casilla no esté ocupada
                    pos_a = nueva_pos
                    index_a += 1
                else:
                    print(f"A no puede moverse a {nueva_pos}, cede el paso.")
            else:
                print(f"A no tiene más movimientos, cede el paso.")
        else:
            # Intentar moverse a la siguiente posición en la ruta de B
            if index_b + 1 < len(rutas_b[0]):
                nueva_pos = rutas_b[0][index_b + 1]
                print(f"B intenta moverse de {pos_b} a {nueva_pos}")
                if nueva_pos != pos_a:  # Verificar que la casilla no esté ocupada
                    pos_b = nueva_pos
                    index_b += 1
                else:
                    print(f"B no puede moverse a {nueva_pos}, cede el paso.")
            else:
                print(f"B no tiene más movimientos, cede el paso.")

        print(f"Estado: A -> {pos_a}, B -> {pos_b}\n")
        turno = "B" if turno == "A" else "A"  # Cambiar turno

    if pos_a == 16:
        ganador = "A"  # A gana al llegar a la casilla 16
    elif pos_b == 13:
        ganador = "B"  # B gana al llegar a la casilla 13
    else:
        ganador = random.choice(["A", "B"])  # Elegir ganador aleatoriamente si ambos llegan al mismo tiempo

    print(f"¡Ganador: {ganador}!")


# Cargar rutas y jugar
rutas_a = leer_rutas("ganadores.txt")
rutas_b = leer_rutas("ganadores2.txt")
print(rutas_a,rutas_b)
jugar(rutas_a, rutas_b)
