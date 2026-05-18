# Câu 1a - Tìm kiếm tham lam Greedy dùng heuristic Manhattan

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
## a) Tìm kiếm tham lam Greedy, sử dụng heuristic khoảng cách Manhattan

### Trả lời: Minh hoạ giải thích cách tìm kiếm

Greedy Best First Search là thuật toán tìm kiếm có thông tin. Thuật toán chỉ dùng heuristic `h(n)` để quyết định trạng thái nào được mở rộng tiếp theo. Trạng thái có `h(n)` nhỏ nhất sẽ được ưu tiên lấy ra khỏi `frontier` trước.

Quy trình chạy Greedy trong bài này:

1. Khởi tạo `frontier` với trạng thái bắt đầu `s`.
2. Tính `h(s)` theo công thức Manhattan đến đích `i`.
3. Lấy trạng thái có `h` nhỏ nhất ra khỏi `frontier`.
4. Nếu trạng thái vừa lấy là `i` thì dừng và truy vết đường đi bằng bảng `parent`.
5. Nếu chưa phải đích, sinh các trạng thái kề hợp lệ theo thứ tự lên, phải, xuống, trái.
6. Bỏ qua những cạnh bị vạch đen chặn và những trạng thái đã thăm.
7. Với mỗi trạng thái mới, tính `h`, lưu cha của nó, rồi đưa vào `frontier`.
8. Lặp lại đến khi gặp `i` hoặc `frontier` rỗng.

Bảng các bước chạy Greedy:

```text
Buoc | Lay ra | h | Them vao frontier | Frontier sau buoc | Parent                                
-----+--------+---+-------------------+-------------------+---------------------------------------
1    | s      | 3 | h(h=2), f(h=4)    | [h(h=2), f(h=4)]  | {f:s, s:None, h:s}                    
2    | h      | 2 | c(h=1)            | [c(h=1), f(h=4)]  | {c:h, f:s, s:None, h:s}               
3    | c      | 1 | a(h=2)            | [a(h=2), f(h=4)]  | {a:c, c:h, f:s, s:None, h:s}          
4    | a      | 2 | b(h=1)            | [b(h=1), f(h=4)]  | {a:c, b:a, c:h, f:s, s:None, h:s}     
5    | b      | 1 | i(h=0)            | [i(h=0), f(h=4)]  | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}
6    | i      | 0 | -                 | [f(h=4)]          | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}
```

Thứ tự trạng thái được duyệt:

```text
s -> h -> c -> a -> b -> i
```

Đường đi tìm được:

```text
s -> h -> c -> a -> b -> i
```

Nhận xét: từ `s`, thuật toán có thể đi đến `h` hoặc `f`. Vì `h(h)=2` nhỏ hơn `h(f)=4`, Greedy chọn `h` trước. Sau đó thuật toán luôn ưu tiên trạng thái có heuristic nhỏ nhất nên đi theo nhánh `s -> h -> c -> a -> b -> i`.

## Giải thích tác dụng của từng hàm

| Hàm | Tác dụng |
|---|---|
| `manhattan_distance` | Tính khoảng cách Manhattan từ một trạng thái đến đích. |
| `build_graph` | Chuyển mê cung thành danh sách kề, đồng thời loại các cạnh bị vạch đen chặn. |
| `reconstruct_path` | Truy vết đường đi từ đích về `s` dựa trên dictionary `parent`. |
| `greedy_best_first_search` | Cài đặt vòng lặp Greedy, dùng hàng đợi ưu tiên theo `h(n)`. |
| `format_graph` | Định dạng danh sách kề để ghi vào file kết quả. |
| `format_heuristics` | In giá trị heuristic của từng trạng thái. |
| `format_frontier` | Hiển thị các trạng thái còn trong frontier cùng giá trị `h`. |
| `format_parents` | Hiển thị bảng cha để kiểm tra quá trình truy vết đường đi. |
| `format_steps` | Tạo bảng từng bước chạy thuật toán. |
| `solve` | Gọi các hàm chính, gom nội dung báo cáo kết quả. |
| `main` | Chạy chương trình và ghi kết quả ra `Greedy_out.txt`. |

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


def greedy_best_first_search(graph, start, goal):
    frontier = []
    order = 0
    heapq.heappush(frontier, (manhattan_distance(start, goal), order, start))

    parent = {start: None}
    visited = set()
    exploration_order = []
    steps = []

    while frontier:
        current_h, _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        exploration_order.append(current)
        added = []

        if current == goal:
            steps.append({
                "popped": current,
                "h": current_h,
                "added": added,
                "frontier": list(frontier),
                "parents": dict(parent),
            })
            return reconstruct_path(parent, goal), exploration_order, steps

        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current
                order += 1
                neighbor_h = manhattan_distance(neighbor, goal)
                heapq.heappush(frontier, (neighbor_h, order, neighbor))
                added.append((neighbor, neighbor_h))

        steps.append({
            "popped": current,
            "h": current_h,
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

    return "[" + ", ".join(f"{node}(h={h})" for h, _, node in sorted(frontier)) + "]"


def format_parents(parent):
    items = []

    for node in sorted(parent, key=lambda item: (POSITIONS[item][1], POSITIONS[item][0])):
        previous = "None" if parent[node] is None else parent[node]
        items.append(f"{node}:{previous}")

    return "{" + ", ".join(items) + "}"


def format_steps(steps):
    headers = ["Buoc", "Lay ra", "h", "Them vao frontier", "Frontier sau buoc", "Parent"]
    rows = []

    for index, step in enumerate(steps, start=1):
        added = ", ".join(f"{node}(h={h})" for node, h in step["added"]) if step["added"] else "-"
        rows.append([
            str(index),
            step["popped"],
            str(step["h"]),
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
    path, exploration_order, steps = greedy_best_first_search(graph, START, GOAL)

    lines = [
        "THUAT TOAN GREEDY BEST FIRST SEARCH - MANHATTAN",
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
        "Bang cac buoc Greedy:",
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
    output_file = Path(__file__).resolve().parent / "Greedy_out.txt"
    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print()
    print(f"Da luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()

```

## Kết quả chạy chương trình

```text
THUAT TOAN GREEDY BEST FIRST SEARCH - MANHATTAN

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

Bang cac buoc Greedy:
Buoc | Lay ra | h | Them vao frontier | Frontier sau buoc | Parent                                
-----+--------+---+-------------------+-------------------+---------------------------------------
1    | s      | 3 | h(h=2), f(h=4)    | [h(h=2), f(h=4)]  | {f:s, s:None, h:s}                    
2    | h      | 2 | c(h=1)            | [c(h=1), f(h=4)]  | {c:h, f:s, s:None, h:s}               
3    | c      | 1 | a(h=2)            | [a(h=2), f(h=4)]  | {a:c, c:h, f:s, s:None, h:s}          
4    | a      | 2 | b(h=1)            | [b(h=1), f(h=4)]  | {a:c, b:a, c:h, f:s, s:None, h:s}     
5    | b      | 1 | i(h=0)            | [i(h=0), f(h=4)]  | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}
6    | i      | 0 | -                 | [f(h=4)]          | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}

Thu tu trang thai duyet:
s -> h -> c -> a -> b -> i

Duong di:
s -> h -> c -> a -> b -> i
```
