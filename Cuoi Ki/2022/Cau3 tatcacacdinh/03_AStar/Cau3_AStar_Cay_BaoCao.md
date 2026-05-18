# Câu 3 - Tìm đường đi trên cây bằng thuật toán A*

## Đề bài

Cho cây `G = (V, E)` như hình vẽ:

- `V` là tập đỉnh.
- `E` là tập cạnh.
- Trọng số tại đỉnh là hàm ước lượng khoảng cách từ đỉnh đó đến trạng thái đích. Giá trị càng nhỏ thì đỉnh đó càng gần trạng thái đích.
- Trọng số trên cạnh là chi phí phải trả khi đi qua cạnh.

Yêu cầu:

1. Khởi tạo tập đỉnh `V`, tập cạnh `E`, trọng số trên đỉnh và trọng số trên cạnh.
2. Dùng thuật toán **A\*** để tìm đường đi từ `S` đến một đỉnh có trọng số trên đỉnh bằng `0`.
3. In ra thứ tự đỉnh khám phá trong quá trình tìm kiếm.

File chương trình:

```text
cau3_astar_cay.py
```

---

## a) Biểu diễn cây bằng V, E, trọng số đỉnh và trọng số cạnh

### Trả lời: Dán code vào bên dưới

```python
V = ["S", "A", "B", "C", "D", "E", "F", "G", "H", "K", "M", "N", "I", "J", "L", "Z"]

H = {
    "S": 10,
    "A": 9,
    "B": 8,
    "C": 7,
    "D": 6,
    "E": 5,
    "F": 4,
    "G": 10,
    "H": 10,
    "K": 3,
    "M": 0,
    "N": 10,
    "I": 6,
    "J": 0,
    "L": 9,
    "Z": 8,
}

E = [
    ("S", "A", 5),
    ("S", "B", 6),
    ("S", "C", 5),
    ("A", "D", 6),
    ("A", "E", 7),
    ("D", "M", 5),
    ("D", "N", 8),
    ("E", "I", 8),
    ("B", "F", 3),
    ("B", "G", 4),
    ("F", "J", 4),
    ("F", "L", 4),
    ("C", "H", 6),
    ("C", "K", 4),
    ("K", "Z", 2),
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

Từ hình vẽ, ta đọc được các đỉnh của cây:

```text
S, A, B, C, D, E, F, G, H, K, M, N, I, J, L, Z
```

Do đó, tập đỉnh được khai báo bằng list `V`.

Trọng số tại đỉnh chính là giá trị heuristic `h(n)`, tức ước lượng khoảng cách từ đỉnh `n` đến trạng thái đích. Trong chương trình, em lưu các giá trị này trong dictionary `H`:

```text
h(S) = 10
h(A) = 9
h(B) = 8
...
h(M) = 0
h(J) = 0
```

Các đỉnh có trọng số bằng `0` là:

```text
M, J
```

Đây là các trạng thái đích mà A* cần tìm.

Tập cạnh `E` được biểu diễn bằng bộ ba:

```text
(đỉnh_1, đỉnh_2, chi_phí)
```

Ví dụ:

```python
("S", "A", 5)
```

nghĩa là có cạnh nối giữa `S` và `A`, chi phí đi qua cạnh này là `5`.

Vì đây là cây vô hướng nên cạnh `("S", "A", 5)` cho phép đi từ `S` sang `A` và cũng cho phép đi từ `A` về `S`, đều với chi phí `5`.

Trong đoạn code trên, em dùng class `Graph` để biểu diễn cây bằng node và edge:

```python
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
```

Ý nghĩa:

- `self.adjacency` lưu danh sách kề của cây.
- `self.heuristic` lưu trọng số trên từng đỉnh.
- `add_node(node, heuristic_value)` thêm một đỉnh và heuristic của đỉnh đó.
- `add_edge(u, v, cost)` thêm cạnh vô hướng giữa `u` và `v` với chi phí `cost`.
- `sort_neighbors(vertex_order)` sắp xếp các đỉnh kề theo thứ tự trong `V` để kết quả chạy ổn định và dễ kiểm tra.

Sau khi có class `Graph`, hàm `build_graph` tạo cây hoàn chỉnh từ `V`, `E` và `H`:

```python
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

Hàm này đảm bảo toàn bộ đỉnh được thêm bằng `add_node`, toàn bộ cạnh có trọng số được thêm bằng `add_edge`, đúng với yêu cầu khởi tạo tập đỉnh, tập cạnh, trọng số trên đỉnh và trọng số trên cạnh.

---

## b) Chương trình A* tìm đường từ S đến đỉnh có trọng số bằng 0

### Trả lời: Dán code vào bên dưới

```python
def astar_to_zero_heuristic_goal(graph, start):
    frontier = []
    order = 0
    start_h = graph.heuristic[start]
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

        if graph.heuristic[current] == 0:
            path = reconstruct_path(parent, start, current)
            return path, current, current_g, exploration_order

        for neighbor, edge_cost in graph.adjacency[current]:
            if neighbor in visited:
                continue

            tentative_g = current_g + edge_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                h = graph.heuristic[neighbor]
                f = tentative_g + h
                order += 1
                heapq.heappush(frontier, (f, h, tentative_g, order, neighbor))

    return None, None, None, exploration_order
```

### Giải thích

Thuật toán A* dùng hàm đánh giá:

```text
f(n) = g(n) + h(n)
```

Trong đó:

- `g(n)` là chi phí thật từ đỉnh bắt đầu `S` đến đỉnh hiện tại `n`.
- `h(n)` là trọng số tại đỉnh, tức chi phí ước lượng từ `n` đến trạng thái đích.
- `f(n)` là tổng chi phí dùng để ưu tiên chọn đỉnh tiếp theo.

Trong chương trình, hàng đợi ưu tiên `frontier` lưu mỗi đỉnh dưới dạng:

```text
(f, h, g, order, node)
```

Ý nghĩa:

- `f`: giá trị ưu tiên chính, `f = g + h`.
- `h`: heuristic của node, dùng để phụ khi nhiều node có cùng `f`.
- `g`: chi phí thật từ `S` đến node.
- `order`: thứ tự đưa vào hàng đợi, giúp kết quả ổn định.
- `node`: đỉnh đang chờ khám phá.

Ban đầu, thuật toán bắt đầu tại `S`:

```text
g(S) = 0
h(S) = 10
f(S) = 10
```

Ở mỗi bước, thuật toán lấy đỉnh có `f` nhỏ nhất ra khám phá. Nếu đỉnh đó có:

```text
h(node) = 0
```

thì đỉnh đó là trạng thái đích, thuật toán dừng và truy vết đường đi.

Hàm truy vết:

```python
def reconstruct_path(parent, start, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path if path[0] == start else None
```

Hàm này đi ngược từ đỉnh đích về `S` thông qua dictionary `parent`, sau đó đảo ngược danh sách để thu được đường đi đúng chiều từ `S` đến đích.

### Minh họa quá trình chọn đỉnh

Từ `S`, có 3 đỉnh kề:

| Đỉnh | g | h | f = g + h |
|---|---:|---:|---:|
| A | 5 | 9 | 14 |
| B | 6 | 8 | 14 |
| C | 5 | 7 | 12 |

A* chọn `C` trước vì `f(C) = 12` nhỏ nhất.

Từ `C`, xét tiếp:

| Đỉnh | g | h | f |
|---|---:|---:|---:|
| H | 11 | 10 | 21 |
| K | 9 | 3 | 12 |

A* chọn `K` vì `f(K) = 12`.

Sau khi khám phá `K`, trong hàng đợi có `A` và `B` cùng có:

```text
f(A) = 14
f(B) = 14
```

Khi hai node có cùng `f`, chương trình ưu tiên node có `h` nhỏ hơn. Vì:

```text
h(B) = 8 < h(A) = 9
```

nên `B` được khám phá trước `A`. Từ `B`, thuật toán tiếp tục đi đến `F`, rồi gặp node đích `J` có `h(J) = 0`.

Đường đi tìm được:

```text
S -> B -> F -> J
```

Chi phí:

```text
S -> B: 6
B -> F: 3
F -> J: 4
Tổng: 13
```

### Bảng bước chạy chi tiết

Quy ước:

- `g(n)` là chi phí thật từ `S` đến `n`.
- `h(n)` là trọng số trên đỉnh.
- `f(n) = g(n) + h(n)`.
- `Frontier sau bước` ghi các đỉnh đang chờ xét theo dạng `node(g,h,f)`.
- A* luôn lấy đỉnh có `f` nhỏ nhất. Nếu bằng `f`, chương trình xét tiếp `h` nhỏ hơn.

| Bước | Đỉnh lấy ra | g | h | f | Đỉnh thêm vào frontier | Frontier sau bước |
|---:|---|---:|---:|---:|---|---|
| 1 | `S` | 0 | 10 | 10 | `A(5,9,14)`, `B(6,8,14)`, `C(5,7,12)` | `C(5,7,12), B(6,8,14), A(5,9,14)` |
| 2 | `C` | 5 | 7 | 12 | `H(11,10,21)`, `K(9,3,12)` | `K(9,3,12), B(6,8,14), A(5,9,14), H(11,10,21)` |
| 3 | `K` | 9 | 3 | 12 | `Z(11,8,19)` | `B(6,8,14), A(5,9,14), Z(11,8,19), H(11,10,21)` |
| 4 | `B` | 6 | 8 | 14 | `F(9,4,13)`, `G(10,10,20)` | `F(9,4,13), A(5,9,14), Z(11,8,19), G(10,10,20), H(11,10,21)` |
| 5 | `F` | 9 | 4 | 13 | `J(13,0,13)`, `L(13,9,22)` | `J(13,0,13), A(5,9,14), Z(11,8,19), G(10,10,20), H(11,10,21), L(13,9,22)` |
| 6 | `J` | 13 | 0 | 13 | Dừng | Dừng |

Nhận xét: A* không chọn `M` dù `M` cũng là đích, vì theo thứ tự ưu tiên `f = g + h`, nhánh qua `B -> F -> J` cho đích có chi phí tốt hơn và được lấy ra trước. Đường đi cuối cùng là `S -> B -> F -> J`.

---

## Trả lời: Dán kết quả thực thi vào bên dưới

Lệnh chạy:

```powershell
python "2022/Cau3/03_AStar/cau3_astar_cay.py"
```

Kết quả:

```text
Tap dinh V:
['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'I', 'J', 'L', 'Z']

Trong so tren dinh H:
h(S) = 10
h(A) = 9
h(B) = 8
h(C) = 7
h(D) = 6
h(E) = 5
h(F) = 4
h(G) = 10
h(H) = 10
h(K) = 3
h(M) = 0
h(N) = 10
h(I) = 6
h(J) = 0
h(L) = 9
h(Z) = 8

Tap canh E va chi phi tren canh:
S -- A: cost = 5
S -- B: cost = 6
S -- C: cost = 5
A -- D: cost = 6
A -- E: cost = 7
D -- M: cost = 5
D -- N: cost = 8
E -- I: cost = 8
B -- F: cost = 3
B -- G: cost = 4
F -- J: cost = 4
F -- L: cost = 4
C -- H: cost = 6
C -- K: cost = 4
K -- Z: cost = 2

THUAT TOAN A*
Thu tu dinh kham pha:
S -> C -> K -> B -> F -> J

Dinh dich tim duoc: J
Tong chi phi duong di: 13
Duong di tu S den dinh co h = 0:
S -> B -> F -> J
```

Kết luận: Thuật toán A* tìm được đỉnh đích `J`, vì `h(J) = 0`. Đường đi từ `S` đến `J` là:

```text
S -> B -> F -> J
```

Tổng chi phí đường đi là:

```text
13
```
