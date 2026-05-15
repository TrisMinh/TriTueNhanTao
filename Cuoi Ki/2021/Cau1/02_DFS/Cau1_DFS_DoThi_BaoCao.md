# Câu 1 - Tìm đường đi trên đồ thị bằng DFS

## Đề bài

Cho đồ thị vô hướng `G = (V, E)` như hình. Cần biểu diễn đồ thị bằng các node/cạnh, sau đó dùng thuật toán tìm kiếm để tìm đường đi từ đỉnh `S` đến đỉnh `G`. Báo cáo này trình bày thuật toán **DFS - Depth First Search**.

File chương trình:

```text
cau1_dfs_do_thi.py
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


class Graph:
    def __init__(self):
        self.adjacency = {}

    def add_node(self, node):
        if node not in self.adjacency:
            self.adjacency[node] = []

    def add_edge(self, u, v):
        self.add_node(u)
        self.add_node(v)
        self.adjacency[u].append(v)
        self.adjacency[v].append(u)
```

### Giải thích chi tiết

Đồ thị được xây dựng theo đúng kiểu node và edge:

- `V` là danh sách node của đồ thị.
- `E` là danh sách cạnh nối giữa các node.
- `add_node(node)` thêm một node vào đồ thị.
- `add_edge(u, v)` thêm cạnh vô hướng giữa `u` và `v`.
- Vì đồ thị vô hướng nên khi thêm cạnh `(u, v)`, chương trình thêm `v` vào danh sách kề của `u` và thêm `u` vào danh sách kề của `v`.

Sau khi xây dựng, danh sách kề được sắp xếp theo thứ tự trong `V` để quá trình chạy ổn định và dễ đối chiếu.

---

## Thuật toán DFS

### Trả lời: Dán code chính

```python
def dfs(adjacency, start, goal):
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

        if current == goal:
            return reconstruct_path(parent, start, goal), exploration_order

        for neighbor in reversed(adjacency[current]):
            if neighbor not in discovered:
                discovered.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return None, exploration_order
```

### Giải thích chi tiết

DFS là thuật toán tìm kiếm theo chiều sâu. Thuật toán chọn một nhánh và đi sâu theo nhánh đó trước, chỉ quay lại xét nhánh khác khi không thể đi tiếp hoặc khi đã gặp node cần tìm.

Các biến chính:

| Biến | Ý nghĩa |
|---|---|
| `stack` | Ngăn xếp chứa các node chờ khám phá |
| `visited` | Các node đã được lấy ra xử lý |
| `discovered` | Các node đã từng được đưa vào stack |
| `parent` | Lưu node cha để truy vết đường đi |
| `exploration_order` | Lưu thứ tự node được khám phá |

DFS dùng ngăn xếp nên node được thêm vào sau sẽ được lấy ra trước. Trong code, em duyệt:

```python
for neighbor in reversed(adjacency[current]):
```

để khi đưa vào stack, thứ tự khám phá vẫn bám theo thứ tự node trong `V`.

Khi gặp `G`, chương trình gọi `reconstruct_path` để truy vết từ `G` ngược về `S` thông qua mảng `parent`.

DFS có thể tìm được một đường đi hợp lệ, nhưng không đảm bảo đường đi đó là ngắn nhất.

---

## Trả lời: Dán kết quả thực thi

Lệnh chạy:

```powershell
python "2021/Cau1/02_DFS/cau1_dfs_do_thi.py"
```

Kết quả:

```text
THUAT TOAN DFS
Thu tu dinh kham pha:
S -> A -> D -> E -> F -> H -> G

Duong di tu S den G:
S -> A -> D -> E -> G
```

Kết luận: DFS tìm được đường đi từ `S` đến `G` là:

```text
S -> A -> D -> E -> G
```

Đường đi này hợp lệ nhưng không phải đường đi ngắn nhất, vì trong đồ thị có đường ngắn hơn là `S -> B -> G`.
