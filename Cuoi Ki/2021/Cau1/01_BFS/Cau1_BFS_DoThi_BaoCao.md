# Câu 1 - Biểu diễn đồ thị và tìm đường đi bằng BFS

## Đề bài

Cho đồ thị vô hướng `G = (V, E)` như hình vẽ, trong đó:

- `V` là tập đỉnh.
- `E` là tập cạnh.

Yêu cầu:

1. Viết đoạn code biểu diễn đồ thị bằng cách khởi tạo tập đỉnh `V` và tập cạnh `E`.
2. Viết chương trình dùng thuật toán tìm kiếm theo chiều rộng `BFS` để tìm đường đi từ đỉnh `S` đến đỉnh `G`.
3. Trong quá trình tìm kiếm, in ra thứ tự đỉnh được khám phá.
4. Nếu không tìm thấy đường đi thì in:

```text
Khong tim thay duong di
```

---

## a) Biểu diễn đồ thị bằng tập đỉnh V và tập cạnh E

### Trả lời: Dán code vào bên dưới

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


graph = Graph()

for vertex in V:
    graph.add_node(vertex)

for u, v in E:
    graph.add_edge(u, v)
```

### Giải thích chi tiết

Từ hình vẽ, ta xác định các đỉnh của đồ thị là:

```text
S, A, B, C, D, E, F, G, H
```

Do đó tập đỉnh được khai báo:

```python
V = ["S", "A", "B", "C", "D", "E", "F", "G", "H"]
```

Vì đồ thị là đồ thị vô hướng nên cạnh `("S", "A")` có nghĩa là có thể đi từ `S` sang `A` và cũng có thể đi từ `A` về `S`.

Các cạnh được đọc từ hình:

| Cạnh | Ý nghĩa |
|---|---|
| `("S", "A")` | Đỉnh `S` nối với `A` |
| `("S", "B")` | Đỉnh `S` nối với `B` |
| `("S", "C")` | Đỉnh `S` nối với `C` |
| `("A", "B")` | Đỉnh `A` nối với `B` |
| `("A", "D")` | Đỉnh `A` nối với `D` |
| `("B", "C")` | Đỉnh `B` nối với `C` |
| `("B", "D")` | Đỉnh `B` nối với `D` |
| `("B", "F")` | Đỉnh `B` nối với `F` |
| `("B", "G")` | Đỉnh `B` nối với `G` |
| `("C", "F")` | Đỉnh `C` nối với `F` |
| `("D", "E")` | Đỉnh `D` nối với `E` |
| `("E", "F")` | Đỉnh `E` nối với `F` |
| `("E", "G")` | Đỉnh `E` nối với `G` |
| `("F", "H")` | Đỉnh `F` nối với `H` |
| `("G", "H")` | Đỉnh `G` nối với `H` |

Việc biểu diễn bằng `V` và `E` giúp chương trình giữ đúng cấu trúc toán học của đồ thị:

```text
G = (V, E)
```

Trong chương trình, em không khai báo trực tiếp danh sách kề ngay từ đầu. Thay vào đó, em xây dựng đồ thị bằng lớp `Graph` và hai thao tác chính:

- `add_node(node)`: thêm một đỉnh vào đồ thị.
- `add_edge(u, v)`: thêm một cạnh vô hướng nối hai đỉnh `u` và `v`.

Cách làm này thống nhất với cách hiểu đồ thị gồm các node và edge: trước hết tạo các node từ tập `V`, sau đó thêm các edge từ tập `E`.

Lớp `Graph`:

```python
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

Hàm xây dựng đồ thị:

```python
def build_graph(vertices, edges):
    graph = Graph()

    for vertex in vertices:
        graph.add_node(vertex)

    for u, v in edges:
        graph.add_edge(u, v)

    vertex_order = {vertex: index for index, vertex in enumerate(vertices)}
    graph.sort_neighbors(vertex_order)
    return graph
```

Trong đó hàm `sort_neighbors` chỉ dùng để sắp xếp danh sách kề theo thứ tự trong `V`, giúp kết quả BFS ổn định khi in ra.

Giải thích:

- `self.adjacency` là danh sách kề của đồ thị. Mỗi key là một node, value là danh sách các node kề với nó.
- `add_node(node)` thêm một node vào `self.adjacency`. Nếu node đã tồn tại thì không thêm trùng.
- `add_edge(u, v)` thêm edge nối giữa `u` và `v`.
- Vì đồ thị vô hướng nên khi thêm cạnh `(u, v)`, chương trình thêm `v` vào danh sách kề của `u` và thêm `u` vào danh sách kề của `v`.
- Sau đó `sort_neighbors` sắp xếp các node kề theo thứ tự trong `V` để quá trình BFS có kết quả ổn định, dễ kiểm tra và dễ trình bày.

Danh sách kề thu được:

```text
S: A, B, C
A: S, B, D
B: S, A, C, D, F, G
C: S, B, F
D: A, B, E
E: D, F, G
F: B, C, E, H
G: B, E, H
H: F, G
```

---

## b) Chương trình BFS tìm đường đi từ S đến G

### Trả lời: Dán code vào bên dưới

```python
from collections import deque
from pathlib import Path


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

    def sort_neighbors(self, vertex_order):
        for vertex in self.adjacency:
            self.adjacency[vertex].sort(key=lambda item: vertex_order[item])


def build_graph(vertices, edges):
    graph = Graph()

    for vertex in vertices:
        graph.add_node(vertex)

    for u, v in edges:
        graph.add_edge(u, v)

    vertex_order = {vertex: index for index, vertex in enumerate(vertices)}
    graph.sort_neighbors(vertex_order)
    return graph


def reconstruct_path(parent, start, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    if path[0] == start:
        return path

    return None


def bfs(adjacency, start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    exploration_order = []

    while queue:
        current = queue.popleft()
        exploration_order.append(current)

        if current == goal:
            return reconstruct_path(parent, start, goal), exploration_order

        for neighbor in adjacency[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None, exploration_order


def format_adjacency(adjacency):
    lines = []

    for vertex in V:
        neighbors = ", ".join(adjacency[vertex])
        lines.append(f"{vertex}: {neighbors}")

    return "\n".join(lines)


def solve():
    graph = build_graph(V, E)
    adjacency = graph.adjacency
    path, exploration_order = bfs(adjacency, "S", "G")

    lines = [
        "Tap dinh V:",
        str(V),
        "",
        "Tap canh E:",
        str(E),
        "",
        "Danh sach ke:",
        format_adjacency(adjacency),
        "",
        "Thu tu dinh kham pha:",
        " -> ".join(exploration_order),
        "",
    ]

    if path is None:
        lines.append("Khong tim thay duong di")
    else:
        lines.append("Duong di tu S den G:")
        lines.append(" -> ".join(path))

    return "\n".join(lines)


def main():
    current_dir = Path(__file__).resolve().parent
    output_text = solve()
    output_file = current_dir / "BFS_out.txt"

    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)
    print(f"\nDa luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()
```

### Giải thích chi tiết

BFS là thuật toán tìm kiếm theo chiều rộng. Thuật toán bắt đầu từ đỉnh xuất phát `S`, sau đó lần lượt xét các đỉnh ở khoảng cách 1 cạnh, rồi đến khoảng cách 2 cạnh, 3 cạnh, ...

Vì BFS xét theo từng lớp khoảng cách nên trong đồ thị không trọng số, BFS tìm được đường đi có số cạnh ít nhất từ `S` đến `G`.

Các biến chính trong chương trình:

| Biến | Chức năng |
|---|---|
| `queue` | Hàng đợi lưu các đỉnh đang chờ xét |
| `visited` | Tập các đỉnh đã được phát hiện để tránh xét lặp |
| `parent` | Lưu đỉnh cha để truy vết đường đi |
| `exploration_order` | Lưu thứ tự các đỉnh được lấy ra khỏi hàng đợi và khám phá |

Ban đầu:

```python
queue = deque(["S"])
visited = {"S"}
parent = {"S": None}
exploration_order = []
```

Nghĩa là thuật toán bắt đầu tại đỉnh `S`. Đỉnh `S` không có cha nên `parent["S"] = None`.

Ở mỗi vòng lặp:

```python
current = queue.popleft()
exploration_order.append(current)
```

Chương trình lấy đỉnh đầu hàng đợi ra để khám phá. Đỉnh này được thêm vào `exploration_order` để in thứ tự tìm kiếm.

Nếu đỉnh hiện tại là `G`:

```python
if current == goal:
    return reconstruct_path(parent, start, goal), exploration_order
```

thì chương trình dừng BFS và truy vết đường đi từ `G` ngược về `S` bằng mảng `parent`.

Nếu chưa gặp `G`, chương trình xét các đỉnh kề:

```python
for neighbor in adjacency[current]:
    if neighbor not in visited:
        visited.add(neighbor)
        parent[neighbor] = current
        queue.append(neighbor)
```

Với mỗi đỉnh kề chưa thăm:

- Đánh dấu đỉnh đó là đã phát hiện.
- Ghi nhận cha của đỉnh đó là `current`.
- Đưa đỉnh đó vào cuối hàng đợi để xét sau.

Hàm truy vết đường đi:

```python
def reconstruct_path(parent, start, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path
```

Ví dụ nếu `parent["G"] = "B"` và `parent["B"] = "S"`, đường đi truy vết được là:

```text
G <- B <- S
```

Sau khi đảo ngược:

```text
S -> B -> G
```

---

## Trả lời: Dán kết quả thực thi vào bên dưới

Lệnh chạy:

```powershell
python "2021/Cau1/01_BFS/cau1_bfs_do_thi.py"
```

Kết quả:

```text
Tap dinh V:
['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

Tap canh E:
[('S', 'A'), ('S', 'B'), ('S', 'C'), ('A', 'B'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('B', 'F'), ('B', 'G'), ('C', 'F'), ('D', 'E'), ('E', 'F'), ('E', 'G'), ('F', 'H'), ('G', 'H')]

Danh sach ke:
S: A, B, C
A: S, B, D
B: S, A, C, D, F, G
C: S, B, F
D: A, B, E
E: D, F, G
F: B, C, E, H
G: B, E, H
H: F, G

Thu tu dinh kham pha:
S -> A -> B -> C -> D -> F -> G

Duong di tu S den G:
S -> B -> G
```

Kết luận: BFS tìm được đường đi từ `S` đến `G` là:

```text
S -> B -> G
```

Đây là đường đi ngắn nhất theo số cạnh trong đồ thị, gồm 2 cạnh.
