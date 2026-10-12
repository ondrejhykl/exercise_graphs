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


if __name__ == "__main__":
    E = [("P1", "P2"), ("P1", "P3"), ("P2", "P3"), ("P3", "P4"), ("P4", "P5")]
    graph = build_adjacency_list(E, directed=True)
    in_deg, out_deg = in_out_degree(graph)

    print(sum(in_deg.values()) == sum(out_deg.values()))
    print(sum(in_deg.values()) == len(E))



