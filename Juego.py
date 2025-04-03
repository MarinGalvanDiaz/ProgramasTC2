import random
import tkinter as tk
from tkinter import messagebox


def leer_rutas(archivo):
    with open(archivo, "r") as f:
        return [eval(line.strip()) for line in f.readlines()]


class Ajedrez:
    def __init__(self, master, rutas_a, rutas_b, cadenaA,cadenaB):
        self.master = master
        self.rutas_a = rutas_a
        self.rutas_b = rutas_b
        self.cadenaA = cadenaA
        self.cadenaB = cadenaB
        self.setup_gui()
        self.iniciar_juego()

    def setup_gui(self):
        self.master.title("Juego de Fichas Automático")

        # Frame principal
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(padx=10, pady=10)

        # Tablero visual
        self.canvas = tk.Canvas(self.main_frame, width=400, height=400)
        self.canvas.pack()

        # Área de información
        self.info_text = tk.Text(self.main_frame, height=10, width=50)
        self.info_text.pack(pady=5)
        self.info_text.config(state=tk.DISABLED)

        # Variables de estado
        self.game_active = True
        self.winner = None
        self.animation_id = None

    def dibujar_tablero(self):
        self.canvas.delete("all")
        colors = ["white", "gray"]

        # Dibujar tablero 4x4
        for row in range(4):
            for col in range(4):
                x1 = col * 100
                y1 = row * 100
                x2 = x1 + 100
                y2 = y1 + 100
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        # Dibujar fichas (si no hay animación en curso)
        if not self.animation_id:
            self.dibujar_ficha(self.pos_a, "red", "A")
            self.dibujar_ficha(self.pos_b, "blue", "B")

    def dibujar_ficha(self, pos, color, tag):
        row = (pos - 1) // 4
        col = (pos - 1) % 4
        x = col * 100 + 50
        y = row * 100 + 50
        self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill=color, tags=tag)
        self.canvas.create_text(x, y, text=tag, font=('Arial', 20, 'bold'), fill="white")

    def agregar_mensaje(self, message):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.DISABLED)

    def iniciar_juego(self):
        # Inicialización idéntica al original
        self.rutas_a[0] = random.choice(self.rutas_a)
        self.rutas_b[0] = random.choice(self.rutas_b)

        self.pos_a, self.pos_b = self.rutas_a[0][0], self.rutas_b[0][0]
        self.index_a, self.index_b = 0, 0
        self.turno = random.choice(["A", "B"])

        self.cedidos_consecutivos = 0
        self.cedido_a = False
        self.cedido_b = False

        self.agregar_mensaje(f"Cadenas elegidas: \nA: {self.cadenaA[0]}\nB: {self.cadenaB[0]}")
        self.agregar_mensaje(f"Rutas elegidas:\nA: {self.rutas_a[0]}\nB: {self.rutas_b[0]}\n")
        self.dibujar_tablero()

        # Iniciar el ciclo de juego automático
        self.master.after(1000, self.jugar_turno)

    def jugar_turno(self):
        if not self.game_active:
            return

        self.agregar_mensaje(f"Turno de {self.turno}: A en {self.pos_a}, B en {self.pos_b}")

        # Lógica original de movimiento
        if self.turno == "A":
            nuevo_index, nueva_ruta, nueva_pos, movio = self.mover_ficha("A", self.rutas_a, self.index_a, self.pos_b)
            self.index_a, self.rutas_a, self.pos_a = nuevo_index, nueva_ruta, nueva_pos

            if self.index_a == len(self.rutas_a[0]) - 1 and self.pos_a == 16:
                self.agregar_mensaje("\n¡Ganador: A!")
                self.game_active = False
                self.animar_ganador("A")
                return

            if not movio:
                self.cedido_a = True
            self.turno = "B" if movio else "A"

        else:
            nuevo_index, nueva_ruta, nueva_pos, movio = self.mover_ficha("B", self.rutas_b, self.index_b, self.pos_a)
            self.index_b, self.rutas_b, self.pos_b = nuevo_index, self.rutas_b, nueva_pos

            if self.index_b == len(self.rutas_b[0]) - 1 and self.pos_b == 13:
                self.agregar_mensaje("\n¡Ganador: B!")
                self.game_active = False
                self.animar_ganador("B")
                return

            if not movio:
                self.cedido_b = True
            self.turno = "A" if movio else "B"

        # Verificar empate
        if self.cedido_a and self.cedido_b:
            self.agregar_mensaje("\n¡Nadie ganó! Ambos cedieron el turno consecutivamente.")
            self.game_active = False
            return

        # Resetear banderas de turno cedido
        if self.cedido_a:
            self.cedido_a = False
        if self.cedido_b:
            self.cedido_b = False

        self.dibujar_tablero()

        # Continuar con el siguiente turno después de un breve retraso
        if self.game_active:
            self.master.after(1500, self.jugar_turno)

    def animar_ganador(self, ganador):
        """Animación de la ficha ganadora"""
        pos = self.pos_a if ganador == "A" else self.pos_b
        color = "red" if ganador == "A" else "blue"

        # Dibujar solo la ficha ganadora
        self.canvas.delete("all")
        self.dibujar_tablero()  # Dibujar tablero primero

        # Coordenadas iniciales
        row = (pos - 1) // 4
        col = (pos - 1) % 4
        x = col * 100 + 50
        y = row * 100 + 50

        # Crear ficha ganadora
        ficha = self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill=color, tags=ganador)
        texto = self.canvas.create_text(x, y, text=ganador, font=('Arial', 20, 'bold'), fill="white")

        # Parámetros de animación
        self.animation_step = 0
        self.animation_max = 20
        self.animation_items = [ficha, texto]

        # Iniciar animación
        self.animar_ficha(x, y)

    def animar_ficha(self, x, y):
        """Realiza la animación de celebración"""
        if self.animation_step >= self.animation_max:
            self.animation_id = None
            return

        # Alternar tamaño para efecto de "latido"
        size = 40 + 5 * (1 if self.animation_step % 2 == 0 else -1)

        # Actualizar gráficos
        self.canvas.coords(self.animation_items[0], x - size, y - size, x + size, y + size)

        self.animation_step += 1
        self.animation_id = self.master.after(200, self.animar_ficha, x, y)

    # Método mover_ficha idéntico al original
    def mover_ficha(self, ficha, rutas, index, pos_oponente):
        ruta_actual = rutas[0]

        if index + 1 < len(ruta_actual):
            nueva_pos = ruta_actual[index + 1]
            if nueva_pos != pos_oponente:
                self.agregar_mensaje(f"{ficha} se mueve a {nueva_pos}")
                return index + 1, rutas, nueva_pos, True

        rutas_posibles = []
        for nueva_ruta in rutas:
            if len(nueva_ruta) > index + 1 and nueva_ruta[index] == ruta_actual[index]:
                nueva_pos = nueva_ruta[index + 1]
                if nueva_pos != pos_oponente:
                    rutas_posibles.append(nueva_ruta)

        if rutas_posibles:
            nueva_ruta = rutas_posibles[0]
            rutas[0] = nueva_ruta
            nueva_pos = nueva_ruta[index + 1]
            self.agregar_mensaje(f"{ficha} cambia a nueva ruta: {nueva_ruta}")
            self.agregar_mensaje(f"{ficha} se mueve a {nueva_pos}")
            return index + 1, rutas_posibles, nueva_pos, True

        self.agregar_mensaje(f"{ficha} no tiene movimientos válidos, cede turno.")
        return index, rutas, ruta_actual[index], True


# Iniciar juego
