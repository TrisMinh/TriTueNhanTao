from pathlib import Path
import heapq


V = ["S", "A", "B", "C", "D", "E", "F", "G", "H", "K", "M", "N", "I", "J", "L", "Z"]

H = {
    "S": 10,
    "A": 9,
    "B": 8,
    "C": 7,
    "D": 6,
    "E": 5,
    "F": 4,
    "G": 10,
    "H": 10,
    "K": 3,
    "M": 0,
    "N": 10,
    "I": 6,
    "J": 0,
    "L": 9,
    "Z": 8,
}

E = [
    ("S", "A", 5),
    ("S", "B", 6),
    ("S", "C", 5),
    ("A", "D", 6),
    ("A", "E", 7),
    ("D", "M", 5),
    ("D", "N", 8),
    ("E", "I", 8),
    ("B", "F", 3),
    ("B", "G", 4),
    ("F", "J", 4),
    ("F", "L", 4),
    ("C", "H", 6),
    ("C", "K", 4),
    ("K", "Z", 2),
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


def astar_to_zero_heuristic_goal(graph, start):
    frontier = []
    order = 0
    start_h = graph.heuristic[start]
    heapq.heappush(frontier, (start_h, start_h, 0, order, start))

    parent = {start: None}
    g_score = {start: 0}
    visited = set()
    exploration_order = []
    steps = []

    while frontier:
        frontier_before = list(frontier)
        _, _, current_g, _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        exploration_order.append(current)

        if graph.heuristic[current] == 0:
            path = reconstruct_path(parent, start, current)
            steps.append({
                "frontier_before": frontier_before,
                "current": current,
                "g": current_g,
                "h": graph.heuristic[current],
                "f": current_g + graph.heuristic[current],
                "added": [],
                "frontier_after": list(frontier),
                "note": "Dung vi h = 0",
            })
            return path, current, current_g, exploration_order, steps

        added = []
        for neighbor, edge_cost in graph.adjacency[current]:
            if neighbor in visited:
                continue

            tentative_g = current_g + edge_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                h = graph.heuristic[neighbor]
                f = tentative_g + h
                order += 1
                heapq.heappush(frontier, (f, h, tentative_g, order, neighbor))
                added.append((neighbor, tentative_g, h, f))

        steps.append({
            "frontier_before": frontier_before,
            "current": current,
            "g": current_g,
            "h": graph.heuristic[current],
            "f": current_g + graph.heuristic[current],
            "added": added,
            "frontier_after": list(frontier),
            "note": "",
        })

    return None, None, None, exploration_order, steps


def format_frontier_astar(frontier):
    ordered = sorted(frontier)
    return "[" + ", ".join(f"{node}(g={g}, h={h}, f={f})" for f, h, g, _, node in ordered) + "]"


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
        added = ", ".join(
            f"{node}(g={g}, h={h}, f={f})" for node, g, h, f in step["added"]
        ) if step["added"] else "Khong co"
        current = f"{step['current']}(g={step['g']}, h={step['h']}, f={step['f']})"
        rows.append([
            index,
            format_frontier_astar(step["frontier_before"]),
            current,
            added,
            format_frontier_astar(step["frontier_after"]),
        ])
    return "\n".join([
        "Bang trang thai:",
        make_table(headers, rows),
        "Dung khi lay ra dinh co h = 0.",
    ])


def format_edges(edges):
    return "\n".join(f"{u} -- {v}: cost = {cost}" for u, v, cost in edges)


def format_heuristics(heuristic_values):
    return "\n".join(f"h({node}) = {heuristic_values[node]}" for node in V)


def solve():
    graph = build_graph(V, E, H)
    path, goal, total_cost, exploration_order, steps = astar_to_zero_heuristic_goal(graph, "S")

    lines = [
        "Tap dinh V:",
        str(V),
        "",
        "Trong so tren dinh H:",
        format_heuristics(H),
        "",
        "Tap canh E va chi phi tren canh:",
        format_edges(E),
        "",
        "THUAT TOAN A*",
        "Thu tu dinh kham pha:",
        " -> ".join(exploration_order),
        "",
        format_steps(steps),
        "",
    ]

    if path is None:
        lines.append("Khong tim thay duong di")
    else:
        lines.extend([
            f"Dinh dich tim duoc: {goal}",
            f"Tong chi phi duong di: {total_cost}",
            "Duong di tu S den dinh co h = 0:",
            " -> ".join(path),
        ])

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
