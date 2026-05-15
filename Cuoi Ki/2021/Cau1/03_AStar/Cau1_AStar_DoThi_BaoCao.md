# Câu 1 - Tìm đường đi trên đồ thị bằng A*

## Đề bài

Cho đồ thị vô hướng `G = (V, E)` như hình. Cần tìm đường đi từ `S` đến `G`. Báo cáo này trình bày thuật toán **A\***.

File chương trình:

```text
cau1_astar_do_thi.py
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

Đồ thị vẫn được xây dựng bằng `Graph`, `add_node` và `add_edge`. Riêng A* cần thêm hàm heuristic nên chương trình khai báo `POSITIONS` để gán tọa độ gần đúng cho từng node dựa trên vị trí của node trong hình vẽ.

Các cạnh trong bài không có trọng số riêng nên mỗi cạnh được xem có chi phí bằng `1`.

---

## Thuật toán A*

### Trả lời: Dán code chính

```python
def heuristic(node, goal):
    x1, y1 = POSITIONS[node]
    x2, y2 = POSITIONS[goal]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def astar(adjacency, start, goal):
    frontier = []
    order = 0
    start_h = heuristic(start, goal)
    heapq.heappush(frontier, (start_h, start_h, 0, order, start))

    parent = {start: None}
    g_score = {start: 0}
    visited = set()
    exploration_order = []

    while frontier:
        _, _, current_g, _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        exploration_order.append(current)

        if current == goal:
            return reconstruct_path(parent, start, goal), exploration_order

        for neighbor, cost in adjacency[current]:
            tentative_g = current_g + cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                h = heuristic(neighbor, goal)
                f = tentative_g + h
                order += 1
                heapq.heappush(frontier, (f, h, tentative_g, order, neighbor))

    return None, exploration_order
```

### Giải thích chi tiết

A* dùng hàm đánh giá:

```text
f(n) = g(n) + h(n)
```

Trong đó:

- `g(n)` là chi phí thật từ `S` đến node `n`.
- `h(n)` là chi phí ước lượng từ node `n` đến đích `G`.
- `f(n)` là tổng chi phí dùng để ưu tiên node cần khám phá.

Với đồ thị trong hình, em dùng khoảng cách Euclid làm heuristic:

```text
h(n) = sqrt((x_n - x_G)^2 + (y_n - y_G)^2)
```

Ví dụ:

```text
h(B) = sqrt((2 - 5)^2 + (1 - 1)^2) = 3
h(G) = 0
```

Khi đứng tại `S`, các node kề là `A`, `B`, `C`. Node `B` có vẻ gần `G` nhất theo heuristic, đồng thời có cạnh trực tiếp đến `G`, nên A* nhanh chóng tìm được đường:

```text
S -> B -> G
```

A* khác Greedy ở chỗ A* không chỉ nhìn `h(n)`, mà còn cộng thêm `g(n)`, tức chi phí thật đã đi.

---

## Trả lời: Dán kết quả thực thi

Lệnh chạy:

```powershell
python "2021/Cau1/03_AStar/cau1_astar_do_thi.py"
```

Kết quả:

```text
THUAT TOAN A*
Thu tu dinh kham pha:
S -> B -> G

Duong di tu S den G:
S -> B -> G
```

Kết luận: A* tìm được đường đi ngắn từ `S` đến `G` là:

```text
S -> B -> G
```

Trong lần chạy này, A* chỉ cần khám phá 3 node: `S`, `B`, `G`.
