# Câu 1b - Tìm kiếm A* dùng heuristic Manhattan

## Đề bài

Cho mê cung như hình. Đường in đậm màu đen biểu diễn vạch ngăn không đi qua được. Yêu cầu tìm đường đi từ trạng thái `s` đến trạng thái `i`.

Trong bài này:

- Mỗi ô có nhãn là một trạng thái, tương ứng với một đỉnh của đồ thị.
- Hai trạng thái có cạnh nối nếu hai ô kề nhau theo 4 hướng lên, phải, xuống, trái và giữa chúng không có vạch ngăn.
- Trạng thái bắt đầu: `s = (2,3)`.
- Trạng thái đích: `i = (4,2)`.

## Biểu diễn mê cung thành đồ thị

Bảng tọa độ các trạng thái:

| Trạng thái | Tọa độ | Trạng thái | Tọa độ |
|---|---:|---|---:|
| `a` | `(3,1)` | `b` | `(4,1)` |
| `c` | `(3,2)` | `i` | `(4,2)` |
| `e` | `(5,2)` | `f` | `(1,3)` |
| `s` | `(2,3)` | `h` | `(3,3)` |
| `k` | `(4,3)` | `m` | `(5,3)` |
| `n` | `(6,3)` | `p` | `(1,4)` |
| `q` | `(2,4)` | `r` | `(3,4)` |
| `t` | `(4,4)` | `g` | `(5,4)` |

Các cạnh bị chặn bởi vạch đen:

```python
BLOCKED_EDGES = {
    frozenset(("c", "i")),
    frozenset(("h", "k")),
    frozenset(("s", "q")),
    frozenset(("h", "r")),
    frozenset(("k", "t")),
    frozenset(("m", "g")),
}
```

Danh sách kề sau khi loại các cạnh bị vạch ngăn:

```text
a: b, c
b: i, a
c: a, h
i: b, e, k
e: m, i
f: s, p
s: h, f
h: c, s
k: i, m
m: e, n, k
n: m
p: f, q
q: r, p
r: t, q
t: g, r
g: t
```

Thứ tự xét hàng xóm trong chương trình là: `Lên -> Phải -> Xuống -> Trái`.

## Heuristic Manhattan

Với trạng thái hiện tại `n = (x1, y1)` và đích `i = (x2, y2)`, khoảng cách Manhattan được tính bằng:

```text
h(n) = |x1 - x2| + |y1 - y2|
```

Vì đích là `i = (4,2)`, một số giá trị quan trọng là:

```text
h(s) = |2-4| + |3-2| = 3
h(h) = |3-4| + |3-2| = 2
h(c) = |3-4| + |2-2| = 1
h(a) = |3-4| + |1-2| = 2
h(b) = |4-4| + |1-2| = 1
h(i) = 0
```
## b) Tìm kiếm A*, sử dụng heuristic khoảng cách Manhattan

### Trả lời: Minh hoạ giải thích cách tìm kiếm

A* là thuật toán tìm kiếm có thông tin, kết hợp chi phí đã đi và heuristic còn lại. Với mỗi trạng thái `n`, thuật toán tính:

```text
f(n) = g(n) + h(n)
```

Trong đó:

- `g(n)` là chi phí từ trạng thái bắt đầu `s` đến `n`.
- `h(n)` là khoảng cách Manhattan ước lượng từ `n` đến đích `i`.
- `f(n)` là tổng chi phí ước lượng, dùng để chọn trạng thái tiếp theo.

Quy trình chạy A* trong bài này:

1. Khởi tạo `frontier` với `s`, có `g(s)=0`, `h(s)=3`, `f(s)=3`.
2. Lấy trạng thái có `f` nhỏ nhất ra khỏi `frontier`.
3. Nếu trạng thái vừa lấy là `i` thì dừng và truy vết đường đi.
4. Nếu chưa phải đích, sinh các trạng thái kề hợp lệ, không đi qua vạch đen.
5. Với mỗi trạng thái kề, tính `tentative_g = g(current) + 1` vì mỗi bước đi có chi phí 1.
6. Tính `h` theo Manhattan và `f = g + h`.
7. Nếu tìm được đường tốt hơn đến trạng thái kề, cập nhật `parent`, `g_score` và đưa trạng thái đó vào `frontier`.
8. Lặp lại đến khi lấy được `i` hoặc `frontier` rỗng.

Bảng các bước chạy A*:

```text
Buoc | Lay ra | g | h | f | Them vao frontier                  | Frontier sau buoc                    | Parent                                
-----+--------+---+---+---+------------------------------------+--------------------------------------+---------------------------------------
1    | s      | 0 | 3 | 3 | h(g=1, h=2, f=3), f(g=1, h=4, f=5) | [h(g=1, h=2, f=3), f(g=1, h=4, f=5)] | {f:s, s:None, h:s}                    
2    | h      | 1 | 2 | 3 | c(g=2, h=1, f=3)                   | [c(g=2, h=1, f=3), f(g=1, h=4, f=5)] | {c:h, f:s, s:None, h:s}               
3    | c      | 2 | 1 | 3 | a(g=3, h=2, f=5)                   | [a(g=3, h=2, f=5), f(g=1, h=4, f=5)] | {a:c, c:h, f:s, s:None, h:s}          
4    | a      | 3 | 2 | 5 | b(g=4, h=1, f=5)                   | [b(g=4, h=1, f=5), f(g=1, h=4, f=5)] | {a:c, b:a, c:h, f:s, s:None, h:s}     
5    | b      | 4 | 1 | 5 | i(g=5, h=0, f=5)                   | [i(g=5, h=0, f=5), f(g=1, h=4, f=5)] | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}
6    | i      | 5 | 0 | 5 | -                                  | [f(g=1, h=4, f=5)]                   | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}
```

Thứ tự trạng thái được duyệt:

```text
s -> h -> c -> a -> b -> i
```

Đường đi tìm được:

```text
s -> h -> c -> a -> b -> i
```

Chi phí đường đi:

```text
g(i) = 5
```

Nhận xét: A* không chỉ nhìn trạng thái nào gần đích theo `h`, mà còn xét chi phí đã đi `g`. Vì vậy `f = g + h` giúp thuật toán cân bằng giữa đường đã đi và khoảng cách ước lượng còn lại.

## Giải thích tác dụng của từng hàm

| Hàm | Tác dụng |
|---|---|
| `manhattan_distance` | Tính heuristic Manhattan từ một trạng thái đến đích. |
| `build_graph` | Tạo đồ thị từ mê cung, bỏ các cạnh bị vạch ngăn màu đen chặn. |
| `reconstruct_path` | Truy vết đường đi sau khi tìm thấy đích. |
| `astar_search` | Cài đặt thuật toán A*, dùng hàng đợi ưu tiên theo `f(n)=g(n)+h(n)`. |
| `format_graph` | Định dạng danh sách kề của đồ thị. |
| `format_heuristics` | In giá trị `h` của từng trạng thái. |
| `format_frontier` | Hiển thị frontier cùng `g`, `h`, `f` của từng trạng thái. |
| `format_parents` | Hiển thị quan hệ cha-con để kiểm tra đường đi. |
| `format_steps` | Tạo bảng mô phỏng từng vòng lặp A*. |
| `solve` | Chạy thuật toán và gom nội dung kết quả. |
| `main` | Ghi kết quả ra `AStar_out.txt` và in ra màn hình. |

### Trả lời: Dán code hoàn thiện
```python
import heapq
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


def manhattan_distance(node, goal):
    x1, y1 = POSITIONS[node]
    x2, y2 = POSITIONS[goal]
    return abs(x1 - x2) + abs(y1 - y2)


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


def astar_search(graph, start, goal):
    frontier = []
    order = 0
    start_h = manhattan_distance(start, goal)
    heapq.heappush(frontier, (start_h, start_h, 0, order, start))

    parent = {start: None}
    g_score = {start: 0}
    visited = set()
    exploration_order = []
    steps = []

    while frontier:
        current_f, current_h, current_g, _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        exploration_order.append(current)
        added = []

        if current == goal:
            steps.append({
                "popped": current,
                "g": current_g,
                "h": current_h,
                "f": current_f,
                "added": added,
                "frontier": list(frontier),
                "parents": dict(parent),
            })
            return reconstruct_path(parent, goal), exploration_order, steps

        for neighbor in graph[current]:
            tentative_g = current_g + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                neighbor_h = manhattan_distance(neighbor, goal)
                neighbor_f = tentative_g + neighbor_h
                order += 1
                heapq.heappush(frontier, (neighbor_f, neighbor_h, tentative_g, order, neighbor))
                added.append((neighbor, tentative_g, neighbor_h, neighbor_f))

        steps.append({
            "popped": current,
            "g": current_g,
            "h": current_h,
            "f": current_f,
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


def format_heuristics():
    lines = []

    for node in sorted(POSITIONS, key=lambda item: (POSITIONS[item][1], POSITIONS[item][0])):
        lines.append(f"h({node}) = {manhattan_distance(node, GOAL)}")

    return "\n".join(lines)


def format_frontier(frontier):
    if not frontier:
        return "[]"

    return "[" + ", ".join(
        f"{node}(g={g}, h={h}, f={f})" for f, h, g, _, node in sorted(frontier)
    ) + "]"


def format_parents(parent):
    items = []

    for node in sorted(parent, key=lambda item: (POSITIONS[item][1], POSITIONS[item][0])):
        previous = "None" if parent[node] is None else parent[node]
        items.append(f"{node}:{previous}")

    return "{" + ", ".join(items) + "}"


def format_steps(steps):
    headers = ["Buoc", "Lay ra", "g", "h", "f", "Them vao frontier", "Frontier sau buoc", "Parent"]
    rows = []

    for index, step in enumerate(steps, start=1):
        added = ", ".join(
            f"{node}(g={g}, h={h}, f={f})" for node, g, h, f in step["added"]
        ) if step["added"] else "-"
        rows.append([
            str(index),
            step["popped"],
            str(step["g"]),
            str(step["h"]),
            str(step["f"]),
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
    path, exploration_order, steps = astar_search(graph, START, GOAL)

    lines = [
        "THUAT TOAN A* - MANHATTAN",
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
        "Gia tri heuristic Manhattan:",
        format_heuristics(),
        "",
        "Bang cac buoc A*:",
        format_steps(steps),
        "",
        "Thu tu trang thai duyet:",
        " -> ".join(exploration_order),
        "",
        "Duong di:",
        "Khong tim thay duong di" if path is None else " -> ".join(path),
    ]

    return "\n".join(lines)


def main():
    output_text = solve()
    output_file = Path(__file__).resolve().parent / "AStar_out.txt"
    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print()
    print(f"Da luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()

```

## Kết quả chạy chương trình

```text
THUAT TOAN A* - MANHATTAN

Trang thai bat dau:
s

Trang thai dich:
i

Danh sach ke sau khi loai vach ngan:
a: b, c
b: i, a
c: a, h
i: b, e, k
e: m, i
f: s, p
s: h, f
h: c, s
k: i, m
m: e, n, k
n: m
p: f, q
q: r, p
r: t, q
t: g, r
g: t

Gia tri heuristic Manhattan:
h(a) = 2
h(b) = 1
h(c) = 1
h(i) = 0
h(e) = 1
h(f) = 4
h(s) = 3
h(h) = 2
h(k) = 1
h(m) = 2
h(n) = 3
h(p) = 5
h(q) = 4
h(r) = 3
h(t) = 2
h(g) = 3

Bang cac buoc A*:
Buoc | Lay ra | g | h | f | Them vao frontier                  | Frontier sau buoc                    | Parent                                
-----+--------+---+---+---+------------------------------------+--------------------------------------+---------------------------------------
1    | s      | 0 | 3 | 3 | h(g=1, h=2, f=3), f(g=1, h=4, f=5) | [h(g=1, h=2, f=3), f(g=1, h=4, f=5)] | {f:s, s:None, h:s}                    
2    | h      | 1 | 2 | 3 | c(g=2, h=1, f=3)                   | [c(g=2, h=1, f=3), f(g=1, h=4, f=5)] | {c:h, f:s, s:None, h:s}               
3    | c      | 2 | 1 | 3 | a(g=3, h=2, f=5)                   | [a(g=3, h=2, f=5), f(g=1, h=4, f=5)] | {a:c, c:h, f:s, s:None, h:s}          
4    | a      | 3 | 2 | 5 | b(g=4, h=1, f=5)                   | [b(g=4, h=1, f=5), f(g=1, h=4, f=5)] | {a:c, b:a, c:h, f:s, s:None, h:s}     
5    | b      | 4 | 1 | 5 | i(g=5, h=0, f=5)                   | [i(g=5, h=0, f=5), f(g=1, h=4, f=5)] | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}
6    | i      | 5 | 0 | 5 | -                                  | [f(g=1, h=4, f=5)]                   | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}

Thu tu trang thai duyet:
s -> h -> c -> a -> b -> i

Duong di:
s -> h -> c -> a -> b -> i
```
