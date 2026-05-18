# Câu 3 - Tìm đường đi trên cây bằng DFS

## Đề bài

Cho cây có trọng số trên đỉnh là heuristic `h(n)` và trọng số trên cạnh là chi phí di chuyển. Cần tìm đường từ `S` đến một đỉnh có `h = 0`.

Báo cáo này trình bày thuật toán **DFS - Depth First Search**.

File chương trình:

```text
cau3_dfs_cay.py
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


class Graph:
    def __init__(self):
        self.adjacency = {}
        self.heuristic = {}

    def add_node(self, node, heuristic_value):
        if node not in self.adjacency:
            self.adjacency[node] = []
        self.heuristic[node] = heuristic_value

    def add_edge(self, u, v, cost):
        self.adjacency[u].append((v, cost))
        self.adjacency[v].append((u, cost))
```

### Giải thích

`V` là tập đỉnh, `H` là trọng số heuristic trên đỉnh, `E` là tập cạnh có trọng số. Cạnh được lưu dưới dạng `(u, v, cost)`.

Trong `Graph`, `self.adjacency` lưu danh sách kề có kèm chi phí cạnh, còn `self.heuristic` lưu trọng số tại từng đỉnh. Đỉnh có `h = 0` là trạng thái đích.

---

## b) Thuật toán DFS

### Trả lời: Dán code vào bên dưới

```python
def dfs_to_zero_heuristic_goal(graph, start):
    stack = [start]
    visited = set()
    discovered = {start}
    parent = {start: None}
    exploration_order = []

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        exploration_order.append(current)

        if graph.heuristic[current] == 0:
            path = reconstruct_path(parent, start, current)
            return path, current, path_cost(path, graph), exploration_order

        for neighbor, _ in reversed(graph.adjacency[current]):
            if neighbor not in discovered:
                discovered.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return None, None, None, exploration_order
```

### Giải thích

DFS dùng ngăn xếp `stack`, nên thuật toán đi sâu theo một nhánh trước khi quay lui. Trong chương trình, các đỉnh kề được duyệt bằng `reversed(...)` để thứ tự khám phá vẫn bám theo thứ tự khai báo trong `V`.

Các biến chính:

| Biến | Ý nghĩa |
|---|---|
| `stack` | Ngăn xếp chứa đỉnh chờ duyệt |
| `visited` | Đỉnh đã được khám phá |
| `discovered` | Đỉnh đã từng được đưa vào stack |
| `parent` | Dùng để truy vết đường đi |
| `exploration_order` | Thứ tự khám phá |

DFS dừng ngay khi gặp đỉnh có `h = 0`. Thuật toán tìm được một đường đi hợp lệ, nhưng không đảm bảo đường có chi phí nhỏ nhất.

### Bảng bước chạy chi tiết

Quy ước:

- `Stack trước khi lấy`: trạng thái ngăn xếp trước khi lấy đỉnh ra khám phá.
- Phần tử bên phải là đỉnh nằm trên đỉnh stack, sẽ được lấy ra trước.
- DFS dừng khi gặp đỉnh có `h = 0`.

| Bước | Stack trước khi lấy | Đỉnh lấy ra | h(đỉnh) | Đỉnh thêm vào stack | Stack sau bước |
|---:|---|---|---:|---|---|
| 1 | `[S]` | `S` | 10 | `C, B, A` | `[C, B, A]` |
| 2 | `[C, B, A]` | `A` | 9 | `E, D` | `[C, B, E, D]` |
| 3 | `[C, B, E, D]` | `D` | 6 | `N, M` | `[C, B, E, N, M]` |
| 4 | `[C, B, E, N, M]` | `M` | 0 | Dừng | Dừng |

Giải thích thêm: trong code, chương trình duyệt `reversed(graph.adjacency[current])`. Nhờ vậy, dù dùng stack, thứ tự khám phá vẫn ưu tiên nhánh trái trước theo hình: `S -> A -> D -> M`.

---

## Trả lời: Dán kết quả thực thi vào bên dưới

Lệnh chạy:

```powershell
python "2022/Cau3/02_DFS/cau3_dfs_cay.py"
```

Kết quả:

```text
THUAT TOAN DFS
Thu tu dinh kham pha:
S -> A -> D -> M

Dinh dich tim duoc: M
Tong chi phi duong di: 16
Duong di tu S den dinh co h = 0:
S -> A -> D -> M
```

Kết luận: DFS đi sâu theo nhánh trái và gặp đỉnh đích `M` trước, với đường đi `S -> A -> D -> M`, tổng chi phí `16`.
