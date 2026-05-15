# Câu 1 - Báo cáo thuật toán UCS

## Đề bài

Cho `n` gáo nước, gáo thứ `i` có dung tích tối đa `a_i` lít. Cần đưa đúng `M` lít nước vào bể lớn bằng các thao tác múc, chuyển và vứt nước. Mỗi thao tác tính chi phí là 1. Nếu không có cách tạo đúng `M` lít thì in `Khong co dap an`.

Báo cáo này trình bày lời giải bằng thuật toán **UCS - Uniform Cost Search**.

---

## Mô hình trạng thái

Trạng thái được biểu diễn:

```text
((x1, x2, ..., xn), B)
```

Trong đó:

- `x_i` là lượng nước hiện có trong gáo thứ `i`.
- `B` là lượng nước đã đưa vào bể.
- Trạng thái đầu là `((0, 0, ..., 0), 0)`.
- Trạng thái đích thỏa mãn `B = M`.

Với input:

```text
3 13 7 8 9
```

ta cần dùng 3 gáo dung tích 7, 8, 9 lít để đưa đúng 13 lít nước vào bể.

---

## Sinh trạng thái

Từ một trạng thái, chương trình sinh trạng thái kế tiếp bằng các thao tác:

| Thao tác | Mô tả |
|---|---|
| Múc từ sông vào gáo | Đổ đầy một gáo chưa đầy |
| Chuyển từ gáo vào bể | Đưa toàn bộ nước trong gáo vào bể nếu không vượt `M` |
| Chuyển giữa hai gáo | Rót từ gáo nguồn sang gáo đích đến khi nguồn hết hoặc đích đầy |
| Vứt bỏ nước | Làm rỗng một gáo đang có nước |

Mỗi thao tác có chi phí bằng 1.

Điều kiện kiểm tra nhanh:

```text
M % gcd(a1, a2, ..., an) == 0
```

Nếu không thỏa mãn, chương trình kết luận không có đáp án.

---

## Thuật toán UCS

UCS luôn mở rộng trạng thái có tổng chi phí thật nhỏ nhất từ trạng thái đầu đến trạng thái hiện tại.

Trong bài này, vì mọi thao tác đều có chi phí bằng 1, chi phí của một trạng thái chính là số thao tác đã thực hiện. Khi UCS lấy được trạng thái đích ra khỏi hàng đợi ưu tiên, lời giải đó là lời giải có số thao tác ít nhất.

Trong chương trình:

- `frontier` là hàng đợi ưu tiên theo `current_cost`.
- `cost[state]` lưu chi phí tốt nhất đã biết để đến trạng thái đó.
- `parent` lưu trạng thái trước và hành động dùng để truy vết.
- `visited` tránh xử lý lại trạng thái đã lấy ra khỏi heap.

Đoạn xử lý chính:

```python
start_state = (tuple([0] * n), 0)
frontier = []
heapq.heappush(frontier, (0, order, start_state))

parent = {start_state: (None, None)}
cost = {start_state: 0}
visited = set()

while frontier:
    current_cost, _, current_state = heapq.heappop(frontier)

    if current_state in visited:
        continue

    visited.add(current_state)

    if tank_amount == target:
        return reconstruct_actions(parent, current_state), len(visited)

    for next_state, action in generate_neighbors(current_state, capacities, target):
        next_cost = current_cost + 1

        if next_state not in cost or next_cost < cost[next_state]:
            cost[next_state] = next_cost
            parent[next_state] = (current_state, action)
            order += 1
            heapq.heappush(frontier, (next_cost, order, next_state))
```

---

## Kết quả thực thi với dữ liệu `3 13 7 8 9`

Lệnh chạy:

```powershell
python "2023/Cau1_AStar_MucNuoc/05_UCS/cau1_ucs.py"
```

Kết quả:

```text
Nhap: 3 13 7 8 9
So trang thai da xet: 479
So thao tac: 7
1. Chuyen/Muc 7 lit nuoc tu bo song qua gao 1 (Gao 1: 7 lit, Gao 2: 0 lit, Gao 3: 0 lit, Be: 0 lit)
2. Chuyen/Muc 8 lit nuoc tu bo song qua gao 2 (Gao 1: 7 lit, Gao 2: 8 lit, Gao 3: 0 lit, Be: 0 lit)
3. Chuyen/Muc 7 lit nuoc tu gao 1 qua be (Gao 1: 0 lit, Gao 2: 8 lit, Gao 3: 0 lit, Be: 7 lit)
4. Chuyen/Muc 7 lit nuoc tu bo song qua gao 1 (Gao 1: 7 lit, Gao 2: 8 lit, Gao 3: 0 lit, Be: 7 lit)
5. Chuyen/Muc 7 lit nuoc tu gao 1 qua gao 3 (Gao 1: 0 lit, Gao 2: 8 lit, Gao 3: 7 lit, Be: 7 lit)
6. Chuyen/Muc 2 lit nuoc tu gao 2 qua gao 3 (Gao 1: 0 lit, Gao 2: 6 lit, Gao 3: 9 lit, Be: 7 lit)
7. Chuyen/Muc 6 lit nuoc tu gao 2 qua be (Gao 1: 0 lit, Gao 2: 0 lit, Gao 3: 9 lit, Be: 13 lit)
```

---

## Nhận xét

UCS tìm được lời giải tối ưu gồm `7` thao tác. Vì tất cả thao tác có cùng chi phí bằng 1, UCS cho kết quả tương tự BFS về số thao tác và số trạng thái đã xét trong lần chạy này.

Điểm mạnh của UCS là có thể mở rộng tốt cho trường hợp các thao tác có chi phí khác nhau. Ví dụ nếu thao tác vứt nước hoặc chuyển giữa gáo có chi phí khác 1, UCS vẫn có thể tìm lời giải chi phí nhỏ nhất, trong khi BFS không còn đảm bảo tối ưu theo tổng chi phí.

