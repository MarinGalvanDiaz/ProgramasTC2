import networkx as nx
import matplotlib.pyplot as plt


def leer_secuencia(filename):
    with open(filename, "r") as f:
        return eval(f.readline().strip())


def leer_rutas(filename):
    rutas = []
    with open(filename, "r") as f:
        for line in f:
            if "GANADOR" not in line:
                rutas.append(eval(line.strip()))
    return rutas


def calcular_niveles(rutas):
    niveles = {}
    for ruta in rutas:
        for nivel, nodo in enumerate(ruta):
            if nodo not in niveles or nivel < niveles[nodo]:
                niveles[nodo] = nivel
    return niveles


def distribuir_nodos_por_nivel(niveles):
    posiciones = {}
    if not niveles:
        return posiciones

    nivel_max = max(niveles.values())

    # Contar nodos por nivel
    conteo_nivel = {}
    for nodo, nivel in niveles.items():
        conteo_nivel[nivel] = conteo_nivel.get(nivel, 0) + 1

    # Calcular posiciones
    offset_nivel = {nivel: 0 for nivel in range(nivel_max + 1)}

    for nodo, nivel in niveles.items():
        total_nodos = conteo_nivel[nivel]
        espaciado = 1.5  # Ajusta este valor según necesites
        x = nivel
        y = -(offset_nivel[nivel] - (total_nodos - 1) / 2) * espaciado

        posiciones[nodo] = (x, y)
        offset_nivel[nivel] += 1

    return posiciones


def graficar_traza(secuencia, rutas):
    G = nx.DiGraph()
    niveles = calcular_niveles(rutas)

    # Construir el grafo completo
    for ruta in rutas:
        for i in range(len(ruta) - 1):
            G.add_edge(ruta[i], ruta[i + 1])

    pos = distribuir_nodos_por_nivel(niveles)
    labels = {n: str(n) for n in G.nodes}

    # Crear figura con espacio adicional abajo
    fig, ax = plt.subplots(figsize=(12, 8))

    # Dibujar el grafo completo como antes
    nx.draw(G, pos, ax=ax, with_labels=True, labels=labels,
            node_size=2000, node_color="lightblue",
            edge_color="black", font_size=12,
            arrowsize=20, arrowstyle='->', width=1.5)

    # Añadir la secuencia en la parte inferior
    secuencia_str = "Secuencia completa: " + " → ".join(secuencia)
    ax.text(0.5, -0.1, secuencia_str, transform=ax.transAxes,
            ha='center', va='center', fontsize=12,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # Ajustar márgenes para la secuencia
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.15)
    plt.title("Traza de Decisiones - Grafo Completo", pad=20)
    plt.show()