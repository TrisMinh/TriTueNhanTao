# Câu 3 - Tìm đường đi trên cây bằng BFS

## Đề bài

Cho cây `G = (V, E)` như hình vẽ. Trọng số trên đỉnh là heuristic `h(n)`, giá trị càng nhỏ thì càng gần trạng thái đích. Trọng số trên cạnh là chi phí đi qua cạnh. Cần tìm đường đi từ `S` đến một đỉnh có `h = 0`.

Báo cáo này trình bày thuật toán **BFS - Breadth First Search**.

File chương trình:

```text
cau3_bfs_cay.py
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

    def sort_neighbors(self, vertex_order):
        for node in self.adjacency:
            self.adjacency[node].sort(key=lambda item: vertex_order[item[0]])


def build_graph(vertices, edges, heuristic_values):
    graph = Graph()
    for vertex in vertices:
        graph.add_node(vertex, heuristic_values[vertex])
    for u, v, cost in edges:
        graph.add_edge(u, v, cost)
    vertex_order = {vertex: index for index, vertex in enumerate(vertices)}
    graph.sort_neighbors(vertex_order)
    return graph
```

### Giải thích

`V` lưu toàn bộ đỉnh của cây. `H` lưu trọng số trên đỉnh, tức heuristic `h(n)`. Các đỉnh đích là những đỉnh có `h = 0`, ở đây gồm `M` và `J`.

`E` lưu cạnh theo dạng:

```text
(đỉnh_1, đỉnh_2, chi_phí)
```

Ví dụ `("S", "A", 5)` nghĩa là đi qua cạnh nối `S` và `A` tốn chi phí `5`. Vì cây là vô hướng nên `add_edge` thêm cả hai chiều.

Class `Graph` giúp biểu diễn cây thống nhất theo node và edge:

- `add_node`: thêm đỉnh và trọng số heuristic của đỉnh.
- `add_edge`: thêm cạnh và chi phí cạnh.
- `adjacency`: danh sách kề, phục vụ quá trình duyệt.
- `heuristic`: bảng trọng số trên đỉnh.

---

## b) Thuật toán BFS

### Trả lời: Dán code vào bên dưới

```python
def bfs_to_zero_heuristic_goal(graph, start):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    exploration_order = []

    while queue:
        current = queue.popleft()
        exploration_order.append(current)

        if graph.heuristic[current] == 0:
            path = reconstruct_path(parent, start, current)
            return path, current, path_cost(path, graph), exploration_order

        for neighbor, _ in graph.adjacency[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None, None, None, exploration_order
```

### Giải thích

BFS dùng hàng đợi `queue` để duyệt cây theo từng tầng. Từ `S`, thuật toán khám phá các đỉnh ở mức 1 trước, sau đó mức 2, mức 3, ...

Các biến chính:

| Biến | Ý nghĩa |
|---|---|
| `queue` | Hàng đợi các đỉnh chờ khám phá |
| `visited` | Tập đỉnh đã phát hiện |
| `parent` | Lưu cha của mỗi đỉnh để truy vết đường đi |
| `exploration_order` | Thứ tự đỉnh được lấy ra khám phá |

Điều kiện dừng:

```python
if graph.heuristic[current] == 0:
```

nghĩa là khi gặp một đỉnh có trọng số trên đỉnh bằng `0`, thuật toán xem đó là đích và dừng.

BFS không xét trọng số cạnh khi chọn đỉnh tiếp theo. Vì vậy BFS tìm đỉnh đích gần nhất theo số cạnh, không nhất thiết là đường có tổng chi phí nhỏ nhất.

### Bảng bước chạy chi tiết

Quy ước:

- `Queue trước khi lấy`: trạng thái hàng đợi trước khi lấy đỉnh ra khám phá.
- `Đỉnh lấy ra`: đỉnh được khám phá ở bước hiện tại.
- `Đỉnh thêm vào queue`: các đỉnh kề chưa thăm được đưa vào cuối hàng đợi.
- BFS dừng khi gặp đỉnh có `h = 0`.

| Bước | Queue trước khi lấy | Đỉnh lấy ra | h(đỉnh) | Đỉnh thêm vào queue | Queue sau bước |
|---:|---|---|---:|---|---|
| 1 | `[S]` | `S` | 10 | `A, B, C` | `[A, B, C]` |
| 2 | `[A, B, C]` | `A` | 9 | `D, E` | `[B, C, D, E]` |
| 3 | `[B, C, D, E]` | `B` | 8 | `F, G` | `[C, D, E, F, G]` |
| 4 | `[C, D, E, F, G]` | `C` | 7 | `H, K` | `[D, E, F, G, H, K]` |
| 5 | `[D, E, F, G, H, K]` | `D` | 6 | `M, N` | `[E, F, G, H, K, M, N]` |
| 6 | `[E, F, G, H, K, M, N]` | `E` | 5 | `I` | `[F, G, H, K, M, N, I]` |
| 7 | `[F, G, H, K, M, N, I]` | `F` | 4 | `J, L` | `[G, H, K, M, N, I, J, L]` |
| 8 | `[G, H, K, M, N, I, J, L]` | `G` | 10 | Không có | `[H, K, M, N, I, J, L]` |
| 9 | `[H, K, M, N, I, J, L]` | `H` | 10 | Không có | `[K, M, N, I, J, L]` |
| 10 | `[K, M, N, I, J, L]` | `K` | 3 | `Z` | `[M, N, I, J, L, Z]` |
| 11 | `[M, N, I, J, L, Z]` | `M` | 0 | Dừng | Dừng |

Nhận xét: BFS gặp `M` trước `J` vì `M` được đưa vào queue trước và nằm ở cùng tầng với các node lá khác. Do đó đường đi được truy vết là `S -> A -> D -> M`.

---

## Trả lời: Dán kết quả thực thi vào bên dưới

Lệnh chạy:

```powershell
python "2022/Cau3/01_BFS/cau3_bfs_cay.py"
```

Kết quả:

```text
THUAT TOAN BFS
Thu tu dinh kham pha:
S -> A -> B -> C -> D -> E -> F -> G -> H -> K -> M

Dinh dich tim duoc: M
Tong chi phi duong di: 16
Duong di tu S den dinh co h = 0:
S -> A -> D -> M
```

Kết luận: BFS tìm được đỉnh đích `M`, đường đi `S -> A -> D -> M`, tổng chi phí `16`.
