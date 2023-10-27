import heapq
import copy


def dijkstra(graph, start, end=None):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {node: None for node in graph}
    queue = [(0, start)]

    while queue:
        (distance, current) = heapq.heappop(queue)
        if distance > distances[current]:
            continue
        if current == end:
            return distances, parent
        for neighbor, cost in graph[current].items():
            new_distance = distance + cost
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parent[neighbor] = current
                heapq.heappush(queue, (new_distance, neighbor))

    return distances, parent


def get_shortest_path(parent, end):
    path = [end]
    node = end
    while node is not None:
        node = parent[node]
        if node is not None:
            path.append(node)

    return path[::-1]


def add(path, degree_num):
    k = 30                               # degree에 대한 할당 값 단위 초
    C = 20                               # 단위 초
    init = 0

    for i in path:                       # 마지막 vertex는 도착하는 곳 이니깐 교차로 걸리는 시간 안구함
        if degree_num[i] - 2 <= 0:       # 시간 = C + k(d-2)
            init += C
        else:
            init += (C + (degree_num[i] - 2) * k)

    return init



def find_quickest_path(graph, start, vertices_time):
    distances = {vertex: float('inf') for vertex in graph}
    previous_vertices = {vertex: None for vertex in graph}
    distances[start] = vertices_time[start]
    vertices = [(distances[start], start)]

    while vertices:
        (current_distance, current_vertex) = heapq.heappop(vertices)

        # 이미 처리된 노드를 스킵
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight + vertices_time[neighbor]

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(vertices, (distance, neighbor))

    return distances, previous_vertices


def get_quickest_path(previous_vertices, end):
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        next_vertex = previous_vertices[current_vertex]
        current_vertex = next_vertex
    path = path[::-1]

    return path


def make_vertices_time(graph, degree_num):
    vertices_time = {}

    k    = 30  # degree에 대한 할당 값 단위 초
    C    = 20  # 단위 초

    for i in graph.keys():
        if degree_num[i] - 2 <= 0:
            vertices_time[i] = C
        else:
            vertices_time[i] = (C + (degree_num[i] - 2) * k)

    return vertices_time


def yen_algorithm(graph, source, dest, k):
    yen_graph = copy.deepcopy(graph)

    A = []
    B = []

    # Compute the shortest path from the source to the destination
    distances, parent = dijkstra(yen_graph, source, dest)
    shortest_path = get_shortest_path(parent, dest)
    A.append(shortest_path)

    for i in range(1, k):
        for j in range(len(A[i - 1]) - 1):
            # Remove edges from the graph
            spur_node = A[i - 1][j]
            root_path = A[i - 1][:j + 1]

            for path in A:
                if len(path) > j and root_path == path[:j + 1]:
                    yen_graph[root_path[-1]].pop(path[j + 1], None)

            for path in B:
                if len(path) > j and root_path == path[:j + 1]:
                    yen_graph[root_path[-1]].pop(path[j + 1], None)

            # Compute the spur path
            distances, parent = dijkstra(yen_graph, spur_node, dest)
            if dest in parent and parent[dest] is not None:
                spur_path = get_shortest_path(parent, dest)
                total_path = root_path[:-1] + spur_path
                B.append(total_path)

            # Restore edges to the graph
            for path in A:
                if len(path) > j and root_path == path[:j + 1]:
                    yen_graph[root_path[-1]][path[j + 1]] = distances[path[j + 1]]

            for path in B:
                if len(path) > j and root_path == path[:j + 1]:
                    yen_graph[root_path[-1]][path[j + 1]] = distances[path[j + 1]]

        if not B:
            break

        B.sort(key=lambda x: sum(yen_graph[x[i]][x[i + 1]] for i in range(len(x) - 1)))
        A.append(B[0])
        B.pop(0)

    return A