# Câu 1 - Tìm đường đi trên đồ thị bằng UCS

## Đề bài

Cho đồ thị vô hướng `G = (V, E)` như hình. Cần tìm đường đi từ `S` đến `G`. Báo cáo này trình bày thuật toán **UCS - Uniform Cost Search**.

File chương trình:

```text
cau1_ucs_do_thi.py
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
```

### Giải thích chi tiết

UCS dùng cùng tập node `V` và tập cạnh `E` như BFS. Đồ thị được xây dựng bằng class `Graph`:

- `add_node(node)` thêm node.
- `add_edge(u, v, cost=1)` thêm cạnh vô hướng có chi phí.

Vì đề chỉ cho đồ thị thường, không ghi trọng số cạnh, nên em quy ước mỗi cạnh có chi phí bằng `1`.

---

## Thuật toán UCS

### Trả lời: Dán code chính

```python
def ucs(adjacency, start, goal):
    frontier = []
    order = 0
    heapq.heappush(frontier, (0, order, start))

    parent = {start: None}
    cost_so_far = {start: 0}
    visited = set()
    exploration_order = []

    while frontier:
        current_cost, _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        exploration_order.append(current)

        if current == goal:
            return reconstruct_path(parent, start, goal), exploration_order

        for neighbor, edge_cost in adjacency[current]:
            new_cost = current_cost + edge_cost

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                order += 1
                heapq.heappush(frontier, (new_cost, order, neighbor))

    return None, exploration_order
```

### Giải thích chi tiết

UCS luôn chọn node có tổng chi phí nhỏ nhất từ `S` đến node đó để khám phá trước.

Các biến chính:

| Biến | Ý nghĩa |
|---|---|
| `frontier` | Hàng đợi ưu tiên theo chi phí |
| `cost_so_far` | Chi phí tốt nhất đã biết từ `S` đến từng node |
| `parent` | Lưu node cha để truy vết đường đi |
| `visited` | Các node đã được xử lý |
| `exploration_order` | Thứ tự node được khám phá |

Mỗi phần tử trong `frontier` có dạng:

```text
(cost, order, node)
```

Trong đó:

- `cost` là tổng chi phí từ `S` đến node hiện tại.
- `order` giúp ổn định thứ tự khi nhiều node có cùng chi phí.
- `node` là đỉnh đang chờ được khám phá.

Vì mọi cạnh đều có chi phí bằng `1`, UCS trong bài này có hành vi gần giống BFS và tìm được đường đi ít cạnh nhất.

---

## Trả lời: Dán kết quả thực thi

Lệnh chạy:

```powershell
python "2021/Cau1/04_UCS/cau1_ucs_do_thi.py"
```

Kết quả:

```text
THUAT TOAN UCS
Thu tu dinh kham pha:
S -> A -> B -> C -> D -> F -> G

Duong di tu S den G:
S -> B -> G
```

Kết luận: UCS tìm được đường đi từ `S` đến `G` là:

```text
S -> B -> G
```

Đây là đường đi có tổng chi phí nhỏ nhất. Vì mỗi cạnh có chi phí `1`, tổng chi phí của đường đi này là `2`.
