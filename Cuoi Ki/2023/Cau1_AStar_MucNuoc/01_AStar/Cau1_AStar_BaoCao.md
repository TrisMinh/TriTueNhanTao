# Câu 1 - Báo cáo thuật toán A*

## Đề bài

Cho `n` cái gáo nước. Gáo thứ `i` chứa tối đa `a_i` lít nước. Cần múc đúng `M` lít nước từ bờ sông qua bể nước lớn với số thao tác ít nhất, không được múc quá và cũng không được múc thiếu.

Các thao tác hợp lệ:

- Múc nước từ bờ sông vào một gáo cho đến khi gáo đầy.
- Chuyển nước từ một gáo sang gáo khác cho đến khi gáo nguồn hết nước hoặc gáo đích đầy.
- Chuyển toàn bộ nước trong một gáo sang bể nếu không làm bể vượt quá `M` lít.
- Vứt bỏ toàn bộ nước trong một gáo. Thao tác vứt bỏ cũng được tính là 1 thao tác.

Yêu cầu chính của báo cáo này là dùng thuật toán **A\*** để tìm cách múc nước. Nếu không có đáp án thì in:

```text
Khong co dap an
```

Trong chương trình, dữ liệu mặc định khi không nhập từ bàn phím là:

```text
3 13 7 8 9
```

Ý nghĩa:

- `n = 3`
- `M = 13`
- Ba gáo có dung tích lần lượt là `7`, `8`, `9` lít.

---

## Mô hình hóa bài toán

Mỗi trạng thái được biểu diễn bằng:

```text
((x1, x2, ..., xn), B)
```

Trong đó:

- `x_i` là lượng nước hiện có trong gáo thứ `i`.
- `B` là lượng nước đã chuyển vào bể.
- Trạng thái bắt đầu là `((0, 0, ..., 0), 0)`.
- Trạng thái đích là trạng thái có `B = M`.

Với dữ liệu `3 13 7 8 9`, trạng thái ban đầu là:

```text
((0, 0, 0), 0)
```

Một trạng thái ví dụ:

```text
((0, 6, 9), 7)
```

nghĩa là gáo 1 có 0 lít, gáo 2 có 6 lít, gáo 3 có 9 lít và bể đang có 7 lít.

Trước khi tìm kiếm, chương trình kiểm tra điều kiện có thể có đáp án:

```text
M % gcd(a1, a2, ..., an) == 0
```

Nếu `M` không chia hết cho ước chung lớn nhất của các dung tích gáo thì không thể đo chính xác `M` lít bằng các gáo đã cho.

---

## Thuật toán A*

A* là thuật toán tìm kiếm có thông tin. Thuật toán chọn trạng thái tiếp theo dựa trên hàm đánh giá:

```text
f(s) = g(s) + h'(s)
```

Trong đó:

- `g(s)` là số thao tác thật đã dùng từ trạng thái ban đầu đến trạng thái `s`.
- `h'(s)` là số thao tác ước lượng tối thiểu còn cần để đi từ trạng thái `s` đến trạng thái đích.
- `f(s)` là giá trị ưu tiên. Trạng thái có `f(s)` nhỏ hơn được xét trước.

Chương trình dùng hàng đợi ưu tiên `heapq`. Mỗi phần tử trong hàng đợi có dạng:

```text
(f, h, g, order, state)
```

Trong đó `order` dùng để ổn định thứ tự xét khi nhiều trạng thái có cùng độ ưu tiên.

---

## Trả lời: Dán code

```python
from pathlib import Path
import heapq
import math
import sys


DEFAULT_INPUT = "3 13 7 8 9"


def parse_input(input_text):
    input_text = input_text.replace("\ufeff", "").strip()
    values = [int(value) for value in input_text.split()]

    if len(values) < 3:
        raise ValueError("Can nhap n, M va danh sach dung tich cac gao")

    n = values[0]
    target = values[1]
    capacities = values[2:]

    if len(capacities) != n:
        raise ValueError("So luong dung tich gao khong khop voi n")

    return n, target, capacities


def normalize_input_text(input_text):
    input_text = input_text.replace("\ufeff", "").strip()

    if not input_text:
        input_text = DEFAULT_INPUT

    return " ".join(input_text.split())


def has_possible_answer(target, capacities):
    return target % math.gcd(*capacities) == 0


def heuristic(state, target, capacities):
    _, tank_amount = state
    remaining = target - tank_amount

    if remaining <= 0:
        return 0

    return math.ceil(remaining / max(capacities))


def format_state(jug_amounts, tank_amount):
    jug_text = ", ".join(
        f"Gao {index + 1}: {amount} lit"
        for index, amount in enumerate(jug_amounts)
    )
    return f"({jug_text}, Be: {tank_amount} lit)"


def generate_neighbors(state, capacities, target):
    jug_amounts, tank_amount = state
    n = len(capacities)
    neighbors = []

    for i in range(n):
        if jug_amounts[i] < capacities[i]:
            new_jugs = list(jug_amounts)
            amount = capacities[i] - jug_amounts[i]
            new_jugs[i] = capacities[i]
            new_state = (tuple(new_jugs), tank_amount)
            action = (
                f"Chuyen/Muc {amount} lit nuoc tu bo song qua gao {i + 1} "
                f"{format_state(new_state[0], new_state[1])}"
            )
            neighbors.append((new_state, action))

    for i in range(n):
        if jug_amounts[i] > 0 and tank_amount + jug_amounts[i] <= target:
            new_jugs = list(jug_amounts)
            amount = new_jugs[i]
            new_jugs[i] = 0
            new_tank = tank_amount + amount
            new_state = (tuple(new_jugs), new_tank)
            action = (
                f"Chuyen/Muc {amount} lit nuoc tu gao {i + 1} qua be "
                f"{format_state(new_state[0], new_state[1])}"
            )
            neighbors.append((new_state, action))

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            if jug_amounts[i] > 0 and jug_amounts[j] < capacities[j]:
                amount = min(jug_amounts[i], capacities[j] - jug_amounts[j])
                new_jugs = list(jug_amounts)
                new_jugs[i] -= amount
                new_jugs[j] += amount
                new_state = (tuple(new_jugs), tank_amount)
                action = (
                    f"Chuyen/Muc {amount} lit nuoc tu gao {i + 1} qua gao {j + 1} "
                    f"{format_state(new_state[0], new_state[1])}"
                )
                neighbors.append((new_state, action))

    for i in range(n):
        if jug_amounts[i] > 0:
            new_jugs = list(jug_amounts)
            amount = new_jugs[i]
            new_jugs[i] = 0
            new_state = (tuple(new_jugs), tank_amount)
            action = (
                f"Vut bo toan bo {amount} lit nuoc cua gao {i + 1}. "
                f"{format_state(new_state[0], new_state[1])}"
            )
            neighbors.append((new_state, action))

    return neighbors


def reconstruct_actions(parent, goal_state):
    actions = []
    current = goal_state

    while parent[current][0] is not None:
        previous_state, action = parent[current]
        actions.append(action)
        current = previous_state

    actions.reverse()
    return actions


def format_solution(actions):
    if actions is None:
        return "Khong co dap an"

    lines = [f"So thao tac: {len(actions)}"]
    lines.extend(f"{index}. {action}" for index, action in enumerate(actions, start=1))
    return "\n".join(lines)


def astar_water_jug(n, target, capacities):
    if n <= 0 or target <= 0 or any(capacity <= 0 for capacity in capacities):
        return None
    if not has_possible_answer(target, capacities):
        return None

    start_state = (tuple([0] * n), 0)
    open_set = []
    order = 0
    start_h = heuristic(start_state, target, capacities)
    heapq.heappush(open_set, (start_h, start_h, 0, order, start_state))

    parent = {start_state: (None, None)}
    g_score = {start_state: 0}
    visited = set()

    while open_set:
        _, _, current_g, _, current_state = heapq.heappop(open_set)

        if current_state in visited:
            continue

        visited.add(current_state)
        _, tank_amount = current_state

        if tank_amount == target:
            return reconstruct_actions(parent, current_state), len(visited)

        for next_state, action in generate_neighbors(current_state, capacities, target):
            tentative_g = current_g + 1

            if next_state not in g_score or tentative_g < g_score[next_state]:
                g_score[next_state] = tentative_g
                parent[next_state] = (current_state, action)
                h = heuristic(next_state, target, capacities)
                f = tentative_g + h
                order += 1
                heapq.heappush(open_set, (f, h, tentative_g, order, next_state))

    return None


def solve(input_text):
    n, target, capacities = parse_input(input_text)
    result = astar_water_jug(n, target, capacities)

    if result is None:
        return "Khong co dap an"

    actions, visited_count = result
    return f"So trang thai da xet: {visited_count}\n{format_solution(actions)}"


def main():
    current_dir = Path(__file__).resolve().parent
    input_text = normalize_input_text(sys.stdin.read())
    output_text = solve(input_text)
    output_file = current_dir / "AStar_out.txt"

    output_file.write_text(output_text, encoding="utf-8")
    print(f"Nhap: {input_text}")
    print(output_text)
    print(f"Da luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()
```

---

## Trả lời: Dán kết quả thực thi với dữ liệu nhập `3 13 7 8 9`

Lệnh chạy:

```powershell
python "2023/Cau1_AStar_MucNuoc/01_AStar/cau1_astar.py"
```

Kết quả:

```text
Nhap: 3 13 7 8 9
So trang thai da xet: 203
So thao tac: 7
1. Chuyen/Muc 7 lit nuoc tu bo song qua gao 1 (Gao 1: 7 lit, Gao 2: 0 lit, Gao 3: 0 lit, Be: 0 lit)
2. Chuyen/Muc 7 lit nuoc tu gao 1 qua be (Gao 1: 0 lit, Gao 2: 0 lit, Gao 3: 0 lit, Be: 7 lit)
3. Chuyen/Muc 7 lit nuoc tu bo song qua gao 1 (Gao 1: 7 lit, Gao 2: 0 lit, Gao 3: 0 lit, Be: 7 lit)
4. Chuyen/Muc 8 lit nuoc tu bo song qua gao 2 (Gao 1: 7 lit, Gao 2: 8 lit, Gao 3: 0 lit, Be: 7 lit)
5. Chuyen/Muc 7 lit nuoc tu gao 1 qua gao 3 (Gao 1: 0 lit, Gao 2: 8 lit, Gao 3: 7 lit, Be: 7 lit)
6. Chuyen/Muc 2 lit nuoc tu gao 2 qua gao 3 (Gao 1: 0 lit, Gao 2: 6 lit, Gao 3: 9 lit, Be: 7 lit)
7. Chuyen/Muc 6 lit nuoc tu gao 2 qua be (Gao 1: 0 lit, Gao 2: 0 lit, Gao 3: 9 lit, Be: 13 lit)
```

Như vậy, chương trình tìm được cách múc đúng `13` lít sau `7` thao tác. Lượng nước trong bể ở trạng thái cuối cùng bằng đúng `M = 13`.

---

## Trả lời: Giải thích hàm h' trong thuật toán A*

Hàm khoảng cách `h'` trong chương trình là:

```python
def heuristic(state, target, capacities):
    _, tank_amount = state
    remaining = target - tank_amount

    if remaining <= 0:
        return 0

    return math.ceil(remaining / max(capacities))
```

Ý tưởng của hàm này là ước lượng số thao tác tối thiểu còn cần để làm đầy bể đến đúng `M` lít.

Ở một trạng thái bất kỳ:

```text
state = ((x1, x2, ..., xn), B)
```

ta có:

- `B = tank_amount`: lượng nước hiện có trong bể.
- `target = M`: lượng nước cần đạt.
- `remaining = M - B`: lượng nước còn thiếu trong bể.

Nếu `remaining <= 0`, nghĩa là bể đã đủ hoặc không còn thiếu nước nữa, khi đó:

```text
h'(state) = 0
```

Nếu bể vẫn còn thiếu nước, chương trình lấy dung tích gáo lớn nhất:

```text
max_capacity = max(a1, a2, ..., an)
```

Trong một lần chuyển nước vào bể, lượng nước nhiều nhất có thể đóng góp không thể vượt quá dung tích của gáo lớn nhất. Vì vậy, số lần ít nhất để đưa thêm `remaining` lít vào bể được ước lượng là:

```text
h'(state) = ceil(remaining / max_capacity)
```

Ví dụ với dữ liệu:

```text
n = 3, M = 13, capacities = [7, 8, 9]
```

Dung tích gáo lớn nhất là:

```text
max_capacity = 9
```

Tại trạng thái ban đầu:

```text
((0, 0, 0), 0)
```

bể có `0` lít, còn thiếu:

```text
remaining = 13 - 0 = 13
```

nên:

```text
h' = ceil(13 / 9) = 2
```

Điều này có nghĩa là trong trường hợp lý tưởng, nếu mỗi lần đưa nước vào bể đều đưa được nhiều nhất có thể, ta vẫn cần ít nhất 2 lần chuyển nước vào bể để đạt 13 lít.

Sau khi đã có 7 lít trong bể:

```text
remaining = 13 - 7 = 6
h' = ceil(6 / 9) = 1
```

Nghĩa là về mặt ước lượng, chỉ cần ít nhất 1 lần chuyển nước nữa vào bể là có thể đủ 13 lít. Thực tế trong lời giải, bước cuối cùng chuyển 6 lít từ gáo 2 vào bể, đúng với ước lượng này.

Hàm `h'` này là một ước lượng lạc quan vì nó chỉ xét lượng nước còn thiếu trong bể và giả sử mỗi thao tác tương lai có thể đóng góp tối đa bằng gáo lớn nhất. Nó chưa tính thêm các thao tác phụ như múc nước từ sông, chuyển giữa các gáo hoặc vứt nước để tạo ra đúng lượng cần đổ vào bể. Do đó `h'` thường nhỏ hơn hoặc bằng số thao tác thật còn lại.

Vai trò của `h'` trong A*:

- Giúp thuật toán ưu tiên các trạng thái có lượng nước trong bể gần với `M` hơn.
- Kết hợp với `g(s)` để không chỉ chọn trạng thái "có vẻ gần đích", mà còn quan tâm số thao tác đã dùng.
- Làm giảm số trạng thái phải xét so với tìm kiếm không có thông tin như BFS hoặc UCS.

Với cùng dữ liệu `3 13 7 8 9`, A* xét `203` trạng thái, trong khi BFS và UCS xét `479` trạng thái. Điều này cho thấy hàm `h'` giúp thuật toán định hướng quá trình tìm kiếm tốt hơn, nhưng vẫn tìm được lời giải có `7` thao tác.

---

## Nhận xét

A* phù hợp với bài toán này vì mỗi thao tác có chi phí bằng nhau và ta có thể xây dựng được hàm ước lượng còn thiếu dựa trên lượng nước trong bể. Thuật toán vừa xét chi phí thật `g`, vừa dùng khoảng cách ước lượng `h'`, nên tìm kiếm có định hướng hơn BFS/UCS nhưng vẫn giữ được mục tiêu tìm lời giải ngắn.

