from collections import deque
from pathlib import Path


POSITIONS = {
    "a": (3, 1),
    "b": (4, 1),
    "c": (3, 2),
    "i": (4, 2),
    "e": (5, 2),
    "f": (1, 3),
    "s": (2, 3),
    "h": (3, 3),
    "k": (4, 3),
    "m": (5, 3),
    "n": (6, 3),
    "p": (1, 4),
    "q": (2, 4),
    "r": (3, 4),
    "t": (4, 4),
    "g": (5, 4),
}

START = "s"
GOAL = "i"

BLOCKED_EDGES = {
    frozenset(("c", "i")),
    frozenset(("h", "k")),
    frozenset(("s", "q")),
    frozenset(("h", "r")),
    frozenset(("k", "t")),
    frozenset(("m", "g")),
}

NEIGHBOR_ORDER = ["up", "right", "down", "left"]
DELTAS = {
    "up": (0, -1),
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0),
}


def build_graph():
    position_to_node = {position: node for node, position in POSITIONS.items()}
    graph = {node: [] for node in POSITIONS}

    for node, (x, y) in POSITIONS.items():
        for direction in NEIGHBOR_ORDER:
            dx, dy = DELTAS[direction]
            neighbor = position_to_node.get((x + dx, y + dy))

            if neighbor is None:
                continue

            if frozenset((node, neighbor)) not in BLOCKED_EDGES:
                graph[node].append(neighbor)

    return graph


def reconstruct_path(parent, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def breadth_first_search(graph, start, goal):
    frontier = deque([start])
    parent = {start: None}
    visited = set()
    exploration_order = []
    steps = []

    while frontier:
        current = frontier.popleft()

        if current in visited:
            continue

        visited.add(current)
        exploration_order.append(current)
        added = []

        if current == goal:
            steps.append({
                "popped": current,
                "added": added,
                "frontier": list(frontier),
                "parents": dict(parent),
            })
            return reconstruct_path(parent, goal), exploration_order, steps

        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current
                frontier.append(neighbor)
                added.append(neighbor)

        steps.append({
            "popped": current,
            "added": added,
            "frontier": list(frontier),
            "parents": dict(parent),
        })

    return None, exploration_order, steps


def format_graph(graph):
    lines = []

    for node in sorted(graph, key=lambda item: (POSITIONS[item][1], POSITIONS[item][0])):
        neighbors = ", ".join(graph[node]) if graph[node] else "-"
        lines.append(f"{node}: {neighbors}")

    return "\n".join(lines)


def format_frontier(frontier):
    if not frontier:
        return "[]"

    return "[" + ", ".join(frontier) + "]"


def format_parents(parent):
    items = []

    for node in sorted(parent, key=lambda item: (POSITIONS[item][1], POSITIONS[item][0])):
        previous = "None" if parent[node] is None else parent[node]
        items.append(f"{node}:{previous}")

    return "{" + ", ".join(items) + "}"


def format_steps(steps):
    headers = ["Buoc", "Lay ra", "Them vao frontier", "Frontier sau buoc", "Parent"]
    rows = []

    for index, step in enumerate(steps, start=1):
        added = ", ".join(step["added"]) if step["added"] else "-"
        rows.append([
            str(index),
            step["popped"],
            added,
            format_frontier(step["frontier"]),
            format_parents(step["parents"]),
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


def solve():
    graph = build_graph()
    path, exploration_order, steps = breadth_first_search(graph, START, GOAL)

    lines = [
        "THUAT TOAN BFS - BREADTH FIRST SEARCH",
        "",
        "Trang thai bat dau:",
        START,
        "",
        "Trang thai dich:",
        GOAL,
        "",
        "Danh sach ke sau khi loai vach ngan:",
        format_graph(graph),
        "",
        "Bang cac buoc BFS:",
        format_steps(steps),
        "",
        "Thu tu trang thai duyet:",
        " -> ".join(exploration_order),
        "",
        "Duong di:",
        "Khong tim thay duong di" if path is None else " -> ".join(path),
        "",
        "So buoc di:",
        "Khong co" if path is None else str(len(path) - 1),
    ]

    return "\n".join(lines)


def main():
    output_text = solve()
    output_file = Path(__file__).resolve().parent / "BFS_out.txt"
    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print()
    print(f"Da luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()