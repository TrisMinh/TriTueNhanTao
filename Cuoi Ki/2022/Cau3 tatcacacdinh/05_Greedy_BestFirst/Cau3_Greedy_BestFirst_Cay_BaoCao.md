# Câu 3 - Tìm đường đi trên cây bằng Greedy Best First Search

## Đề bài

Cho cây có trọng số tại đỉnh là heuristic `h(n)` và trọng số cạnh là chi phí di chuyển. Cần tìm đường từ `S` đến một đỉnh có `h = 0`.

Báo cáo này trình bày thuật toán **Greedy Best First Search**.

File chương trình:

```text
cau3_greedy_best_first_cay.py
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

Greedy Best First Search sử dụng trực tiếp trọng số trên đỉnh `H` làm hàm heuristic. Đỉnh nào có `h` nhỏ hơn thì được xem là gần đích hơn.

Trong cây này, các đỉnh đích là:

```text
M, J
```

vì:

```text
h(M) = 0
h(J) = 0
```

Trọng số cạnh vẫn được lưu trong `E` để sau khi tìm được đường đi, chương trình tính tổng chi phí đường đi.

---

## b) Thuật toán Greedy Best First Search

### Trả lời: Dán code vào bên dưới

```python
def greedy_to_zero_heuristic_goal(graph, start):
    frontier = []
    order = 0
    heapq.heappush(frontier, (graph.heuristic[start], order, start))
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

        if graph.heuristic[current] == 0:
            path = reconstruct_path(parent, start, current)
            return path, current, path_cost(path, graph), exploration_order

        for neighbor, _ in graph.adjacency[current]:
            if neighbor not in discovered:
                discovered.add(neighbor)
                parent[neighbor] = current
                order += 1
                heapq.heappush(frontier, (graph.heuristic[neighbor], order, neighbor))

    return None, None, None, exploration_order
```

### Giải thích

Greedy Best First Search chọn đỉnh tiếp theo chỉ dựa vào heuristic:

```text
priority(n) = h(n)
```

Thuật toán không cộng chi phí đã đi `g(n)`. Vì vậy Greedy thường đi rất nhanh về phía đỉnh có vẻ gần mục tiêu nhất, nhưng không đảm bảo luôn cho đường đi tối ưu.

Từ `S`, các đỉnh kề có heuristic:

| Đỉnh | h |
|---|---:|
| A | 9 |
| B | 8 |
| C | 7 |

Greedy chọn `C` trước vì `h(C)` nhỏ nhất. Sau đó chọn `K`, rồi quay sang `B`, `F`, và gặp `J` có `h(J) = 0`.

### Bảng bước chạy chi tiết

Quy ước:

- `Frontier` là hàng đợi ưu tiên theo `h`.
- `Frontier sau bước` ghi các đỉnh đang chờ xét theo dạng `node(h)`.
- Greedy chỉ xét `h`, không xét tổng chi phí đã đi.

| Bước | Đỉnh lấy ra | h(đỉnh) | Đỉnh thêm vào frontier | Frontier sau bước |
|---:|---|---:|---|---|
| 1 | `S` | 10 | `A(9)`, `B(8)`, `C(7)` | `C(7), B(8), A(9)` |
| 2 | `C` | 7 | `H(10)`, `K(3)` | `K(3), B(8), A(9), H(10)` |
| 3 | `K` | 3 | `Z(8)` | `B(8), Z(8), A(9), H(10)` |
| 4 | `B` | 8 | `F(4)`, `G(10)` | `F(4), Z(8), A(9), H(10), G(10)` |
| 5 | `F` | 4 | `J(0)`, `L(9)` | `J(0), Z(8), A(9), L(9), H(10), G(10)` |
| 6 | `J` | 0 | Dừng | Dừng |

Nhận xét: Greedy đi theo các đỉnh có heuristic nhỏ nên thứ tự khám phá giống A* trong ví dụ này: `S -> C -> K -> B -> F -> J`. Tuy nhiên, Greedy không dùng `g`, nên trong đồ thị khác nó có thể chọn đường không tối ưu.

---

## Trả lời: Dán kết quả thực thi vào bên dưới

Lệnh chạy:

```powershell
python "2022/Cau3/05_Greedy_BestFirst/cau3_greedy_best_first_cay.py"
```

Kết quả:

```text
THUAT TOAN GREEDY BEST FIRST SEARCH
Thu tu dinh kham pha:
S -> C -> K -> B -> F -> J

Dinh dich tim duoc: J
Tong chi phi duong di: 13
Duong di tu S den dinh co h = 0:
S -> B -> F -> J
```

Kết luận: Greedy Best First Search tìm được đỉnh đích `J`, đường đi `S -> B -> F -> J`, tổng chi phí `13`. Trong ví dụ này kết quả trùng với A*, nhưng về nguyên lý Greedy không đảm bảo tối ưu trong mọi trường hợp.
