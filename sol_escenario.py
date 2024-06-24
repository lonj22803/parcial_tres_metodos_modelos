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

def dijkstra(grafo, inicio, objetivo):
    cola = [(0, inicio)]
    distancias = {nodo: 999999 for nodo in grafo}  # 999999 como una representación de "infinito"
    distancias[inicio] = 0
    anteriores = {nodo: None for nodo in grafo}

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual == objetivo:
            break

        for vecino, peso in grafo[nodo_actual]:
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

def guardar_solucion(filename, rutas_tortugas, type_method):
    with open(filename, "r") as file:
        data = json.load(file)

    data["turtle"] = rutas_tortugas

    filename = filename.replace(".json", f"_solucion{type_method}.json")
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Solucion guardada en {filename}")

def main():
    grafo = cargar_grafo('graph_generado.json')
    with open('graph_generado.json', 'r') as file:
        data = json.load(file)

    tortugas = list(data['turtle'].keys())
    puntos_rojos = [int(k) for k, v in data['colors'].items() if v == 'red']
    
    rutas_tortugas = {}

    for tortuga in tortugas:
        inicio = int(tortuga)
        dist_min = 999999
        punto_cercano = None
        ruta_minima = []

        for punto in puntos_rojos:
            objetivo = int(punto)
            camino, distancia = dijkstra(grafo, inicio, objetivo)
            if distancia < dist_min:
                dist_min = distancia
                punto_cercano = punto
                ruta_minima = camino

        if ruta_minima:
            for i in range(len(ruta_minima) - 1):
                rutas_tortugas[ruta_minima[i]] = ruta_minima[i + 1]
            rutas_tortugas[ruta_minima[-1]] = 'f'  # Marca el objetivo como final
            puntos_rojos.remove(punto_cercano)  # Eliminar el punto rojo utilizado

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



