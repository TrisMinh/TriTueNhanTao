# Câu 1 - Tìm kiếm BFS

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
## Tìm kiếm theo chiều rộng BFS

### Trả lời: Minh hoạ giải thích cách tìm kiếm

BFS duyệt đồ thị theo từng lớp. Thuật toán dùng hàng đợi `queue`: trạng thái nào được đưa vào trước sẽ được lấy ra trước. Vì mỗi bước trong mê cung có cùng chi phí, BFS tìm được đường đi có số bước ít nhất từ `s` đến `i`.

Quy trình chạy BFS trong bài này:

1. Đưa trạng thái bắt đầu `s` vào hàng đợi.
2. Lấy phần tử đầu hàng đợi ra để duyệt.
3. Nếu trạng thái vừa lấy là `i` thì dừng và truy vết đường đi.
4. Nếu chưa phải đích, xét các trạng thái kề hợp lệ theo thứ tự lên, phải, xuống, trái.
5. Bỏ qua cạnh bị vạch đen chặn và trạng thái đã được phát hiện trước đó.
6. Với mỗi trạng thái mới, lưu `parent` để biết nó đi từ đâu tới.
7. Đưa các trạng thái mới vào cuối hàng đợi.
8. Lặp lại đến khi tìm thấy `i` hoặc hàng đợi rỗng.

Bảng các bước chạy BFS:

```text
Buoc | Lay ra | Them vao frontier | Frontier sau buoc | Parent                                                    
-----+--------+-------------------+-------------------+-----------------------------------------------------------
1    | s      | h, f              | [h, f]            | {f:s, s:None, h:s}                                        
2    | h      | c                 | [f, c]            | {c:h, f:s, s:None, h:s}                                   
3    | f      | p                 | [c, p]            | {c:h, f:s, s:None, h:s, p:f}                              
4    | c      | a                 | [p, a]            | {a:c, c:h, f:s, s:None, h:s, p:f}                         
5    | p      | q                 | [a, q]            | {a:c, c:h, f:s, s:None, h:s, p:f, q:p}                    
6    | a      | b                 | [q, b]            | {a:c, b:a, c:h, f:s, s:None, h:s, p:f, q:p}               
7    | q      | r                 | [b, r]            | {a:c, b:a, c:h, f:s, s:None, h:s, p:f, q:p, r:q}          
8    | b      | i                 | [r, i]            | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q}     
9    | r      | t                 | [i, t]            | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q, t:r}
10   | i      | -                 | [t]               | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q, t:r}
```

Thứ tự trạng thái được duyệt:

```text
s -> h -> f -> c -> p -> a -> q -> b -> r -> i
```

Đường đi tìm được:

```text
s -> h -> c -> a -> b -> i
```

Số bước đi: `5`.

Nhận xét: BFS duyệt cả hai nhánh gần `s` theo từng lớp, nên thứ tự duyệt có cả `h` và `f`. Đường đi cuối cùng được truy vết qua bảng `parent` là đường có số cạnh ít nhất.

## Giải thích tác dụng của từng hàm

| Hàm | Tác dụng |
|---|---|
| `build_graph` | Chuyển mê cung thành danh sách kề và loại các cạnh bị vạch đen chặn. |
| `reconstruct_path` | Truy vết đường đi từ `i` về `s` bằng dictionary `parent`. |
| `breadth_first_search` | Cài đặt BFS bằng hàng đợi `deque`. |
| `format_graph` | Định dạng danh sách kề để ghi ra output. |
| `format_frontier` | Hiển thị hàng đợi frontier tại mỗi bước. |
| `format_parents` | Hiển thị quan hệ cha-con của các trạng thái đã phát hiện. |
| `format_steps` | Tạo bảng mô phỏng từng vòng lặp BFS. |
| `solve` | Gọi thuật toán và gom nội dung kết quả. |
| `main` | Chạy chương trình, ghi kết quả ra `BFS_out.txt`. |

### Trả lời: Dán code hoàn thiện
```python
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
```

## Kết quả chạy chương trình

```text
THUAT TOAN BFS - BREADTH FIRST SEARCH

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

Bang cac buoc BFS:
Buoc | Lay ra | Them vao frontier | Frontier sau buoc | Parent                                                    
-----+--------+-------------------+-------------------+-----------------------------------------------------------
1    | s      | h, f              | [h, f]            | {f:s, s:None, h:s}                                        
2    | h      | c                 | [f, c]            | {c:h, f:s, s:None, h:s}                                   
3    | f      | p                 | [c, p]            | {c:h, f:s, s:None, h:s, p:f}                              
4    | c      | a                 | [p, a]            | {a:c, c:h, f:s, s:None, h:s, p:f}                         
5    | p      | q                 | [a, q]            | {a:c, c:h, f:s, s:None, h:s, p:f, q:p}                    
6    | a      | b                 | [q, b]            | {a:c, b:a, c:h, f:s, s:None, h:s, p:f, q:p}               
7    | q      | r                 | [b, r]            | {a:c, b:a, c:h, f:s, s:None, h:s, p:f, q:p, r:q}          
8    | b      | i                 | [r, i]            | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q}     
9    | r      | t                 | [i, t]            | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q, t:r}
10   | i      | -                 | [t]               | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q, t:r}

Thu tu trang thai duyet:
s -> h -> f -> c -> p -> a -> q -> b -> r -> i

Duong di:
s -> h -> c -> a -> b -> i

So buoc di:
5
```
