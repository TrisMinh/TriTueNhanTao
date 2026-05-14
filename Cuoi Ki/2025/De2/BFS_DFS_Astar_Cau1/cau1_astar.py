import csv
import heapq
import math
import os


def heuristic_to_edge(position, n):
    row, col = position

    current = (row, col)
    top_edge = (0, col)
    bottom_edge = (n - 1, col)
    left_edge = (row, 0)
    right_edge = (row, n - 1)

    return min(
        math.dist(current, top_edge),
        math.dist(current, bottom_edge),
        math.dist(current, left_edge),
        math.dist(current, right_edge),
    )


def read_input(file_path):
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = [[int(value) for value in row] for row in reader if row]

    n, start_row, start_col = rows[0]
    maze = rows[1:]

    return n, (start_row, start_col), maze


def is_valid_cell(row, col, n, maze):
    return 0 <= row < n and 0 <= col < n and maze[row][col] == 1


def is_exit(position, n):
    row, col = position
    return row == 0 or row == n - 1 or col == 0 or col == n - 1


def get_neighbors(position, n, maze):
    row, col = position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []

    for d_row, d_col in directions:
        next_row = row + d_row
        next_col = col + d_col
        if is_valid_cell(next_row, next_col, n, maze):
            neighbors.append((next_row, next_col))

    return neighbors


def reconstruct_path(parent, end_position):
    path = []
    current = end_position

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def astar_search(n, start, maze):
    start_row, start_col = start

    if not is_valid_cell(start_row, start_col, n, maze):
        return None, []

    open_set = []
    start_g = 0
    start_h = heuristic_to_edge(start, n)
    heapq.heappush(open_set, (start_g + start_h, start_g, start))

    parent = {start: None}
    g_score = {start: 0}
    closed_set = set()
    selected_order = []

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        if current in closed_set:
            continue

        if g_score.get(current) != current_g:
            continue

        h_current = heuristic_to_edge(current, n)
        selected_order.append((current, current_g, h_current, current_g + h_current))

        if is_exit(current, n):
            return reconstruct_path(parent, current), selected_order

        closed_set.add(current)

        for neighbor in get_neighbors(current, n, maze):
            if neighbor in closed_set:
                continue

            new_g = current_g + 1

            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                parent[neighbor] = current
                h_value = heuristic_to_edge(neighbor, n)
                f_value = new_g + h_value
                heapq.heappush(open_set, (f_value, new_g, neighbor))

    return None, selected_order


def write_output(file_path, path):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if path is None:
            writer.writerow([-1])
            return

        writer.writerow([len(path)])
        for row, col in path:
            writer.writerow([row, col])


def cell_symbol(row, col, maze, start, exit_cell, path_set, selected_set):
    position = (row, col)

    if position == start:
        return "S"
    if position == exit_cell:
        return "E"
    if position in path_set:
        return "*"
    if position in selected_set:
        return "."
    if maze[row][col] == 1:
        return "1"
    return "#"


def build_search_space_text(n, maze, start, path, selected_order):
    path_set = set(path) if path is not None else set()
    selected_set = {item[0] for item in selected_order}
    exit_cell = path[-1] if path is not None else None

    lines = []
    lines.append("CHU THICH")
    lines.append("S: phong trung tam / o bat dau")
    lines.append("E: cua ra tim duoc")
    lines.append("*: duong di cuoi cung")
    lines.append(".: o da duoc A* chon de xet")
    lines.append("1: duong ham co the di nhung khong nam tren duong ket qua")
    lines.append("#: khong co duong ham / khong di duoc")
    lines.append("")
    lines.append("BAN DO KHONG GIAN TIM KIEM")
    lines.append("    " + " ".join(f"{col:2}" for col in range(n)))

    for row in range(n):
        symbols = []
        for col in range(n):
            symbols.append(cell_symbol(row, col, maze, start, exit_cell, path_set, selected_set))
        lines.append(f"{row:2}: " + "  ".join(symbols))

    lines.append("")
    if path is None:
        lines.append("Ket luan: Khong tim thay duong thoat.")
    else:
        lines.append(f"Ket luan: Tim thay duong thoat gom {len(path)} o.")

    lines.append(f"So o A* da chon de xet: {len(selected_order)}")
    return "\n".join(lines)


def print_path_result(path):
    print("KET QUA GHI VAO A_out.csv")

    if path is None:
        print("-1")
        return

    print(len(path))
    for row, col in path:
        print(f"{row},{col}")


def print_search_steps(selected_order):
    print()
    print("BANG CAC BUOC A*")
    print(f"{'step':>4} {'row':>4} {'col':>4} {'g':>4} {'h':>6} {'f':>6}")

    for step, (position, g_value, h_value, f_value) in enumerate(selected_order):
        row, col = position
        print(f"{step:>4} {row:>4} {col:>4} {g_value:>4} {h_value:>6.2f} {f_value:>6.2f}")


def print_report(n, maze, start, path, selected_order):
    print_path_result(path)
    print_search_steps(selected_order)
    print()
    print(build_search_space_text(n, maze, start, path, selected_order))


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, "A_in.csv")
    output_file = os.path.join(current_dir, "A_out.csv")

    n, start, maze = read_input(input_file)
    path, selected_order = astar_search(n, start, maze)
    write_output(output_file, path)
    print_report(n, maze, start, path, selected_order)


if __name__ == "__main__":
    main()
