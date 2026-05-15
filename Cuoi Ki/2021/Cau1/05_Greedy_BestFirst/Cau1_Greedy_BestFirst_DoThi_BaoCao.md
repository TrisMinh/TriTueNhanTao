# Câu 1 - Tìm đường đi trên đồ thị bằng Greedy Best First Search

## Đề bài

Cho đồ thị vô hướng `G = (V, E)` như hình. Cần tìm đường đi từ đỉnh `S` đến đỉnh `G`. Báo cáo này trình bày thuật toán **Greedy Best First Search**.

File chương trình:

```text
cau1_greedy_best_first_do_thi.py
```

---

## Biểu diễn đồ thị

### Trả lời: Dán code biểu diễn đồ thị

```python
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

POSITIONS = {
    "S": (0, 1),
    "A": (1, 2),
    "B": (2, 1),
    "C": (1, 0),
    "D": (3, 2),
    "E": (4, 2),
    "F": (3, 0),
    "G": (5, 1),
    "H": (4, 0),
}
```

### Giải thích chi tiết

Greedy Best First Search cần một hàm heuristic để ước lượng node nào gần đích hơn. Vì vậy ngoài `V` và `E`, chương trình dùng thêm `POSITIONS`, tức tọa độ gần đúng của từng node theo hình vẽ.

Đồ thị vẫn được xây dựng thống nhất bằng:

- `add_node(node)` để thêm node.
- `add_edge(u, v)` để thêm cạnh vô hướng.

---

## Thuật toán Greedy Best First Search

### Trả lời: Dán code chính

```python
def heuristic(node, goal):
    x1, y1 = POSITIONS[node]
    x2, y2 = POSITIONS[goal]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def greedy_best_first(adjacency, start, goal):
    frontier = []
    order = 0
    heapq.heappush(frontier, (heuristic(start, goal), order, start))

    parent = {start: None}
    visited = set()
    discovered = {start}
    exploration_order = []

    while frontier:
        _, _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        exploration_order.append(current)

        if current == goal:
            return reconstruct_path(parent, start, goal), exploration_order

        for neighbor in adjacency[current]:
            if neighbor not in discovered:
                discovered.add(neighbor)
                parent[neighbor] = current
                order += 1
                heapq.heappush(frontier, (heuristic(neighbor, goal), order, neighbor))

    return None, exploration_order
```

### Giải thích chi tiết

Greedy Best First Search chọn node tiếp theo chỉ dựa vào heuristic:

```text
priority(n) = h(n)
```

Trong chương trình:

```text
h(n) = khoảng cách Euclid từ node n đến G
```

Công thức:

```text
h(n) = sqrt((x_n - x_G)^2 + (y_n - y_G)^2)
```

Ví dụ:

```text
h(B) = sqrt((2 - 5)^2 + (1 - 1)^2) = 3
h(A) = sqrt((1 - 5)^2 + (2 - 1)^2) = sqrt(17)
h(C) = sqrt((1 - 5)^2 + (0 - 1)^2) = sqrt(17)
```

Từ `S`, các node kề là `A`, `B`, `C`. Vì `B` có heuristic nhỏ nhất nên Greedy chọn `B` trước. Từ `B` có cạnh trực tiếp đến `G`, nên thuật toán tìm được đường:

```text
S -> B -> G
```

Khác với A*, Greedy không cộng chi phí đã đi `g(n)`. Vì vậy Greedy thường chạy nhanh, nhưng không đảm bảo luôn tìm được đường đi tối ưu trong mọi đồ thị.

---

## Trả lời: Dán kết quả thực thi

Lệnh chạy:

```powershell
python "2021/Cau1/05_Greedy_BestFirst/cau1_greedy_best_first_do_thi.py"
```

Kết quả:

```text
THUAT TOAN GREEDY BEST FIRST SEARCH
Thu tu dinh kham pha:
S -> B -> G

Duong di tu S den G:
S -> B -> G
```

Kết luận: Greedy Best First Search tìm được đường đi:

```text
S -> B -> G
```

Trong ví dụ này, heuristic dẫn thẳng đến node `B`, nên thuật toán chỉ khám phá 3 node.
