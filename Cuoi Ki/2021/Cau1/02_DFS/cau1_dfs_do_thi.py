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
    return path if path[0] == start else None


def format_parent_map(parent):
    items = []
    for vertex, previous in parent.items():
        previous_text = "None" if previous is None else previous
        items.append(f"{vertex}:{previous_text}")
    return "{" + ", ".join(items) + "}"


def format_dfs_steps(steps):
    if not steps:
        return "Khong co buoc DFS nao duoc ghi nhan."

    headers = ["Step", "Popped", "Stack", "Discovered", "Parents"]
    rows = []

    for step_index, popped, stack_snapshot, discovered_nodes, parent_snapshot in steps:
        stack_text = "[" + ", ".join(stack_snapshot) + "]"
        discovered_text = ", ".join(discovered_nodes) if discovered_nodes else "-"
        parent_text = format_parent_map(parent_snapshot)
        rows.append([
            str(step_index),
            popped,
            stack_text,
            discovered_text,
            parent_text,
        ])

    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def pad(value, width):
        return value.ljust(width)

    lines = []
    lines.append(" | ".join(pad(header, widths[index]) for index, header in enumerate(headers)))
    lines.append("-+-".join("-" * width for width in widths))
    for row in rows:
        lines.append(" | ".join(pad(value, widths[index]) for index, value in enumerate(row)))

    return "\n".join(lines)


def dfs(adjacency, start, goal):
    stack = [start]
    visited = set()
    discovered = {start}
    parent = {start: None}
    exploration_order = []
    steps = []
    step_index = 0

    while stack:
        step_index += 1
        current = stack.pop()

        if current in visited:
            steps.append((step_index, current, list(stack), [], dict(parent)))
            continue

        visited.add(current)
        exploration_order.append(current)

        discovered_this_step = []

        if current == goal:
            steps.append((step_index, current, list(stack), discovered_this_step, dict(parent)))
            return reconstruct_path(parent, start, goal), exploration_order, steps

        for neighbor in reversed(adjacency[current]):
            if neighbor not in discovered:
                discovered.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
                discovered_this_step.append(neighbor)

        steps.append((step_index, current, list(stack), discovered_this_step, dict(parent)))

    return None, exploration_order, steps


def format_adjacency(adjacency):
    lines = ["Danh sach ke:"]
    for vertex in V:
        neighbors = ", ".join(adjacency[vertex])
        lines.append(f"{vertex}: {neighbors}")
    return "\n".join(lines)


def solve():
    graph = build_graph(V, E)
    path, exploration_order, steps = dfs(graph.adjacency, "S", "G")

    lines = [
        "THUAT TOAN DFS",
        "",
        format_adjacency(graph.adjacency),
        "",
        "Bang cac buoc DFS:",
        format_dfs_steps(steps),
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
    output_file = current_dir / "DFS_out.txt"

    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print(f"\nDa luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()
