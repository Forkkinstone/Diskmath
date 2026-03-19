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

    # 1. Делаем граф связным (проводим путь через все вершины)
    for i in range(N - 1):
        add_edge(i, i + 1, random.randint(1, 10))

    # 2. Добавляем подграф K_6 (полный граф на 6 вершинах)
    # Выделим под него вершины с 1 по 6
    for i in range(1, 7):
        for j in range(i + 1, 7):
            add_edge(i, j, random.randint(1, 10))

    # 3. Добавляем подграф K_3,5 (двудольный граф)
    # Доли: вершины 10-12 и вершины 13-17
    part1 = [10, 11, 12]
    part2 = [13, 14, 15, 16, 17]
    for u in part1:
        for v in part2:
            add_edge(u, v, random.randint(1, 10))

    # 4. Добиваем граф до нужной степени разреженности (средняя степень n^(1/2))
    # Количество ребер = (N * среднюю_степень) / 2
    target_edges = int(N * math.sqrt(N) / 2)
    current_edges = sum(len(neighbors) for neighbors in graph.values()) // 2

    while current_edges < target_edges:
        u = random.randint(0, N - 1)
        v = random.randint(0, N - 1)
        if u != v and v not in graph[u]:
            add_edge(u, v, random.randint(1, 10))
            current_edges += 1

    print(f"Граф сгенерирован. Вершин: {N}, Ребер: {current_edges}")
    return graph


def dijkstra(graph, start):
    N = len(graph)
    distances = {i: float('inf') for i in range(N)}
    distances[start] = 0
    parents = {i: -1 for i in range(N)}

    # Очередь с приоритетом: (расстояние, вершина)
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
    # ВНИМАНИЕ: Алгоритм O(N^3). На больших N он будет работать вечность.
    # Создаем матрицу смежности
    dist = [[float('inf')] * N for _ in range(N)]
    for i in range(N):
        dist[i][i] = 0
        for v, w in graph[i].items():
            dist[i][v] = w

    iterations = 0
    # Сам алгоритм
    for k in range(N):
        for i in range(N):
            for j in range(N):
                iterations += 1
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist, iterations


# Тестируем на самом маленьком графе из задания, чтобы не ждать часами
N = 1500
graph = generate_graph(N)

# --- Блок Дейкстры ---
print("\nЗапускаем алгоритм Дейкстры...")
start_time = time.time()
distances, parents, dijkstra_iters = dijkstra(graph, 0)
print(f"Дейкстра отработал за {time.time() - start_time:.4f} сек. Итераций: {dijkstra_iters}")

# Восстанавливаем путь от 0 до N-1
target = N - 1
path = []
curr = target
while curr != -1:
    path.append(curr)
    curr = parents[curr]
path.reverse()

print(f"Кратчайший путь от 0 до {target}: {path[:5]} ... {path[-5:]} (показано начало и конец)")
print(f"Длина пути: {distances[target]}")

# --- Блок Флойда-Уоршелла ---
print("\nЗапускаем алгоритм Флойда-Уоршелла...")
start_time = time.time()
_, floyd_iters = floyd_warshall(graph, N)
print(f"Флойд-Уоршелл отработал за {time.time() - start_time:.4f} сек. Итераций: {floyd_iters}")

print("\n--- Сравнение сложности ---")
print(f"Дейкстра (O(E log V)): ~{dijkstra_iters} итераций внутреннего цикла.")
print(f"Флойд-Уоршелл (O(V^3)): {floyd_iters} итераций внутреннего цикла.")
