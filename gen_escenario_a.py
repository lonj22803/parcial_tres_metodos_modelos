from grafo import Grafo
from labyrinth import Labyrinth
import random

if __name__ == '__main__':
    grafo = Grafo()

    posiciones_usada = set()

    def es_posicion_valida(i, tipo):
        if tipo == 'O':
            aristas = [
                (i, i - 1),     # Lado izquierdo superior
                ((i + 20) - 1, i + 20),  # Lado izquierdo inferior
                (i + 1, i + 2),    # Lado derecho superior
                (i + 21, i + 22),    # Lado derecho inferior
                (i - 20, i),  # Lado superior izquierdo
                (i - 19, i + 1),  # Lado superior derecho
                (i + 20, i + 40),   # Lado inferior izquierdo
                (i + 21, i + 41) # Lado inferior derecho
            ]
        elif tipo == 'I':
            aristas = [
                (i, i - 1), # Lado izquierdo
                (i + 20, i + 19), # Lado izquierdo
                (i + 40, i + 39), # Lado izquierdo
                (i + 60, i + 59), # Lado izquierdo
                (i - 20, i), # Lado superior
                (i + 60, i + 80), # Lado inferior
                (i, i + 1), # Lado derecho
                (i + 20, i + 21), # Lado derecho
                (i + 40, i + 41), # Lado derecho
                (i + 60, i + 61) # Lado derecho
            ]
        elif tipo == 'T':
            aristas = [
                (i, i - 1),  # Lado izquierdo
                (i + 20, i + 19),  # Lado izquierdo
                (i + 40, i + 39),  # Lado izquierdo
                (i - 20, i),  # Lado superior
                (i + 40, i + 60),  # Lado inferior
                (i, i + 1),  # Lado derecho
                (i + 40, i + 41),  # Lado derecho
                (i + 21, i + 22),  # Lado derecho más
                (i + 1, i + 21), # Lado superior
                (i + 21, i + 41) # Lado inferior
            ]
        else:
            return False

        for a, b in aristas:
            if a in posiciones_usada or b in posiciones_usada or not (0 <= a < 300) or not (0 <= b < 300):
                return False
        return True

    def Pieza(tipo, i):
        if tipo == 'O':
            aristas = [
                (i, i - 1),     # Lado izquierdo superior
                ((i + 20) - 1, i + 20),  # Lado izquierdo inferior
                (i + 1, i + 2),    # Lado derecho superior
                (i + 21, i + 22),    # Lado derecho inferior
                (i - 20, i),  # Lado superior izquierdo
                (i - 19, i + 1),  # Lado superior derecho
                (i + 20, i + 40),   # Lado inferior izquierdo
                (i + 21, i + 41) # Lado inferior derecho
            ]
        elif tipo == 'I':
            aristas = [
                (i, i - 1), # Lado izquierdo
                (i + 20, i + 19), # Lado izquierdo
                (i + 40, i + 39), # Lado izquierdo
                (i + 60, i + 59), # Lado izquierdo
                (i - 20, i), # Lado superior
                (i + 60, i + 80), # Lado inferior
                (i, i + 1), # Lado derecho
                (i + 20, i + 21), # Lado derecho
                (i + 40, i + 41), # Lado derecho
                (i + 60, i + 61) # Lado derecho
            ]
        elif tipo == 'T':
            aristas = [
                (i, i - 1),  # Lado izquierdo
                (i + 20, i + 19),  # Lado izquierdo
                (i + 40, i + 39),  # Lado izquierdo
                (i - 20, i),  # Lado superior
                (i + 40, i + 60),  # Lado inferior
                (i, i + 1),  # Lado derecho
                (i + 40, i + 41),  # Lado derecho
                (i + 21, i + 22),  # Lado derecho más
                (i + 1, i + 21), # Lado superior
                (i + 21, i + 41) # Lado inferior
            ]
        else:
            return []

        for a, b in aristas:
            grafo.add_edge(a, b, 0)
            posiciones_usada.add(a)
            posiciones_usada.add(b)
        return aristas

    # Crear lista de posiciones disponibles
    posiciones_disponibles = set(range(300))
    posiciones_disponibles -= set(range(0, 20))
    posiciones_disponibles -= set(range(280, 300))
    posiciones_disponibles -= set(range(0, 280, 20))
    posiciones_disponibles -= set(range(19, 300, 20))
    posiciones_disponibles -= set(range(18,300, 20))

    tipos = ['O', 'I', 'T']
    figuras = []

    while len(figuras) < 7 and posiciones_disponibles:
        i = random.choice(list(posiciones_disponibles))
        tipo = random.choice(tipos)
        if es_posicion_valida(i, tipo):
            aristas = Pieza(tipo, i)
            figuras.append((tipo, i))
            # Actualizar posiciones disponibles
            for a, b in aristas:
                posiciones_disponibles.discard(a)
                posiciones_disponibles.discard(b)

    # Crear grafo solo con las paredes externas
    for i in range(300):
        if (i, i + 1) in posiciones_usada or (i + 1, i) in posiciones_usada:
            continue
        if i < 299:
            grafo.add_edge(i, i + 1, 1)
        if (i, i + 20) in posiciones_usada or (i + 20, i) in posiciones_usada:
            continue
        if i < 279:
            grafo.add_edge(i, i + 20, 1)

    # Generar tortugas aleatoriamente
    num_tortugas = random.randint(1, 10)
    turtle_list = {}
    posiciones_disponibles -= posiciones_usada

    for _ in range(num_tortugas):
        if not posiciones_disponibles:
            break
        pos = random.choice(list(posiciones_disponibles))
        turtle_list[pos] = random.randint(1, 4)  # Puedes definir la lógica para asignar valores a las tortugas
        posiciones_disponibles.discard(pos)

    # Asignar una posición de salida para una tortuga
    if posiciones_disponibles:
        exit_pos = random.choice(list(posiciones_disponibles))
        turtle_list[exit_pos] = 'f'

    grafo.turtle = turtle_list

    # Generar puntos verdes aleatoriamente
    colors_list = {}
    num_puntos_verdes = random.randint(1, 10)

    for _ in range(num_puntos_verdes):
        if not posiciones_disponibles:
            break
        pos = random.choice(list(posiciones_disponibles))
        colors_list[pos] = 'green'
        posiciones_disponibles.discard(pos)
        posiciones_disponibles -= posiciones_usada
    print(colors_list)

    grafo.colors = colors_list

    # Mostrar el grafo en la terminal
    print(grafo)
    # Mostrar las posiciones usadas
    print("Posiciones usadas", sorted(posiciones_usada))
    # Mostrar la lista de tortugas
    print("Lista de tortugas", turtle_list)
    # Guardar el grafo en el archivo
    grafo.save_graph(r'C:\Users\USER\PycharmProjects\labyrinth\graph_punto_dos.json')
    maze = Labyrinth(15, 20, path=r'C:\Users\USER\PycharmProjects\labyrinth\graph_punto_dos.json')
    maze.start()
