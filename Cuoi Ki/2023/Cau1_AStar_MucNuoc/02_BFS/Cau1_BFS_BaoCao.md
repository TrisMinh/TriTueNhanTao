# Câu 1 - Báo cáo thuật toán BFS

## Đề bài

Cho `n` cái gáo nước có dung tích lần lượt là `a1, a2, ..., an`. Cần múc đúng `M` lít nước từ bờ sông qua bể nước lớn, không được múc thiếu hoặc múc quá. Có thể múc nước vào gáo, chuyển nước giữa các gáo, chuyển nước từ gáo vào bể và vứt bỏ nước trong gáo. Mỗi hành động được tính là 1 thao tác.

Báo cáo này trình bày lời giải bằng thuật toán **BFS - Breadth First Search**.

---

## Mô hình trạng thái

Một trạng thái được biểu diễn dưới dạng:

```text
((x1, x2, ..., xn), B)
```

Trong đó:

- `x_i` là lượng nước hiện có trong gáo thứ `i`.
- `B` là lượng nước hiện có trong bể.
- Trạng thái ban đầu là tất cả gáo rỗng và bể rỗng.
- Trạng thái đích là trạng thái có `B = M`.

Với dữ liệu:

```text
3 13 7 8 9
```

trạng thái ban đầu là:

```text
((0, 0, 0), 0)
```

---

## Các phép sinh trạng thái

Từ một trạng thái hiện tại, chương trình sinh các trạng thái kế tiếp theo 4 nhóm thao tác:

| Nhóm thao tác | Điều kiện | Kết quả |
|---|---|---|
| Múc nước từ sông vào gáo `i` | Gáo `i` chưa đầy | Gáo `i` được đổ đầy |
| Chuyển nước từ gáo `i` vào bể | Gáo `i` có nước và không làm bể vượt quá `M` | Gáo `i` về 0, bể tăng thêm lượng nước trong gáo |
| Chuyển nước từ gáo `i` sang gáo `j` | Gáo `i` có nước, gáo `j` chưa đầy | Chuyển đến khi gáo nguồn hết hoặc gáo đích đầy |
| Vứt nước trong gáo `i` | Gáo `i` có nước | Gáo `i` về 0 |

Trước khi tìm kiếm, chương trình kiểm tra:

```text
M % gcd(a1, a2, ..., an) == 0
```

Nếu điều kiện này sai thì không thể tạo chính xác `M` lít từ các gáo đã cho.

---

## Thuật toán BFS

BFS duyệt trạng thái theo từng mức. Tất cả trạng thái cách trạng thái ban đầu 1 thao tác được xét trước, sau đó đến các trạng thái cách 2 thao tác, rồi 3 thao tác, ...

Vì mỗi thao tác đều có chi phí bằng 1, BFS đảm bảo khi gặp trạng thái có `B = M` lần đầu tiên thì đó là lời giải có số thao tác ít nhất.

Trong chương trình:

- `queue` là hàng đợi dùng để lưu các trạng thái chờ xét.
- `visited` lưu các trạng thái đã được phát hiện để tránh lặp vô hạn.
- `parent` lưu trạng thái cha và hành động sinh ra trạng thái hiện tại.
- Khi tìm thấy đích, hàm `reconstruct_actions` truy vết ngược từ trạng thái đích về trạng thái đầu để in lời giải.

Đoạn xử lý chính:

```python
start_state = (tuple([0] * n), 0)
queue = deque([start_state])
parent = {start_state: (None, None)}
visited = {start_state}

while queue:
    current_state = queue.popleft()

    if tank_amount == target:
        return reconstruct_actions(parent, current_state), visited_count

    for next_state, action in generate_neighbors(current_state, capacities, target):
        if next_state not in visited:
            visited.add(next_state)
            parent[next_state] = (current_state, action)
            queue.append(next_state)
```

---

## Kết quả thực thi với dữ liệu `3 13 7 8 9`

Lệnh chạy:

```powershell
python "2023/Cau1_AStar_MucNuoc/02_BFS/cau1_bfs.py"
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

BFS tìm được lời giải gồm `7` thao tác, đây là số thao tác ít nhất vì BFS duyệt theo độ sâu tăng dần. Tuy nhiên BFS không dùng hàm định hướng nên số trạng thái đã xét khá nhiều: `479` trạng thái. So với A*, BFS chắc chắn tối ưu trong bài toán chi phí đều, nhưng thường tốn bộ nhớ và thời gian hơn khi không gian trạng thái lớn.

