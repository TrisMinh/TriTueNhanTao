# Câu 1 - Báo cáo thuật toán Greedy Best First Search

## Đề bài

Cần dùng `n` gáo nước có dung tích `a1, a2, ..., an` để múc đúng `M` lít nước vào bể. Các thao tác gồm múc nước từ sông vào gáo, chuyển nước giữa các gáo, chuyển nước từ gáo vào bể và vứt bỏ nước. Mỗi thao tác có chi phí bằng 1.

Báo cáo này trình bày lời giải bằng thuật toán **Greedy Best First Search**.

---

## Mô hình trạng thái

Một trạng thái có dạng:

```text
((x1, x2, ..., xn), B)
```

Trong đó:

- `x_i` là lượng nước trong gáo thứ `i`.
- `B` là lượng nước trong bể.
- Mục tiêu là đạt `B = M`.

Trạng thái đầu với dữ liệu `3 13 7 8 9`:

```text
((0, 0, 0), 0)
```

---

## Hàm đánh giá h'

Greedy Best First Search chỉ dùng hàm heuristic `h'` để chọn trạng thái tiếp theo. Trong chương trình, hàm `h'` là:

```python
def heuristic(state, target, capacities):
    _, tank_amount = state
    remaining = target - tank_amount
    if remaining <= 0:
        return 0
    return math.ceil(remaining / max(capacities))
```

Ý nghĩa:

- `tank_amount` là lượng nước hiện có trong bể.
- `remaining = target - tank_amount` là lượng nước còn thiếu.
- `max(capacities)` là dung tích gáo lớn nhất.
- `ceil(remaining / max(capacities))` ước lượng số lần ít nhất cần đưa nước vào bể nếu mỗi lần đưa được tối đa bằng gáo lớn nhất.

Ví dụ với `M = 13`, các gáo `7, 8, 9`:

```text
h' ở trạng thái đầu = ceil(13 / 9) = 2
h' khi bể có 7 lít = ceil(6 / 9) = 1
h' khi bể có 13 lít = 0
```

Greedy ưu tiên trạng thái có `h'` nhỏ nhất, tức trạng thái có vẻ gần mục tiêu nhất.

---

## Thuật toán Greedy Best First Search

Khác với A*, Greedy không cộng thêm chi phí đã đi `g(s)`. Thuật toán chỉ dùng:

```text
priority(s) = h'(s)
```

Do đó Greedy thường đi nhanh về phía mục tiêu, nhưng không đảm bảo luôn tìm được lời giải ngắn nhất.

Trong chương trình:

- `frontier` là hàng đợi ưu tiên.
- `visited` lưu các trạng thái đã xét.
- `parent` dùng để truy vết thao tác.
- Mỗi trạng thái đưa vào heap có dạng `(h, order, state)`.

Đoạn xử lý chính:

```python
start_h = heuristic(start_state, target, capacities)
heapq.heappush(frontier, (start_h, order, start_state))

while frontier:
    _, _, current_state = heapq.heappop(frontier)

    if current_state in visited:
        continue

    visited.add(current_state)

    if tank_amount == target:
        return reconstruct_actions(parent, current_state), len(visited)

    for next_state, action in generate_neighbors(current_state, capacities, target):
        if next_state not in visited and next_state not in parent:
            parent[next_state] = (current_state, action)
            order += 1
            h = heuristic(next_state, target, capacities)
            heapq.heappush(frontier, (h, order, next_state))
```

---

## Kết quả thực thi với dữ liệu `3 13 7 8 9`

Lệnh chạy:

```powershell
python "2023/Cau1_AStar_MucNuoc/04_Greedy_BestFirst/cau1_greedy_best_first.py"
```

Kết quả:

```text
Nhap: 3 13 7 8 9
So trang thai da xet: 41
So thao tac: 7
1. Chuyen/Muc 7 lit nuoc tu bo song qua gao 1 (Gao 1: 7 lit, Gao 2: 0 lit, Gao 3: 0 lit, Be: 0 lit)
2. Chuyen/Muc 7 lit nuoc tu gao 1 qua be (Gao 1: 0 lit, Gao 2: 0 lit, Gao 3: 0 lit, Be: 7 lit)
3. Chuyen/Muc 7 lit nuoc tu bo song qua gao 1 (Gao 1: 7 lit, Gao 2: 0 lit, Gao 3: 0 lit, Be: 7 lit)
4. Chuyen/Muc 8 lit nuoc tu bo song qua gao 2 (Gao 1: 7 lit, Gao 2: 8 lit, Gao 3: 0 lit, Be: 7 lit)
5. Chuyen/Muc 7 lit nuoc tu gao 1 qua gao 3 (Gao 1: 0 lit, Gao 2: 8 lit, Gao 3: 7 lit, Be: 7 lit)
6. Chuyen/Muc 2 lit nuoc tu gao 2 qua gao 3 (Gao 1: 0 lit, Gao 2: 6 lit, Gao 3: 9 lit, Be: 7 lit)
7. Chuyen/Muc 6 lit nuoc tu gao 2 qua be (Gao 1: 0 lit, Gao 2: 0 lit, Gao 3: 9 lit, Be: 13 lit)
```

---

## Nhận xét

Với bộ dữ liệu này, Greedy Best First Search tìm được lời giải `7` thao tác và chỉ xét `41` trạng thái, ít hơn A* trong lần chạy hiện tại. Tuy nhiên Greedy chỉ dựa vào `h'`, không xét số thao tác đã đi, nên về lý thuyết không đảm bảo lời giải luôn tối ưu.

Trong bài toán múc nước, Greedy có thể hoạt động tốt khi hàm `h'` dẫn đường đúng, nhưng nếu một trạng thái có bể gần đủ nước lại cần nhiều thao tác phụ để xử lý các gáo, thuật toán vẫn có thể bị hút vào nhánh không tối ưu.

