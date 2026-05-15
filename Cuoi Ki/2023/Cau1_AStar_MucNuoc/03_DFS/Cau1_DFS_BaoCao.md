# Câu 1 - Báo cáo thuật toán DFS

## Đề bài

Bài toán yêu cầu dùng `n` gáo nước có dung tích `a1, a2, ..., an` để múc đúng `M` lít nước vào bể. Không được để bể vượt quá `M`, không được dừng khi còn thiếu nước, và thao tác vứt bỏ nước cũng được tính là 1 thao tác.

Báo cáo này trình bày cách giải bằng thuật toán **DFS - Depth First Search**.

---

## Mô hình trạng thái

Trạng thái của bài toán:

```text
((x1, x2, ..., xn), B)
```

Trong đó:

- `x_i` là lượng nước trong gáo thứ `i`.
- `B` là lượng nước trong bể.
- Bắt đầu tại `((0, 0, ..., 0), 0)`.
- Kết thúc khi `B = M`.

Với dữ liệu:

```text
3 13 7 8 9
```

ta có 3 gáo với dung tích 7, 8, 9 lít và cần đưa đúng 13 lít vào bể.

---

## Sinh trạng thái kế tiếp

Hàm `generate_neighbors` sinh các trạng thái mới từ trạng thái hiện tại:

- Đổ đầy một gáo từ bờ sông.
- Chuyển toàn bộ nước trong một gáo vào bể nếu không vượt quá `M`.
- Chuyển nước từ gáo này sang gáo khác.
- Vứt bỏ toàn bộ nước trong một gáo.

Mỗi trạng thái mới đi kèm mô tả thao tác để cuối cùng có thể in lại đường đi.

Chương trình cũng kiểm tra nhanh khả năng có đáp án bằng:

```text
M % gcd(a1, a2, ..., an) == 0
```

Nếu điều kiện sai, chương trình in `Khong co dap an`.

---

## Thuật toán DFS

DFS dùng ngăn xếp để đi sâu theo một nhánh trước. Khi không thể tiếp tục hoặc gặp trạng thái đã xét, thuật toán quay lui sang nhánh khác.

Trong chương trình:

- `stack` lưu các trạng thái chờ xét.
- `visited` lưu các trạng thái đã thật sự được lấy ra xử lý.
- `discovered` lưu các trạng thái đã từng được đưa vào stack để tránh đưa trùng.
- `parent` lưu đường đi để truy vết lời giải.

Đoạn xử lý chính:

```python
start_state = (tuple([0] * n), 0)
stack = [start_state]
parent = {start_state: (None, None)}
visited = set()
discovered = {start_state}

while stack:
    current_state = stack.pop()

    if current_state in visited:
        continue

    visited.add(current_state)

    if tank_amount == target:
        return reconstruct_actions(parent, current_state), visited_count

    neighbors = generate_neighbors(current_state, capacities, target)

    for next_state, action in reversed(neighbors):
        if next_state not in discovered:
            discovered.add(next_state)
            parent[next_state] = (current_state, action)
            stack.append(next_state)
```

Việc duyệt `reversed(neighbors)` giúp thứ tự lấy ra khỏi stack tương ứng với thứ tự sinh trạng thái ban đầu.

---

## Kết quả thực thi với dữ liệu `3 13 7 8 9`

Lệnh chạy:

```powershell
python "2023/Cau1_AStar_MucNuoc/03_DFS/cau1_dfs.py"
```

Kết quả:

```text
Nhap: 3 13 7 8 9
So trang thai da xet: 11
So thao tac: 10
1. Chuyen/Muc 7 lit nuoc tu bo song qua gao 1 (Gao 1: 7 lit, Gao 2: 0 lit, Gao 3: 0 lit, Be: 0 lit)
2. Chuyen/Muc 8 lit nuoc tu bo song qua gao 2 (Gao 1: 7 lit, Gao 2: 8 lit, Gao 3: 0 lit, Be: 0 lit)
3. Chuyen/Muc 9 lit nuoc tu bo song qua gao 3 (Gao 1: 7 lit, Gao 2: 8 lit, Gao 3: 9 lit, Be: 0 lit)
4. Chuyen/Muc 7 lit nuoc tu gao 1 qua be (Gao 1: 0 lit, Gao 2: 8 lit, Gao 3: 9 lit, Be: 7 lit)
5. Chuyen/Muc 7 lit nuoc tu bo song qua gao 1 (Gao 1: 7 lit, Gao 2: 8 lit, Gao 3: 9 lit, Be: 7 lit)
6. Vut bo toan bo 8 lit nuoc cua gao 2. (Gao 1: 7 lit, Gao 2: 0 lit, Gao 3: 9 lit, Be: 7 lit)
7. Chuyen/Muc 7 lit nuoc tu gao 1 qua gao 2 (Gao 1: 0 lit, Gao 2: 7 lit, Gao 3: 9 lit, Be: 7 lit)
8. Chuyen/Muc 7 lit nuoc tu bo song qua gao 1 (Gao 1: 7 lit, Gao 2: 7 lit, Gao 3: 9 lit, Be: 7 lit)
9. Chuyen/Muc 1 lit nuoc tu gao 1 qua gao 2 (Gao 1: 6 lit, Gao 2: 8 lit, Gao 3: 9 lit, Be: 7 lit)
10. Chuyen/Muc 6 lit nuoc tu gao 1 qua be (Gao 1: 0 lit, Gao 2: 8 lit, Gao 3: 9 lit, Be: 13 lit)
```

---

## Nhận xét

DFS tìm được một lời giải hợp lệ sau khi xét `11` trạng thái, nhưng lời giải có `10` thao tác, dài hơn lời giải tối ưu `7` thao tác của A*, BFS và UCS. Điều này đúng với đặc điểm của DFS: thuật toán có thể tìm lời giải nhanh nếu may mắn đi đúng nhánh, nhưng không đảm bảo lời giải có số thao tác ít nhất.

Vì vậy, DFS phù hợp để minh họa quá trình tìm kiếm theo chiều sâu, nhưng nếu đề bài yêu cầu số thao tác ít nhất thì BFS, UCS hoặc A* phù hợp hơn.

