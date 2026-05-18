# Câu 1 - Tìm kiếm UCS

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
## Tìm kiếm chi phí cực tiểu UCS

### Trả lời: Minh hoạ giải thích cách tìm kiếm

UCS mở rộng trạng thái có tổng chi phí từ `s` đến trạng thái đó nhỏ nhất. Thuật toán dùng hàng đợi ưu tiên theo `g(n)`, trong đó `g(n)` là chi phí đã đi từ trạng thái bắt đầu đến `n`.

Trong bài mê cung này, mỗi bước đi có chi phí bằng `1`, nên:

```text
g(neighbor) = g(current) + 1
```

Vì mọi cạnh có cùng chi phí, UCS sẽ tìm đường có tổng chi phí nhỏ nhất và thường cho đường đi có độ dài giống BFS.

Quy trình chạy UCS trong bài này:

1. Đưa trạng thái bắt đầu `s` vào hàng đợi ưu tiên với `g(s)=0`.
2. Lấy trạng thái có `g` nhỏ nhất ra khỏi frontier.
3. Nếu trạng thái vừa lấy là `i` thì dừng và truy vết đường đi.
4. Nếu chưa phải đích, sinh các trạng thái kề hợp lệ, không đi qua vạch đen.
5. Tính chi phí mới `new_cost = g(current) + 1`.
6. Nếu trạng thái kề chưa có chi phí hoặc tìm được chi phí nhỏ hơn, cập nhật `parent` và `cost_so_far`.
7. Đưa trạng thái kề vào hàng đợi ưu tiên theo chi phí mới.
8. Lặp lại đến khi lấy được `i` hoặc frontier rỗng.

Bảng các bước chạy UCS:

```text
Buoc | Lay ra | g | Them vao frontier | Frontier sau buoc | Parent                                                    
-----+--------+---+-------------------+-------------------+-----------------------------------------------------------
1    | s      | 0 | h(g=1), f(g=1)    | [h(g=1), f(g=1)]  | {f:s, s:None, h:s}                                        
2    | h      | 1 | c(g=2)            | [f(g=1), c(g=2)]  | {c:h, f:s, s:None, h:s}                                   
3    | f      | 1 | p(g=2)            | [c(g=2), p(g=2)]  | {c:h, f:s, s:None, h:s, p:f}                              
4    | c      | 2 | a(g=3)            | [p(g=2), a(g=3)]  | {a:c, c:h, f:s, s:None, h:s, p:f}                         
5    | p      | 2 | q(g=3)            | [a(g=3), q(g=3)]  | {a:c, c:h, f:s, s:None, h:s, p:f, q:p}                    
6    | a      | 3 | b(g=4)            | [q(g=3), b(g=4)]  | {a:c, b:a, c:h, f:s, s:None, h:s, p:f, q:p}               
7    | q      | 3 | r(g=4)            | [b(g=4), r(g=4)]  | {a:c, b:a, c:h, f:s, s:None, h:s, p:f, q:p, r:q}          
8    | b      | 4 | i(g=5)            | [r(g=4), i(g=5)]  | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q}     
9    | r      | 4 | t(g=5)            | [i(g=5), t(g=5)]  | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q, t:r}
10   | i      | 5 | -                 | [t(g=5)]          | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q, t:r}
```

Thứ tự trạng thái được duyệt:

```text
s -> h -> f -> c -> p -> a -> q -> b -> r -> i
```

Đường đi tìm được:

```text
s -> h -> c -> a -> b -> i
```

Tổng chi phí: `5`.

Nhận xét: UCS ưu tiên trạng thái có chi phí đường đi nhỏ nhất. Vì mỗi cạnh đều có chi phí `1`, thứ tự mở rộng của UCS gần với BFS và đường đi tìm được có tổng chi phí nhỏ nhất.

## Giải thích tác dụng của từng hàm

| Hàm | Tác dụng |
|---|---|
| `build_graph` | Chuyển mê cung thành danh sách kề và loại các cạnh bị vạch đen chặn. |
| `reconstruct_path` | Truy vết đường đi bằng dictionary `parent`. |
| `uniform_cost_search` | Cài đặt UCS bằng hàng đợi ưu tiên theo `g(n)`. |
| `format_graph` | Định dạng danh sách kề để ghi ra output. |
| `format_frontier` | Hiển thị frontier cùng chi phí `g`. |
| `format_parents` | Hiển thị quan hệ cha-con của các trạng thái. |
| `format_steps` | Tạo bảng mô phỏng từng vòng lặp UCS. |
| `solve` | Chạy UCS và gom nội dung kết quả. |
| `main` | Chạy chương trình, ghi kết quả ra `UCS_out.txt`. |

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
STEP_COST = 1

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


def uniform_cost_search(graph, start, goal):
    frontier = []
    order = 0
    heapq.heappush(frontier, (0, order, start))

    parent = {start: None}
    cost_so_far = {start: 0}
    visited = set()
    exploration_order = []
    steps = []

    while frontier:
        current_cost, _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        exploration_order.append(current)
        added = []

        if current == goal:
            steps.append({
                "popped": current,
                "cost": current_cost,
                "added": added,
                "frontier": list(frontier),
                "parents": dict(parent),
            })
            return reconstruct_path(parent, goal), exploration_order, steps, current_cost

        for neighbor in graph[current]:
            new_cost = current_cost + STEP_COST

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                order += 1
                heapq.heappush(frontier, (new_cost, order, neighbor))
                added.append((neighbor, new_cost))

        steps.append({
            "popped": current,
            "cost": current_cost,
            "added": added,
            "frontier": list(frontier),
            "parents": dict(parent),
        })

    return None, exploration_order, steps, None


def format_graph(graph):
    lines = []

    for node in sorted(graph, key=lambda item: (POSITIONS[item][1], POSITIONS[item][0])):
        neighbors = ", ".join(graph[node]) if graph[node] else "-"
        lines.append(f"{node}: {neighbors}")

    return "\n".join(lines)


def format_frontier(frontier):
    if not frontier:
        return "[]"

    return "[" + ", ".join(f"{node}(g={cost})" for cost, _, node in sorted(frontier)) + "]"


def format_parents(parent):
    items = []

    for node in sorted(parent, key=lambda item: (POSITIONS[item][1], POSITIONS[item][0])):
        previous = "None" if parent[node] is None else parent[node]
        items.append(f"{node}:{previous}")

    return "{" + ", ".join(items) + "}"


def format_steps(steps):
    headers = ["Buoc", "Lay ra", "g", "Them vao frontier", "Frontier sau buoc", "Parent"]
    rows = []

    for index, step in enumerate(steps, start=1):
        added = ", ".join(f"{node}(g={cost})" for node, cost in step["added"]) if step["added"] else "-"
        rows.append([
            str(index),
            step["popped"],
            str(step["cost"]),
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
    path, exploration_order, steps, total_cost = uniform_cost_search(graph, START, GOAL)

    lines = [
        "THUAT TOAN UCS - UNIFORM COST SEARCH",
        "",
        "Trang thai bat dau:",
        START,
        "",
        "Trang thai dich:",
        GOAL,
        "",
        "Chi phi moi buoc di:",
        str(STEP_COST),
        "",
        "Danh sach ke sau khi loai vach ngan:",
        format_graph(graph),
        "",
        "Bang cac buoc UCS:",
        format_steps(steps),
        "",
        "Thu tu trang thai duyet:",
        " -> ".join(exploration_order),
        "",
        "Duong di:",
        "Khong tim thay duong di" if path is None else " -> ".join(path),
        "",
        "Tong chi phi:",
        "Khong co" if total_cost is None else str(total_cost),
    ]

    return "\n".join(lines)


def main():
    output_text = solve()
    output_file = Path(__file__).resolve().parent / "UCS_out.txt"
    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print()
    print(f"Da luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()
```

## Kết quả chạy chương trình

```text
THUAT TOAN UCS - UNIFORM COST SEARCH

Trang thai bat dau:
s

Trang thai dich:
i

Chi phi moi buoc di:
1

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

Bang cac buoc UCS:
Buoc | Lay ra | g | Them vao frontier | Frontier sau buoc | Parent                                                    
-----+--------+---+-------------------+-------------------+-----------------------------------------------------------
1    | s      | 0 | h(g=1), f(g=1)    | [h(g=1), f(g=1)]  | {f:s, s:None, h:s}                                        
2    | h      | 1 | c(g=2)            | [f(g=1), c(g=2)]  | {c:h, f:s, s:None, h:s}                                   
3    | f      | 1 | p(g=2)            | [c(g=2), p(g=2)]  | {c:h, f:s, s:None, h:s, p:f}                              
4    | c      | 2 | a(g=3)            | [p(g=2), a(g=3)]  | {a:c, c:h, f:s, s:None, h:s, p:f}                         
5    | p      | 2 | q(g=3)            | [a(g=3), q(g=3)]  | {a:c, c:h, f:s, s:None, h:s, p:f, q:p}                    
6    | a      | 3 | b(g=4)            | [q(g=3), b(g=4)]  | {a:c, b:a, c:h, f:s, s:None, h:s, p:f, q:p}               
7    | q      | 3 | r(g=4)            | [b(g=4), r(g=4)]  | {a:c, b:a, c:h, f:s, s:None, h:s, p:f, q:p, r:q}          
8    | b      | 4 | i(g=5)            | [r(g=4), i(g=5)]  | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q}     
9    | r      | 4 | t(g=5)            | [i(g=5), t(g=5)]  | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q, t:r}
10   | i      | 5 | -                 | [t(g=5)]          | {a:c, b:a, c:h, i:b, f:s, s:None, h:s, p:f, q:p, r:q, t:r}

Thu tu trang thai duyet:
s -> h -> f -> c -> p -> a -> q -> b -> r -> i

Duong di:
s -> h -> c -> a -> b -> i

Tong chi phi:
5
```
