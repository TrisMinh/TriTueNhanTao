from collections import deque
from pathlib import Path


V = ["S", "A", "B", "C", "D", "E", "F", "G", "H"]

E = [
    ("S", "A"),
    ("S", "B"),
    ("S", "C"),
    ("A", "B"),
    ("A", "D"),
    ("B", "C"),
    ("B", "D"),
    ("B", "F"),
    ("B", "G"),
    ("C", "F"),
    ("D", "E"),
    ("E", "F"),
    ("E", "G"),
    ("F", "H"),
    ("G", "H"),
]


class Graph:
    def __init__(self):
        self.adjacency = {}

    def add_node(self, node):
        if node not in self.adjacency:
            self.adjacency[node] = []

    def add_edge(self, u, v):
        self.add_node(u)
        self.add_node(v)
        self.adjacency[u].append(v)
        self.adjacency[v].append(u)

    def sort_neighbors(self, vertex_order):
        for vertex in self.adjacency:
            self.adjacency[vertex].sort(key=lambda item: vertex_order[item])


def build_graph(vertices, edges):
    graph = Graph()

    for vertex in vertices:
        graph.add_node(vertex)

    for u, v in edges:
        graph.add_edge(u, v)

    vertex_order = {vertex: index for index, vertex in enumerate(vertices)}
    graph.sort_neighbors(vertex_order)
    return graph


def reconstruct_path(parent, start, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    if path[0] == start:
        return path

    return None


def bfs(adjacency, start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    exploration_order = []

    while queue:
        current = queue.popleft()
        exploration_order.append(current)

        if current == goal:
            return reconstruct_path(parent, start, goal), exploration_order

        for neighbor in adjacency[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None, exploration_order


def format_adjacency(adjacency):
    lines = []

    for vertex in V:
        neighbors = ", ".join(adjacency[vertex])
        lines.append(f"{vertex}: {neighbors}")

    return "\n".join(lines)


def solve():
    graph = build_graph(V, E)
    adjacency = graph.adjacency
    path, exploration_order = bfs(adjacency, "S", "G")

    lines = [
        "Tap dinh V:",
        str(V),
        "",
        "Tap canh E:",
        str(E),
        "",
        "Danh sach ke:",
        format_adjacency(adjacency),
        "",
        "Thu tu dinh kham pha:",
        " -> ".join(exploration_order),
        "",
    ]

    if path is None:
        lines.append("Khong tim thay duong di")
    else:
        lines.append("Duong di tu S den G:")
        lines.append(" -> ".join(path))

    return "\n".join(lines)


def main():
    current_dir = Path(__file__).resolve().parent
    output_text = solve()
    output_file = current_dir / "BFS_out.txt"

    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print(f"\nDa luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()
