import random
import time


def leer_rutas(archivo):
    with open(archivo, "r") as f:
        return [eval(line.strip()) for line in f.readlines()]


def imprimir_tablero(pos_a, pos_b):
    tablero = ["."] * 16
    tablero[pos_a - 1] = "A"
    tablero[pos_b - 1] = "B"
    for i in range(0, 16, 4):
        print(" ".join(tablero[i:i + 4]))
    print("\n")


def jugar(rutas_a, rutas_b):
    rutas_a[0] = random.choice(rutas_a)
    rutas_b[0] = random.choice(rutas_b)

    pos_a, pos_b = rutas_a[0][0], rutas_b[0][0]
    index_a, index_b = 0, 0
    turno = random.choice(["A", "B"])

    cedidos_consecutivos = 0  # Para contar turnos consecutivos cedidos
    cedido_a, cedido_b = False, False  # Indica si A o B cedió el turno

    print(f"Rutas elegidas:\nA: {rutas_a[0]}\nB: {rutas_b[0]}\n")

    while index_a < len(rutas_a[0]) - 1 or index_b < len(rutas_b[0]) - 1:
        print(f"Turno de {turno}: A en {pos_a}, B en {pos_b}")
        imprimir_tablero(pos_a, pos_b)
        time.sleep(1.5)

        if turno == "A":
            nuevo_index, nueva_ruta, nueva_pos, movio = mover_ficha("A", rutas_a, index_a, pos_b)
            index_a, rutas_a, pos_a = nuevo_index, nueva_ruta, nueva_pos
            if index_a == len(rutas_a[0]) - 1 and pos_a == 16:  # Verifica si A ganó
                print("\n¡Ganador: A!")
                break  # Termina el juego si A gana

            if not movio:  # Si A cedió el turno
                cedido_a = True
            turno = "B" if movio else "A"  # Solo cambia si A se movió

        else:
            nuevo_index, nueva_ruta, nueva_pos, movio = mover_ficha("B", rutas_b, index_b, pos_a)
            index_b, rutas_b, pos_b = nuevo_index, rutas_b, nueva_pos
            if index_b == len(rutas_b[0]) - 1 and pos_b == 13:  # Verifica si B ganó
                print("\n¡Ganador: B!")
                break  # Termina el juego si B gana

            if not movio:  # Si B cedió el turno
                cedido_b = True
            turno = "A" if movio else "B"  # Solo cambia si B se movió

        # Verificar si ambos cedieron el turno consecutivamente
        if cedido_a and cedido_b:
            print("\n¡Nadie ganó! Ambos cedieron el turno consecutivamente.")
            break  # Termina el juego si ambos cedieron el turno

        # Si un jugador cedió el turno, reiniciar la bandera del otro jugador
        if cedido_a:
            cedido_a = False
        if cedido_b:
            cedido_b = False


def mover_ficha(ficha, rutas, index, pos_oponente):
    ruta_actual = rutas[0]

    # Intentar moverse en la ruta actual
    if index + 1 < len(ruta_actual):
        nueva_pos = ruta_actual[index + 1]
        # Verificar que la posición siguiente no esté ocupada por la otra ficha
        if nueva_pos != pos_oponente:
            print(f"{ficha} se mueve a {nueva_pos}")
            return index + 1, rutas, nueva_pos, True

    # Buscar todas las rutas posibles con la misma posición en el índice actual
    rutas_posibles = []
    for nueva_ruta in rutas:
        if len(nueva_ruta) > index + 1 and nueva_ruta[index] == ruta_actual[index]:
            nueva_pos = nueva_ruta[index + 1]
            # Verificar que la nueva posición no esté ocupada por la otra ficha
            if nueva_pos != pos_oponente:
                rutas_posibles.append(nueva_ruta)

    # Si se encontró alguna ruta válida para moverse
    if rutas_posibles:
        nueva_ruta = rutas_posibles[0]  # Seleccionar una ruta válida aleatoriamente
        rutas[0] = nueva_ruta  # Actualiza la ruta seleccionada en rutas[0]
        nueva_pos = nueva_ruta[index + 1]  # Obtener la nueva posición desde la ruta seleccionada
        print(f"{ficha} cambia a nueva ruta: {nueva_ruta}")
        print(f"{ficha} se mueve a {nueva_pos}")
        return index + 1, rutas, nueva_pos, True

    # Si no encuentra movimiento, cede el turno
    print(f"{ficha} no tiene movimientos válidos, cede turno.")
    return index, rutas, ruta_actual[index], True  # Mantiene su posición y cede turno


# Cargar rutas y jugar
"""rutas_a = leer_rutas("ganadores.txt")
rutas_b = leer_rutas("ganadores2.txt")
jugar(rutas_a, rutas_b)"""
