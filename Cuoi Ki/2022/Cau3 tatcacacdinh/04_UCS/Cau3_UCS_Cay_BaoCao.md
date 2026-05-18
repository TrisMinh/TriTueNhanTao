# Câu 3 - Tìm đường đi trên cây bằng UCS

## Đề bài

Cho cây có trọng số trên đỉnh và trọng số trên cạnh. Cần tìm đường từ `S` đến một đỉnh có trọng số trên đỉnh bằng `0`.

Báo cáo này trình bày thuật toán **UCS - Uniform Cost Search**.

File chương trình:

```text
cau3_ucs_cay.py
```

---

## a) Biểu diễn cây

### Trả lời: Dán code vào bên dưới

```python
V = ["S", "A", "B", "C", "D", "E", "F", "G", "H", "K", "M", "N", "I", "J", "L", "Z"]

H = {
    "S": 10, "A": 9, "B": 8, "C": 7, "D": 6, "E": 5, "F": 4, "G": 10,
    "H": 10, "K": 3, "M": 0, "N": 10, "I": 6, "J": 0, "L": 9, "Z": 8,
}

E = [
    ("S", "A", 5), ("S", "B", 6), ("S", "C", 5), ("A", "D", 6),
    ("A", "E", 7), ("D", "M", 5), ("D", "N", 8), ("E", "I", 8),
    ("B", "F", 3), ("B", "G", 4), ("F", "J", 4), ("F", "L", 4),
    ("C", "H", 6), ("C", "K", 4), ("K", "Z", 2),
]
```

### Giải thích

UCS cần trọng số cạnh để tính chi phí thật từ `S` đến từng đỉnh. Vì vậy mỗi cạnh trong `E` có dạng `(u, v, cost)`. Trọng số đỉnh `H` vẫn được lưu để xác định trạng thái đích: đỉnh nào có `h = 0` thì là đích.

Đồ thị được xây dựng bằng `Graph`, `add_node` và `add_edge`, tương tự các thuật toán còn lại.

---

## b) Thuật toán UCS

### Trả lời: Dán code vào bên dưới

```python
def ucs_to_zero_heuristic_goal(graph, start):
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

        if graph.heuristic[current] == 0:
            path = reconstruct_path(parent, start, current)
            return path, current, current_cost, exploration_order

        for neighbor, edge_cost in graph.adjacency[current]:
            if neighbor in visited:
                continue
            new_cost = current_cost + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                order += 1
                heapq.heappush(frontier, (new_cost, order, neighbor))

    return None, None, None, exploration_order
```

### Giải thích

UCS luôn chọn đỉnh có chi phí thật `g(n)` nhỏ nhất để khám phá trước. Trong bài này:

```text
g(n) = tổng chi phí cạnh từ S đến n
```

Mỗi phần tử trong hàng đợi ưu tiên có dạng:

```text
(current_cost, order, node)
```

Trong đó:

- `current_cost` là chi phí thật từ `S` đến `node`.
- `order` giúp ổn định thứ tự khi nhiều đỉnh có cùng chi phí.
- `node` là đỉnh đang chờ khám phá.

UCS không dùng heuristic để chọn đường, nhưng dùng `H` để kiểm tra đỉnh nào là đích. Khi lấy ra một đỉnh có `h = 0`, đường đi đến đỉnh đó là đường có tổng chi phí nhỏ nhất trong các đích có thể gặp.

### Bảng bước chạy chi tiết

Quy ước:

- `g` là tổng chi phí thật từ `S` đến đỉnh hiện tại.
- `Frontier sau bước` ghi các đỉnh đang chờ xét theo dạng `node(g)`.
- UCS luôn lấy đỉnh có `g` nhỏ nhất.

| Bước | Đỉnh lấy ra | g | h(đỉnh) | Đỉnh thêm vào frontier | Frontier sau bước |
|---:|---|---:|---:|---|---|
| 1 | `S` | 0 | 10 | `A(5)`, `B(6)`, `C(5)` | `A(5), C(5), B(6)` |
| 2 | `A` | 5 | 9 | `D(11)`, `E(12)` | `C(5), B(6), D(11), E(12)` |
| 3 | `C` | 5 | 7 | `H(11)`, `K(9)` | `B(6), K(9), D(11), H(11), E(12)` |
| 4 | `B` | 6 | 8 | `F(9)`, `G(10)` | `K(9), F(9), G(10), D(11), H(11), E(12)` |
| 5 | `K` | 9 | 3 | `Z(11)` | `F(9), G(10), D(11), H(11), Z(11), E(12)` |
| 6 | `F` | 9 | 4 | `J(13)`, `L(13)` | `G(10), D(11), H(11), Z(11), E(12), J(13), L(13)` |
| 7 | `G` | 10 | 10 | Không có | `D(11), H(11), Z(11), E(12), J(13), L(13)` |
| 8 | `D` | 11 | 6 | `M(16)`, `N(19)` | `H(11), Z(11), E(12), J(13), L(13), M(16), N(19)` |
| 9 | `H` | 11 | 10 | Không có | `Z(11), E(12), J(13), L(13), M(16), N(19)` |
| 10 | `Z` | 11 | 8 | Không có | `E(12), J(13), L(13), M(16), N(19)` |
| 11 | `E` | 12 | 5 | `I(20)` | `J(13), L(13), M(16), N(19), I(20)` |
| 12 | `J` | 13 | 0 | Dừng | Dừng |

Nhận xét: UCS tìm `J` trước `M` vì chi phí đến `J` là `13`, nhỏ hơn chi phí đến `M` là `16`. Vì UCS ưu tiên chi phí thật, kết quả là đường đi có tổng chi phí nhỏ nhất.

---

## Trả lời: Dán kết quả thực thi vào bên dưới

Lệnh chạy:

```powershell
python "2022/Cau3/04_UCS/cau3_ucs_cay.py"
```

Kết quả:

```text
THUAT TOAN UCS
Thu tu dinh kham pha:
S -> A -> C -> B -> K -> F -> G -> D -> H -> Z -> E -> J

Dinh dich tim duoc: J
Tong chi phi duong di: 13
Duong di tu S den dinh co h = 0:
S -> B -> F -> J
```

Kết luận: UCS tìm được đỉnh đích `J` với tổng chi phí nhỏ nhất là `13`.
