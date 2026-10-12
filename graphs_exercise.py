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


def eulerian_type(graph, directed=False):
    # Directed graph
    if directed:
        in_degree, out_degree = in_out_degree(graph)

        # Check weak connectivity, ignoring isolated vertices
        shadow = {vertex: [] for vertex in graph}

        for vertex, neighbours in graph.items():
            for neighbour in neighbours:
                shadow[vertex].append(neighbour)
                shadow[neighbour].append(vertex)

        active = {
            vertex for vertex in graph
            if in_degree[vertex] + out_degree[vertex] > 0
        }

        for component in connected_components(shadow):
            if component & active and not active.issubset(component):
                return "none"

        # Calculate out-degree minus in-degree
        excess = {
            vertex: out_degree[vertex] - in_degree[vertex]
            for vertex in graph
        }

        if all(value == 0 for value in excess.values()):
            return "circuit"

        if (
            sum(value == 1 for value in excess.values()) == 1
            and sum(value == -1 for value in excess.values()) == 1
            and all(value in (-1, 0, 1) for value in excess.values())
        ):
            return "path"

        return "none"

    # Undirected graph
    deg = degrees(graph)

    # Check connectivity, ignoring isolated vertices
    active = {vertex for vertex in graph if deg[vertex] > 0}

    for component in connected_components(graph):
        if component & active and not active.issubset(component):
            return "none"

    odd = sum(degree % 2 != 0 for degree in deg.values())

    if odd == 0:
        return "circuit"
    if odd == 2:
        return "path"

    return "none"


if __name__ == "__main__":
    print("Task 1:")
    E = [("P1", "P2"), ("P1", "P3"), ("P2", "P3"), ("P3", "P4"), ("P4", "P5")]
    graph = build_adjacency_list(E, directed=True)
    in_deg, out_deg = in_out_degree(graph)

    print(sum(in_deg.values()) == sum(out_deg.values()))
    print(sum(in_deg.values()) == len(E))

    print("Task 3:")
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

    print("Task 4:")
    g1 = build_adjacency_list([("A", "D"), ("A", "I"), ("B", "D"), ("B", "F"), ("B", "G"),
                               ("B", "I"), ("C", "E"), ("C", "H"), ("C", "J"), ("C", "K"),
                               ("D", "F"), ("D", "G"), ("E", "J"), ("H", "J"), ("J", "K")])
    print("G1: ", eulerian_type(g1))
    g3 = build_adjacency_list([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("D", "E"),
                               ("E", "F"), ("F", "G"), ("G", "D")])
    print("G3 :", eulerian_type(g3))
    g4 = build_adjacency_list([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("D", "E"),
                               ("E", "F"), ("G", "D")])
    print("G4 :", eulerian_type(g4))
    g5a = build_adjacency_list([(1,2), (2,3), (3,1), (1,4), (4,1)],True)
    print("G5a: ", eulerian_type(g5a, True))
    g5b = build_adjacency_list([(1, 2), (2, 3), (3, 1), (1, 4)], True)
    print("G5b: ", eulerian_type(g5b, True))
    k = build_adjacency_list([(1,2), (1,2), (1,3), (1,3), (1,4), (2,4), (3,4)])
    print("Konigsberg: ", eulerian_type(k))
