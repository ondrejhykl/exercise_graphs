def build_adjacency_list(edges, directed=False):
    graph = {}
    for u, v in edges:
        if u not in graph.keys():
            graph[u] = []
        if v not in graph.keys():
            graph[v] = []

        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph


def degrees(graph):
    deg = {}
    for vertex, neighbours in graph.items():
        deg[vertex] = len(neighbours)
    return deg


def in_out_degree(graph):
    in_degree = {}
    out_degree = {}
    for vertex in graph.keys():
        in_degree[vertex] = 0
    for vertex, neighbours in graph.items():
        out_degree[vertex] = len(neighbours)
        for neighbour in neighbours:
            in_degree[neighbour] += 1
    return in_degree, out_degree


def dfs(graph, start):
    visited = set()
    order = []

    def visit(vertex):
        visited.add(vertex)
        order.append(vertex)

        for neighbour in sorted(graph[vertex]):
            if neighbour not in visited:
                visit(neighbour)

    visit(start)
    return order


def connected_components(graph):
    components = []
    visited = set()

    for vertex in graph:
        if vertex not in visited:
            component = set(dfs(graph, vertex))
            components.append(component)
            visited.update(component)
    return components


def is_weakly_connected(graph):
    shadow = {vertex: [] for vertex in graph}

    for vertex, neighbours in graph.items():
        for neighbour in neighbours:
            shadow[vertex].append(neighbour)
            shadow[neighbour].append(vertex)

    return len(connected_components(shadow)) == 1


if __name__ == "__main__":
    print("Task 1:")
    E = [("P1", "P2"), ("P1", "P3"), ("P2", "P3"), ("P3", "P4"), ("P4", "P5")]
    graph = build_adjacency_list(E, directed=True)
    in_deg, out_deg = in_out_degree(graph)

    print(sum(in_deg.values()) == sum(out_deg.values()))
    print(sum(in_deg.values()) == len(E))

    print("Task 2:")
    graph = {
        "a": ["b", "c"],
        "b": ["a", "d", "e"],
        "c": ["a"],
        "d": ["b"],
        "e": ["b"]
    }

    print("DFS:", dfs(graph, "a"))
    # Expected: ['a', 'b', 'd', 'e', 'c']

    # Test connected components
    graph2 = {
        "a": ["b"],
        "b": ["a"],
        "c": ["d"],
        "d": ["c"],
        "e": []
    }

    print("Connected components:", connected_components(graph2))
    # Expected: [{'a', 'b'}, {'c', 'd'}, {'e'}]

    # Test weakly connected
    graph3 = {
        "a": ["b"],
        "b": ["c"],
        "c": []
    }
    print(connected_components(graph3))
    print("Weakly connected:", is_weakly_connected(graph3))
    # Expected: True

    graph4 = {
        "a": ["b"],
        "b": [],
        "c": []
    }
    print(connected_components(graph4))
    print("Weakly connected:", is_weakly_connected(graph4))
    # Expected: False

