# Câu 1 - Tổng hợp các thuật toán tìm kiếm

Theo phần ôn tập của thầy, nhóm tìm kiếm gồm:

```text
BFS, DFS, A*, tham lam tốt nhất, minimax, UCS
```

Với bài lâu đài tìm đường thoát, em đã cài đặt 5 thuật toán phù hợp:

- BFS
- DFS
- A*
- Greedy Best-First Search, tức tham lam tốt nhất
- UCS

Minimax không được cài cho bài này vì Minimax phù hợp với trò chơi đối kháng có hai người chơi MAX/MIN, không phù hợp trực tiếp với bài toán tìm đường một tác nhân trong mê cung.

## Bảng tổng hợp

| Thuật toán | Thư mục | File output | Số ô đường đi | Số bước xét | Ghi chú |
|---|---|---|---|---:|---:|---|
| A* | `01_AStar` | `A_out.csv` | 7 | 11 | Thuật toán chính theo đề |
| BFS | `02_BFS` | `BFS_out.csv` | 7 | 16 | Tìm đường ngắn khi chi phí mỗi bước bằng nhau |
| DFS | `03_DFS` | `DFS_out.csv` | 9 | 9 | Tìm được đường thoát nhưng không đảm bảo ngắn nhất |
| Greedy Best-First | `04_Greedy_BestFirst` | `Greedy_out.csv` | 7 | 9 | Chọn ô có `h(x)` nhỏ nhất |
| UCS | `05_UCS` | `UCS_out.csv` | 7 | 16 | Chọn ô có `g(x)` nhỏ nhất |

## Cấu trúc thư mục

```text
BFS_DFS_Astar_Cau1/
├── A_in.csv
├── Cau1_TongHop_5ThuatToan_BaoCao.md
├── 01_AStar/
├── 02_BFS/
├── 03_DFS/
├── 04_Greedy_BestFirst/
└── 05_UCS/
```

## Kết quả đường đi

A*, BFS, Greedy và UCS đều tìm được đường:

```text
7
5,5
5,6
5,7
5,8
6,8
7,8
7,9
```

DFS tìm được đường khác:

```text
9
5,5
4,5
3,5
3,4
3,3
2,3
1,3
1,2
0,2
```

## Nhận xét

Trong dữ liệu này:

- A*, BFS, Greedy và UCS đều tìm được đường đi gồm 7 ô.
- DFS tìm được đường đi gồm 9 ô vì DFS đi sâu theo một nhánh trước và không đảm bảo đường ngắn nhất.
- Greedy xét ít bước nhất trong nhóm tìm được đường 7 ô, nhưng về lý thuyết Greedy không đảm bảo tối ưu.
- UCS và BFS có kết quả giống nhau vì chi phí mỗi bước đều bằng 1.
- A* cân bằng giữa chi phí đã đi `g(x)` và heuristic `h(x)`, nên là thuật toán phù hợp nhất với yêu cầu đề bài.

## Lệnh chạy

```powershell
python "2025/De2/BFS_DFS_Astar_Cau1/01_AStar/cau1_astar.py"
python "2025/De2/BFS_DFS_Astar_Cau1/02_BFS/cau1_bfs.py"
python "2025/De2/BFS_DFS_Astar_Cau1/03_DFS/cau1_dfs.py"
python "2025/De2/BFS_DFS_Astar_Cau1/04_Greedy_BestFirst/cau1_greedy_best_first.py"
python "2025/De2/BFS_DFS_Astar_Cau1/05_UCS/cau1_ucs.py"
```
