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

    # Agregar todos los nodos y aristas
    for ruta in rutas:
        for i in range(len(ruta) - 1):
            G.add_edge(ruta[i], ruta[i + 1])

    pos = distribuir_nodos_por_nivel(niveles)
    labels = {n: str(n) for n in G.nodes}

    # Crear figura con más espacio en la parte inferior
    fig, ax = plt.subplots(figsize=(14, 9))

    # Dibujar el grafo base
    nx.draw(G, pos, ax=ax, with_labels=True, labels=labels,
            node_size=2000, node_color="lightblue",
            edge_color="lightgray", font_size=12,
            arrowsize=20, arrowstyle='->', width=1.5)

    # Resaltar cada ruta con colores
    colors = plt.cm.tab10.colors
    for i, ruta in enumerate(rutas):
        edge_list = [(ruta[j], ruta[j + 1]) for j in range(len(ruta) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edge_list,
                               edge_color=colors[i % len(colors)],
                               width=2.5, arrowsize=25, ax=ax)

        # Etiqueta de ruta
        if len(ruta) > 0:
            x, y = pos[ruta[0]]
            ax.text(x, y + 0.3, f"Ruta {i + 1}: {ruta}",
                    color=colors[i % len(colors)],
                    bbox=dict(facecolor='white', alpha=0.7))

    # Mostrar la secuencia en la parte inferior
    secuencia_str = "Secuencia: " + " → ".join(secuencia)
    ax.text(0.5, -0.1, secuencia_str, transform=ax.transAxes,
            ha='center', va='center', fontsize=12,
            bbox=dict(facecolor='white', alpha=0.7))

    # Ajustar márgenes para dar espacio a la secuencia
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.15)
    plt.title("Traza de Decisiones", pad=20)
    plt.show()