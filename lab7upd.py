import random
import math
import heapq
import time


def generate_graph(N):
    print(f"\n--- Генерация графа на {N} вершин ---")
    # Используем список смежности для экономии памяти
    graph = {i: {} for i in range(N)}

    def add_edge(u, v, weight):
        if u != v and v not in graph[u]:
            graph[u][v] = weight
            graph[v][u] = weight

    # 1. Делаем граф связным (проводим магистраль через все вершины)
    for i in range(N - 1):
        add_edge(i, i + 1, random.randint(10, 50))

    # 2. Добавляем подграф K_6 (полный граф на 6 вершинах)
    for i in range(1, 7):
        for j in range(i + 1, 7):
            add_edge(i, j, random.randint(10, 50))

    # 3. Добавляем подграф K_3,5 (двудольный граф)
    part1 = [10, 11, 12]
    part2 = [13, 14, 15, 16, 17]
    for u in part1:
        for v in part2:
            add_edge(u, v, random.randint(10, 50))

    # 4. Добиваем граф до нужной степени разреженности (средняя степень n^(1/2))
    target_edges = int(N * math.sqrt(N) / 2)
    current_edges = sum(len(neighbors) for neighbors in graph.values()) // 2

    # ИЗМЕНЕНИЕ: Ограничиваем дальность "полета" ребра, чтобы не было "телепортов"
    # Соединяем только те вершины, которые находятся не дальше 100 шагов друг от друга
    while current_edges < target_edges:
        u = random.randint(0, N - 1)
        offset = random.randint(-100, 100)
        v = u + offset

        # Проверяем, что v существует, не равно u и дороги еще нет
        if 0 <= v < N and u != v and v not in graph[u]:
            add_edge(u, v, random.randint(10, 50))
            current_edges += 1

    print(f"Граф сгенерирован. Вершин: {N}, Ребер: {current_edges}")
    return graph


def dijkstra(graph, start):
    N = len(graph)
    distances = {i: float('inf') for i in range(N)}
    distances[start] = 0
    parents = {i: -1 for i in range(N)}

    pq = [(0, start)]
    iterations = 0

    while pq:
        iterations += 1
        current_dist, u = heapq.heappop(pq)

        if current_dist > distances[u]:
            continue

        for v, weight in graph[u].items():
            iterations += 1
            distance = current_dist + weight
            if distance < distances[v]:
                distances[v] = distance
                parents[v] = u
                heapq.heappush(pq, (distance, v))

    return distances, parents, iterations


def floyd_warshall(graph, N):
    # Создаем матрицу расстояний и матрицу маршрутов (next_node)
    dist = [[float('inf')] * N for _ in range(N)]
    next_node = [[-1] * N for _ in range(N)]

    for i in range(N):
        dist[i][i] = 0
        next_node[i][i] = i
        for v, w in graph[i].items():
            dist[i][v] = w
            next_node[i][v] = v

    iterations = 0
    # Основной цикл алгоритма Флойда-Уоршелла
    for k in range(N):
        for i in range(N):
            for j in range(N):
                iterations += 1
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node, iterations


def get_path_floyd(next_node, start, target):
    if next_node[start][target] == -1:
        return []

    path = [start]
    curr = start
    while curr != target:
        curr = next_node[curr][target]
        path.append(curr)
    return path


# --- ТЕСТИРОВАНИЕ ---
N = 500
graph = generate_graph(N)
target = N - 1  

# --- Блок Дейкстры ---
print("\nЗапускаем алгоритм Дейкстры...")
start_time = time.time()
distances, parents, dijkstra_iters = dijkstra(graph, 0)
dijkstra_time = time.time() - start_time
print(f"Дейкстра отработал за {dijkstra_time:.4f} сек. Итераций: {dijkstra_iters}")

# Восстанавливаем путь от 0 до N-1
dijkstra_path = []
curr = target
while curr != -1:
    dijkstra_path.append(curr)
    curr = parents[curr]
dijkstra_path.reverse()

print(f"Длина пути (Дейкстра): {distances[target]}")
print(f"Маршрут (Дейкстра): {dijkstra_path[:5]} ... {dijkstra_path[-5:]}")
print(f"Всего остановок в пути: {len(dijkstra_path)}")

# --- Блок Флойда-Уоршелла ---
print("\nЗапускаем алгоритм Флойда-Уоршелла...")
start_time = time.time()
dist_matrix, next_node_matrix, floyd_iters = floyd_warshall(graph, N)
floyd_time = time.time() - start_time
print(f"Флойд-Уоршелл отработал за {floyd_time:.4f} сек. Итераций: {floyd_iters}")

# Восстанавливаем путь
floyd_path = get_path_floyd(next_node_matrix, 0, target)

print(f"Длина пути (Флойд): {dist_matrix[0][target]}")
print(f"Маршрут (Флойд): {floyd_path[:5]} ... {floyd_path[-5:]}")

print("\n--- Сравнение алгоритмов ---")
print(f"Дейкстра (O(E log V)): ~{dijkstra_iters} итераций внутреннего цикла.")
print(f"Флойд-Уоршелл (O(V^3)): {floyd_iters} итераций внутреннего цикла.")

if distances[target] == dist_matrix[0][target] and dijkstra_path == floyd_path:
    print("\nУСПЕХ: Оба алгоритма нашли абсолютно одинаковый и реалистичный кратчайший маршрут!")
