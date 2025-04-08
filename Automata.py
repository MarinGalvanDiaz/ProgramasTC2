import random
import Automata2 as Au2
import Juego as Ju
import Traza as Tra
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


def guardar_resultados(tablero, secuencia, inicio=1):
    with open("caminos.txt", "w") as f_cam, open("ganadores.txt", "w") as f_gan:
        def backtrack(pos, index, ruta):
            if index == len(secuencia):
                ruta_str = f"{ruta}\n"
                f_cam.write(ruta_str)
                if pos == 16:  # Posición final
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
    secuencia = random.choices(letras, k=longitud) + ["b"]
    with open("secuencia.txt", "w") as f_secu:
        secu = f"{secuencia}\n"
        f_secu.write(secu)
    return secuencia


def menu_principal():
    print("\n=== MENÚ ===")
    print("1. Juego automático (todo aleatorio)")
    print("2. Configurar manualmente")
    print("3. Salir")

    while True:
        opcion = input("Seleccione: ")
        if opcion in ["1", "2", "3"]:
            return opcion
        print("Opción no válida")


def configurar_manual():
    # Longitud
    while True:
        try:
            n = int(input("\nLongitud de secuencia (4-15): "))
            if 4 <= n <= 15:
                break
        except:
            pass
        print("Debe ser número entre 4 y 15")

    # Tipo de secuencia
    while True:
        tipo = input("¿Generar aleatorio? (s/n): ").lower()
        if tipo in ["s", "n"]:
            break

    if tipo == "s":
        sec = generar_secuencia_aleatoria(n-1,["b", "n"])
        sec2 = Au2.generar_secuencia_aleatoria(n-1,["b", "n"])
    else:
        sec = ingresar_secuencia(n)
        sec2 = ingresar_secuencia(n, "Jugador 2")

    return sec, sec2


def ingresar_secuencia(n, jugador="Jugador 1"):
    print(f"\nIngrese secuencia para {jugador}:")
    return [input(f"Color {i + 1} (b/n): ") for i in range(n)]

def guardar_secuencia(secuencia, archivo="secuencia.txt"):
    with open(archivo, "w") as f:
        f.write(f"{secuencia}\n")

if __name__ == "__main__":
    while True:
        op = menu_principal()

        if op == "1":
            # Modo automático
            n = random.randint(3, 14)
            secuencia = generar_secuencia_aleatoria(n, ["b", "n"])
            secuencia2 = Au2.generar_secuencia_aleatoria(n, ["b", "n"])

        elif op == "2":
            # Modo manual
            secuencia, secuencia2 = configurar_manual()

        elif op == "3":
            exit(0)

        # Generar y guardar tableros
        tablero = generar_tablero()
        tablero2 = Au2.generar_tablero()

        guardar_resultados(tablero, secuencia)
        Au2.guardar_resultados(tablero2, secuencia2)

        guardar_secuencia(secuencia)
        guardar_secuencia(secuencia2, "secuencia2.txt")

        # Leer datos para los gráficos
        rutas_a = Ju.leer_rutas("ganadores.txt")
        rutas_b = Ju.leer_rutas("ganadores2.txt")
        cadenaA = Ju.leer_rutas("secuencia.txt")
        cadenaB = Ju.leer_rutas("secuencia2.txt")

        # Mostrar gráficos antes de la interfaz Tkinter
        secuencia7 = Tra.leer_secuencia("secuencia.txt")
        rutas8 = Tra.leer_rutas("ganadores.txt")
        Tra.graficar_traza(secuencia7, rutas8)

        secuencia5 = Tra.leer_secuencia("secuencia2.txt")
        rutas6 = Tra.leer_rutas("ganadores2.txt")
        Tra.graficar_traza(secuencia5, rutas6)

        # Iniciar interfaz gráfica
        if len(rutas_a) == 0:
            print("No hay rutas para A")
            exit(0)
        if len(rutas_b) == 0:
            print("No hay rutas para B")
            exit(0)
        root = Ju.tk.Tk()
        app = Ju.Ajedrez(root, rutas_a, rutas_b, cadenaA, cadenaB)
        root.mainloop()

        input("\nPresione Enter para continuar...")