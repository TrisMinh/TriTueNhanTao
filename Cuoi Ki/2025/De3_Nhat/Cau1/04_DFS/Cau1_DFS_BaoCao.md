# Câu 1 - Tìm kiếm DFS

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
## Tìm kiếm theo chiều sâu DFS

### Trả lời: Minh hoạ giải thích cách tìm kiếm

DFS duyệt đồ thị bằng cách đi sâu theo một nhánh trước khi quay lui. Thuật toán dùng `stack`: trạng thái nào được đưa vào sau sẽ được lấy ra trước. DFS không đảm bảo đường đi ngắn nhất, kết quả phụ thuộc vào thứ tự xét hàng xóm.

Trong code, thứ tự xét hàng xóm vẫn là `Lên -> Phải -> Xuống -> Trái`. Khi đưa vào stack, chương trình đẩy ngược thứ tự để trạng thái ưu tiên đầu tiên nằm ở đỉnh stack và được lấy ra trước.

Quy trình chạy DFS trong bài này:

1. Đưa trạng thái bắt đầu `s` vào stack.
2. Lấy trạng thái ở đỉnh stack ra để duyệt.
3. Nếu trạng thái vừa lấy là `i` thì dừng và truy vết đường đi.
4. Nếu chưa phải đích, xét các trạng thái kề hợp lệ theo thứ tự đã quy định.
5. Bỏ qua cạnh bị vạch đen chặn và trạng thái đã được phát hiện.
6. Lưu `parent` cho mỗi trạng thái mới.
7. Đưa các trạng thái mới vào stack sao cho trạng thái ưu tiên được lấy ra trước.
8. Lặp lại đến khi tìm thấy `i` hoặc stack rỗng.

Bảng các bước chạy DFS:

```text
Buoc | Lay ra | Them vao stack | Stack sau buoc | Parent                                
-----+--------+----------------+----------------+---------------------------------------
1    | s      | h, f           | [f, h]         | {f:s, s:None, h:s}                    
2    | h      | c              | [f, c]         | {c:h, f:s, s:None, h:s}               
3    | c      | a              | [f, a]         | {a:c, c:h, f:s, s:None, h:s}          
4    | a      | b              | [f, b]         | {a:c, b:a, c:h, f:s, s:None, h:s}     
5    | b      | i              | [f, i]         | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}
6    | i      | -              | [f]            | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}
```

Thứ tự trạng thái được duyệt:

```text
s -> h -> c -> a -> b -> i
```

Đường đi tìm được:

```text
s -> h -> c -> a -> b -> i
```

Số bước đi: `5`.

Nhận xét: DFS đi sâu ngay theo nhánh `s -> h -> c -> a -> b`. Do nhánh này dẫn tới `i`, thuật toán dừng mà chưa cần mở rộng nhánh `f`.

## Giải thích tác dụng của từng hàm

| Hàm | Tác dụng |
|---|---|
| `build_graph` | Chuyển mê cung thành danh sách kề và loại các cạnh bị vạch đen chặn. |
| `reconstruct_path` | Truy vết đường đi từ đích về trạng thái bắt đầu. |
| `depth_first_search` | Cài đặt DFS bằng stack. |
| `format_graph` | Định dạng danh sách kề để ghi ra output. |
| `format_frontier` | Hiển thị stack tại mỗi bước. |
| `format_parents` | Hiển thị bảng cha để kiểm tra đường đi. |
| `format_steps` | Tạo bảng mô phỏng từng vòng lặp DFS. |
| `solve` | Chạy DFS và gom nội dung kết quả. |
| `main` | Chạy chương trình, ghi kết quả ra `DFS_out.txt`. |

### Trả lời: Dán code hoàn thiện
```python
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


def depth_first_search(graph, start, goal):
    frontier = [start]
    parent = {start: None}
    visited = set()
    exploration_order = []
    steps = []

    while frontier:
        current = frontier.pop()

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

        candidates = [
            neighbor for neighbor in graph[current]
            if neighbor not in visited and neighbor not in parent
        ]

        for neighbor in reversed(candidates):
            parent[neighbor] = current
            frontier.append(neighbor)

        added = candidates
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
    headers = ["Buoc", "Lay ra", "Them vao stack", "Stack sau buoc", "Parent"]
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
    path, exploration_order, steps = depth_first_search(graph, START, GOAL)

    lines = [
        "THUAT TOAN DFS - DEPTH FIRST SEARCH",
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
        "Ghi chu stack:",
        "Phan tu ben phai la dinh stack va se duoc lay ra truoc.",
        "",
        "Bang cac buoc DFS:",
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
    output_file = Path(__file__).resolve().parent / "DFS_out.txt"
    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print()
    print(f"Da luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()
```

## Kết quả chạy chương trình

```text
THUAT TOAN DFS - DEPTH FIRST SEARCH

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

Ghi chu stack:
Phan tu ben phai la dinh stack va se duoc lay ra truoc.

Bang cac buoc DFS:
Buoc | Lay ra | Them vao stack | Stack sau buoc | Parent                                
-----+--------+----------------+----------------+---------------------------------------
1    | s      | h, f           | [f, h]         | {f:s, s:None, h:s}                    
2    | h      | c              | [f, c]         | {c:h, f:s, s:None, h:s}               
3    | c      | a              | [f, a]         | {a:c, c:h, f:s, s:None, h:s}          
4    | a      | b              | [f, b]         | {a:c, b:a, c:h, f:s, s:None, h:s}     
5    | b      | i              | [f, i]         | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}
6    | i      | -              | [f]            | {a:c, b:a, c:h, i:b, f:s, s:None, h:s}

Thu tu trang thai duyet:
s -> h -> c -> a -> b -> i

Duong di:
s -> h -> c -> a -> b -> i

So buoc di:
5
```
