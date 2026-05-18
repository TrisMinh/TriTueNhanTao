from pathlib import Path
import heapq


V = ["S", "A", "B", "C", "D", "E", "F", "G", "H", "K", "M", "N", "I", "J", "L", "Z"]

H = {
    "S": 10, "A": 9, "B": 8, "C": 7, "D": 6, "E": 5, "F": 4, "G": 10,
    "H": 10, "K": 3, "M": 0, "N": 10, "I": 6, "J": 0, "L": 9, "Z": 8,
}

E = [
    ("S", "A", 5), ("S", "B", 6), ("S", "C", 5), ("A", "D", 6),
    ("A", "E", 7), ("D", "M", 5), ("D", "N", 8), ("E", "I", 8),
    ("B", "F", 3), ("B", "G", 4), ("F", "J", 4), ("F", "L", 4),
    ("C", "H", 6), ("C", "K", 4), ("K", "Z", 2),
]


class Graph:
    def __init__(self):
        self.adjacency = {}
        self.heuristic = {}

    def add_node(self, node, heuristic_value):
        if node not in self.adjacency:
            self.adjacency[node] = []
        self.heuristic[node] = heuristic_value

    def add_edge(self, u, v, cost):
        self.adjacency[u].append((v, cost))
        self.adjacency[v].append((u, cost))

    def sort_neighbors(self, vertex_order):
        for node in self.adjacency:
            self.adjacency[node].sort(key=lambda item: vertex_order[item[0]])


def build_graph(vertices, edges, heuristic_values):
    graph = Graph()
    for vertex in vertices:
        graph.add_node(vertex, heuristic_values[vertex])
    for u, v, cost in edges:
        graph.add_edge(u, v, cost)
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


def ucs_to_zero_heuristic_goals(graph, start):
    frontier = []
    order = 0
    heapq.heappush(frontier, (0, order, start))
    parent = {start: None}
    cost_so_far = {start: 0}
    visited = set()
    exploration_order = []
    steps = []
    goals = []

    while frontier:
        frontier_before = list(frontier)
        current_cost, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        exploration_order.append(current)

        if graph.heuristic[current] == 0:
            path = reconstruct_path(parent, start, current)
            goals.append({
                "goal": current,
                "path": path,
                "cost": current_cost,
            })
            steps.append({
                "frontier_before": frontier_before,
                "current": current,
                "g": current_cost,
                "h": graph.heuristic[current],
                "added": [],
                "frontier_after": list(frontier),
                "note": "Ghi nhan dinh dich h = 0",
            })
            continue

        added = []
        for neighbor, edge_cost in graph.adjacency[current]:
            if neighbor in visited:
                continue
            new_cost = current_cost + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                order += 1
                heapq.heappush(frontier, (new_cost, order, neighbor))
                added.append((neighbor, new_cost))

        steps.append({
            "frontier_before": frontier_before,
            "current": current,
            "g": current_cost,
            "h": graph.heuristic[current],
            "added": added,
            "frontier_after": list(frontier),
            "note": "",
        })

    return goals, exploration_order, steps


def format_frontier_ucs(frontier):
    ordered = sorted(frontier)
    return "[" + ", ".join(f"{node}(g={cost})" for cost, _, node in ordered) + "]"


def make_table(headers, rows):
    widths = [
        max(len(str(row[index])) for row in [headers] + rows)
        for index in range(len(headers))
    ]
    separator = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(row):
        cells = [
            str(value).ljust(widths[index])
            for index, value in enumerate(row)
        ]
        return "| " + " | ".join(cells) + " |"

    lines = [separator, format_row(headers), separator]
    lines.extend(format_row(row) for row in rows)
    lines.append(separator)
    return "\n".join(lines)


def format_steps(steps):
    headers = ["Buoc", "Frontier truoc", "Lay ra", "Them vao", "Frontier sau"]
    rows = []
    for index, step in enumerate(steps, start=1):
        added = ", ".join(f"{node}(g={cost})" for node, cost in step["added"]) if step["added"] else "Khong co"
        current = f"{step['current']}(g={step['g']}, h={step['h']})"
        rows.append([
            index,
            format_frontier_ucs(step["frontier_before"]),
            current,
            added,
            format_frontier_ucs(step["frontier_after"]),
        ])
    return "\n".join([
        "Bang trang thai:",
        make_table(headers, rows),
        "Ghi nhan moi dinh co h = 0 va tiep tuc cho den khi frontier rong.",
    ])


def solve():
    graph = build_graph(V, E, H)
    goals, exploration_order, steps = ucs_to_zero_heuristic_goals(graph, "S")
    lines = [
        "THUAT TOAN UCS",
        "Thu tu dinh kham pha:",
        " -> ".join(exploration_order),
        "",
        format_steps(steps),
        "",
    ]
    if not goals:
        lines.append("Khong tim thay duong di")
    else:
        lines.append("Cac dinh dich tim duoc:")
        lines.append(", ".join(item["goal"] for item in goals))
        lines.append("Cac duong di tu S den cac dinh co h = 0:")
        for item in goals:
            lines.append(f'{item["goal"]}: { " -> ".join(item["path"]) } | Tong chi phi = {item["cost"]}')
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
