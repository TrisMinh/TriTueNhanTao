from pathlib import Path
import heapq


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


def format_frontier(frontier):
    if not frontier:
        return "[]"

    ordered_items = sorted(frontier)
    parts = []

    for cost, _, node in ordered_items:
        parts.append(f"{node}(cost={cost})")

    return "[" + ", ".join(parts) + "]"


def format_parent_map(parent):
    items = []

    for vertex in V:
        if vertex in parent:
            previous = parent[vertex]
            previous_text = "None" if previous is None else previous
            items.append(f"{vertex}:{previous_text}")

    return "{" + ", ".join(items) + "}"


def format_ucs_steps(steps):
    if not steps:
        return "Khong co buoc UCS nao duoc ghi nhan."

    headers = ["Step", "Popped", "Cost", "Frontier", "Updated", "Parents"]
    rows = []

    for step in steps:
        updated_text = ", ".join(step["updated"]) if step["updated"] else "-"
        rows.append([
            str(step["step"]),
            step["popped"],
            str(step["cost"]),
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


def ucs(adjacency, start, goal):
    frontier = []
    order = 0
    heapq.heappush(frontier, (0, order, start))

    parent = {start: None}
    cost_so_far = {start: 0}
    visited = set()
    exploration_order = []
    steps = []
    step_no = 0

    while frontier:
        current_cost, _, current = heapq.heappop(frontier)

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
                "cost": current_cost,
                "frontier": format_frontier(frontier),
                "updated": updated,
                "parents": dict(parent),
            })
            return reconstruct_path(parent, start, goal), exploration_order, steps

        for neighbor, edge_cost in adjacency[current]:
            new_cost = current_cost + edge_cost

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                order += 1
                heapq.heappush(frontier, (new_cost, order, neighbor))
                updated.append(f"{neighbor}(cost={new_cost})")

        step_no += 1
        steps.append({
            "step": step_no,
            "popped": current,
            "cost": current_cost,
            "frontier": format_frontier(frontier),
            "updated": updated,
            "parents": dict(parent),
        })

    return None, exploration_order, steps


def solve():
    graph = build_graph(V, E)
    path, exploration_order, steps = ucs(graph.adjacency, "S", "G")

    lines = [
        "THUAT TOAN UCS",
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
        "Bang cac buoc UCS:",
        format_ucs_steps(steps),
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
    output_file = current_dir / "UCS_out.txt"

    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print(f"\nDa luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()
