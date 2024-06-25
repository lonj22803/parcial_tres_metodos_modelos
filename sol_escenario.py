import json
import heapq
import shutil
import threading
import labyrinth

def cargar_grafo(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    grafo = {}
    for nodo, vecinos in data["V"].items():
        grafo[int(nodo)] = []
        for vecino in vecinos:
            peso = data["E"].get(f"({nodo}, {vecino})") or data["E"].get(f"({vecino}, {nodo})")
            if peso is not None:
                grafo[int(nodo)].append((int(vecino), peso))
    return grafo

def backup_labyrinth(ruta):
    original_json_path = ruta
    backup_json_path = 'backup.json'
    shutil.copy(original_json_path, backup_json_path)
    return backup_json_path

def es_valida(pos, nrows, ncols):
    row, col = divmod(pos, ncols)
    if not (0 <= row < nrows and 0 <= col < ncols):
        return False
    
    # Verificar si la posición está en el borde derecho o izquierdo del laberinto
    if (col == 0 and pos - 1 != 0) or (col == ncols - 1 and pos + 1 != nrows * ncols):
        return False
    
    return True

def dijkstra(grafo, inicio, objetivo, posiciones_prohibidas, posiciones_bloqueadas, nrows, ncols):
    cola = [(0, inicio)]
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    anteriores = {nodo: None for nodo in grafo}

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual == objetivo:
            break

        for vecino, peso in grafo[nodo_actual]:
            if vecino in posiciones_prohibidas or not es_valida(vecino, nrows, ncols):
                continue
            if vecino in posiciones_bloqueadas and vecino != objetivo:
                continue
            distancia = distancia_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                anteriores[vecino] = nodo_actual
                heapq.heappush(cola, (distancia, vecino))

    camino = []
    nodo = objetivo
    while nodo is not None:
        camino.append(nodo)
        nodo = anteriores[nodo]
    camino.reverse()

    return camino, distancias[objetivo]

def cargar_posiciones_prohibidas(filename):
    with open(filename, 'r') as file:
        posiciones_prohibidas = [int(line.strip()) for line in file.readlines()]
    return posiciones_prohibidas

def guardar_solucion(filename, rutas_tortugas, type_method):
    with open(filename, "r") as file:
        data = json.load(file)

    data["turtle"] = rutas_tortugas

    filename = filename.replace(".json", f"_solucion{type_method}.json")
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Solucion guardada en {filename}")

def main():
    nrows, ncols = 15, 20
    grafo = cargar_grafo('graph_generado.json')
    posiciones_prohibidas = cargar_posiciones_prohibidas('cuadros_encerrados.txt')
    
    with open('graph_generado.json', 'r') as file:
        data = json.load(file)

    tortugas = list(data['turtle'].keys())
    colores_prioridad = ['red', 'blue', 'green']
    puntos_prioridad = {color: [int(k) for k, v in data['colors'].items() if v == color] for color in colores_prioridad}
    
    rutas_tortugas = {}
    posiciones_bloqueadas = set()

    for color in colores_prioridad:
        puntos_colores = puntos_prioridad[color]

        for tortuga in tortugas:
            inicio = int(tortuga)
            ruta_tortuga = [inicio]  # Inicializar la ruta con la posición inicial de la tortuga
            posiciones_bloqueadas_temp = set(posiciones_bloqueadas)  # Copiar las posiciones bloqueadas actuales

            for punto in puntos_colores:
                objetivo = int(punto)
                camino, distancia = dijkstra(grafo, inicio, objetivo, posiciones_prohibidas, posiciones_bloqueadas_temp, nrows, ncols)
                if distancia < float('inf'):
                    ruta_tortuga.extend(camino[1:])  # Añadir la ruta encontrada a la ruta de la tortuga
                    inicio = objetivo  # Actualizar el inicio para el próximo punto
                    posiciones_bloqueadas_temp.add(objetivo)  # Bloquear esta posición para otras tortugas

            if ruta_tortuga:
                for i in range(len(ruta_tortuga) - 1):
                    rutas_tortugas[ruta_tortuga[i]] = ruta_tortuga[i + 1]
                rutas_tortugas[ruta_tortuga[-1]] = 'f'  # Marcar el objetivo como final

            posiciones_bloqueadas.update(posiciones_bloqueadas_temp)  # Actualizar las posiciones bloqueadas

    guardar_solucion('graph_generado.json', rutas_tortugas, "Dijkstra")

if __name__ == "__main__":
    hilo1 = threading.Thread(target=lambda: labyrinth.Labyrinth(15, 20, path=backup_labyrinth('graph_generado.json')).start())
    hilo2 = threading.Thread(target=main)
    hilo3 = threading.Thread(target=lambda: labyrinth.Labyrinth(15, 20, path=backup_labyrinth('graph_generado_solucionDijkstra.json')).start())

    hilo1.start()
    hilo2.start()

    hilo2.join()
    hilo1.join()
    hilo3.start()

    hilo3.join()