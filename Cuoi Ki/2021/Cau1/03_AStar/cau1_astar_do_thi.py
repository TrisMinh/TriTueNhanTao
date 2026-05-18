from pathlib import Path
import heapq
import math


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

POSITIONS = {
    "S": (0, 1),
    "A": (1, 2),
    "B": (2, 1),
    "C": (1, 0),
    "D": (3, 2),
    "E": (4, 2),
    "F": (3, 0),
    "G": (5, 1),
    "H": (4, 0),
}


class Graph:
    def __init__(self):
        self.adjacency = {}

    def add_node(self, node):
        if node not in self.adjacency:
            self.adjacency[node] = []

    def add_edge(self, u, v, cost=1):
        self.add_node(u)
        self.add_node(v)
        self.adjacency[u].append((v, cost))
        self.adjacency[v].append((u, cost))

    def sort_neighbors(self, vertex_order):
        for vertex in self.adjacency:
            self.adjacency[vertex].sort(key=lambda item: vertex_order[item[0]])


def build_graph(vertices, edges):
    graph = Graph()

    for vertex in vertices:
        graph.add_node(vertex)

    for u, v in edges:
        graph.add_edge(u, v)

    vertex_order = {vertex: index for index, vertex in enumerate(vertices)}
    graph.sort_neighbors(vertex_order)
    return graph


def heuristic(node, goal):
    x1, y1 = POSITIONS[node]
    x2, y2 = POSITIONS[goal]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def reconstruct_path(parent, start, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path if path[0] == start else None


def format_adjacency(adjacency):
    lines = []

    for vertex in V:
        neighbors = ", ".join(f"{neighbor}({cost})" for neighbor, cost in adjacency[vertex])
        lines.append(f"{vertex}: {neighbors}")

    return "\n".join(lines)


def format_heuristics(goal):
    lines = []

    for vertex in V:
        lines.append(f"h({vertex}) = {heuristic(vertex, goal):.3f}")

    return "\n".join(lines)


def format_frontier(frontier):
    if not frontier:
        return "[]"

    ordered_items = sorted(frontier)
    parts = []

    for f_value, h_value, g_value, _, node in ordered_items:
        parts.append(f"{node}(g={g_value:.0f}, h={h_value:.3f}, f={f_value:.3f})")

    return "[" + ", ".join(parts) + "]"


def format_parent_map(parent):
    items = []

    for vertex in V:
        if vertex in parent:
            previous = parent[vertex]
            previous_text = "None" if previous is None else previous
            items.append(f"{vertex}:{previous_text}")

    return "{" + ", ".join(items) + "}"


def format_astar_steps(steps):
    if not steps:
        return "Khong co buoc A* nao duoc ghi nhan."

    headers = ["Step", "Popped", "g", "h", "f", "Frontier", "Updated", "Parents"]
    rows = []

    for step in steps:
        updated_text = ", ".join(step["updated"]) if step["updated"] else "-"
        rows.append([
            str(step["step"]),
            step["popped"],
            f"{step['g']:.0f}",
            f"{step['h']:.3f}",
            f"{step['f']:.3f}",
            step["frontier"],
            updated_text,
            format_parent_map(step["parents"]),
        ])

    widths = [len(header) for header in headers]

    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    lines = []
    lines.append(" | ".join(headers[index].ljust(widths[index]) for index in range(len(headers))))
    lines.append("-+-".join("-" * width for width in widths))

    for row in rows:
        lines.append(" | ".join(row[index].ljust(widths[index]) for index in range(len(row))))

    return "\n".join(lines)


def astar(adjacency, start, goal):
    frontier = []
    order = 0
    start_h = heuristic(start, goal)
    heapq.heappush(frontier, (start_h, start_h, 0, order, start))

    parent = {start: None}
    g_score = {start: 0}
    visited = set()
    exploration_order = []
    steps = []
    step_no = 0

    while frontier:
        current_f, current_h, current_g, _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        exploration_order.append(current)
        updated = []

        if current == goal:
            step_no += 1
            steps.append({
                "step": step_no,
                "popped": current,
                "g": current_g,
                "h": current_h,
                "f": current_f,
                "frontier": format_frontier(frontier),
                "updated": updated,
                "parents": dict(parent),
            })
            return reconstruct_path(parent, start, goal), exploration_order, steps

        for neighbor, cost in adjacency[current]:
            tentative_g = current_g + cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                h = heuristic(neighbor, goal)
                f = tentative_g + h
                order += 1
                heapq.heappush(frontier, (f, h, tentative_g, order, neighbor))
                updated.append(f"{neighbor}(g={tentative_g:.0f}, h={h:.3f}, f={f:.3f})")

        step_no += 1
        steps.append({
            "step": step_no,
            "popped": current,
            "g": current_g,
            "h": current_h,
            "f": current_f,
            "frontier": format_frontier(frontier),
            "updated": updated,
            "parents": dict(parent),
        })

    return None, exploration_order, steps


def solve():
    graph = build_graph(V, E)
    path, exploration_order, steps = astar(graph.adjacency, "S", "G")

    lines = [
        "THUAT TOAN A*",
        "",
        "Tap dinh V:",
        str(V),
        "",
        "Tap canh E:",
        str(E),
        "",
        "Danh sach ke kem chi phi:",
        format_adjacency(graph.adjacency),
        "",
        "Gia tri heuristic den G:",
        format_heuristics("G"),
        "",
        "Bang cac buoc A*:",
        format_astar_steps(steps),
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
    output_file = current_dir / "AStar_out.txt"

    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print(f"\nDa luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()
