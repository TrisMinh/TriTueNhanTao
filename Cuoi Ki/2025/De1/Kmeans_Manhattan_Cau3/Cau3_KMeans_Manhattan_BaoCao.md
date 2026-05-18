# Câu 3 - Phân cụm dữ liệu Countries bằng thuật toán K-means dùng khoảng cách Manhattan

## Đề bài

Cho tập dữ liệu `Countries.csv`. Hãy viết chương trình phân cụm bằng thuật toán K-means.

Yêu cầu:

1. Xây dựng hàm đo khoảng cách sử dụng độ đo Manhattan.
2. Xây dựng hàm chứa thuật toán K-means để phân cụm.
3. Xây dựng hàm để khảo sát việc lựa chọn `k`.

Chương trình được cài đặt trong file:

```text
cau3_kmeans_manhattan.py
```

Trong bài này, em chỉ dùng:

- `numpy` để tính toán mảng và giá trị trung bình.
- `matplotlib` để vẽ biểu đồ.
- `csv` và `pathlib` là thư viện chuẩn của Python để đọc/ghi file.

Không dùng thư viện K-means có sẵn như `sklearn.cluster.KMeans`.

---

## a) Xây dựng hàm đo khoảng cách sử dụng độ đo Manhattan

### Trả lời: Hàm khoảng cách Manhattan

Mỗi quốc gia trong `Countries.csv` được biểu diễn bằng 2 đặc trưng:

- `Longitude`: kinh độ
- `Latitude`: vĩ độ

Ta coi mỗi quốc gia là một điểm trong mặt phẳng 2 chiều:

```text
P = (Longitude, Latitude)
```

Giả sử có hai điểm:

```text
A = (x1, y1)
B = (x2, y2)
```

Khoảng cách Manhattan giữa hai điểm được tính theo công thức:

```text
d(A, B) = |x1 - x2| + |y1 - y2|
```

Trong thuật toán K-means, khoảng cách Manhattan được dùng để xác định một điểm dữ liệu gần tâm cụm nào nhất. Điểm dữ liệu sẽ được gán vào cụm có tâm gần nhất theo tổng độ lệch tuyệt đối trên từng chiều.

### Trả lời: Dán code hàm tính khoảng cách

```python
def manhattan_distance(point_a, point_b):
    return np.sum(np.abs(point_a - point_b))
```

Giải thích:

- `point_a - point_b`: tính hiệu từng tọa độ.
- `np.abs(...)`: lấy giá trị tuyệt đối của từng hiệu.
- `np.sum(...)`: cộng các độ lệch tuyệt đối để ra khoảng cách Manhattan.

Ví dụ:

```text
A = (2, 3)
B = (5, 7)

d(A, B) = |2 - 5| + |3 - 7|
        = 3 + 4
        = 7
```

---

## b) Xây dựng hàm chứa thuật toán K-means để phân cụm

### Trả lời: Ý tưởng thuật toán K-means với khoảng cách Manhattan

K-means là thuật toán phân cụm không giám sát. Thuật toán không cần nhãn đúng ban đầu mà tự chia dữ liệu thành `k` nhóm dựa trên khoảng cách giữa các điểm.

Các bước chính:

1. Chọn số cụm `k`.
2. Khởi tạo ngẫu nhiên `k` tâm cụm ban đầu.
3. Với mỗi điểm dữ liệu, tính khoảng cách Manhattan từ điểm đó đến từng tâm cụm.
4. Gán điểm dữ liệu vào cụm có tâm gần nhất.
5. Cập nhật lại tâm cụm bằng trung bình cộng các điểm trong cụm.
6. Lặp lại bước 3 đến bước 5 cho đến khi tâm cụm không thay đổi nhiều hoặc đạt số vòng lặp tối đa.

Trong bài này, dữ liệu phân cụm là:

```text
X = [Longitude, Latitude]
```

Sau khi chạy K-means, mỗi quốc gia được gán thêm một nhãn cụm `Cluster`.

### Trả lời: Dán code thuật toán K-means

Dưới đây là toàn bộ chương trình hoàn thiện. Có thể copy nguyên khối code này để chạy:

```python
from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np


DATA_FILE_NAME = "Countries.csv"


def manhattan_distance(point_a, point_b):
    return np.sum(np.abs(point_a - point_b))


def initialize_centroids(X, k, rng):
    indices = rng.choice(len(X), size=k, replace=False)
    return X[indices].copy()


def assign_clusters(X, centroids):
    labels = []

    for point in X:
        distances = [manhattan_distance(point, centroid) for centroid in centroids]
        labels.append(int(np.argmin(distances)))

    return np.array(labels)


def update_centroids(X, labels, k, old_centroids, rng):
    centroids = old_centroids.copy()

    for cluster_id in range(k):
        points = X[labels == cluster_id]

        if len(points) > 0:
            centroids[cluster_id] = np.mean(points, axis=0)
        else:
            centroids[cluster_id] = X[rng.integers(len(X))]

    return centroids


def compute_wcss(X, labels, centroids):
    total = 0

    for point, label in zip(X, labels):
        total += manhattan_distance(point, centroids[label]) ** 2

    return total


def kmeans_manhattan(X, k, max_iters=100, random_state=42):
    if k <= 0:
        raise ValueError("k phai lon hon 0")
    if k > len(X):
        raise ValueError("k khong duoc lon hon so diem du lieu")

    rng = np.random.default_rng(random_state)
    centroids = initialize_centroids(X, k, rng)

    for _ in range(max_iters):
        labels = assign_clusters(X, centroids)
        new_centroids = update_centroids(X, labels, k, centroids, rng)

        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids

    labels = assign_clusters(X, centroids)
    wcss = compute_wcss(X, labels, centroids)

    return centroids, labels, wcss


def run_kmeans_best_of_n(X, k, n_init=20, max_iters=100):
    best_centroids = None
    best_labels = None
    best_wcss = float("inf")

    for seed in range(n_init):
        centroids, labels, wcss = kmeans_manhattan(
            X,
            k,
            max_iters=max_iters,
            random_state=seed,
        )

        if wcss < best_wcss:
            best_centroids = centroids
            best_labels = labels
            best_wcss = wcss

    return best_centroids, best_labels, best_wcss
```

### Biểu đồ phân cụm với k = 3

Sau khi khảo sát `k`, em chọn `k = 3` để phân cụm dữ liệu các quốc gia.

![Biểu đồ phân cụm Countries với k = 3 dùng Manhattan](cau3_manhattan_clusters.png)

Nhận xét:

- Mỗi màu là một cụm quốc gia.
- Trục hoành là `Longitude`.
- Trục tung là `Latitude`.
- Dấu `x` màu đen là tâm cụm.
- Vì dữ liệu là kinh độ và vĩ độ, các cụm thể hiện sự gần nhau tương đối về vị trí địa lý.
- Khoảng cách Manhattan đo mức chênh lệch theo từng trục rồi cộng lại, nên cách gán cụm có thể khác so với khi dùng các độ đo khoảng cách khác.

Tâm các cụm khi chọn `k = 3`:

| Cụm | Longitude | Latitude | Số nước |
|---:|---:|---:|---:|
| 0 | 122.1545 | 8.1700 | 39 |
| 1 | 21.2718 | 26.2067 | 115 |
| 2 | -83.7257 | 5.0822 | 46 |

---

## c) Xây dựng hàm để khảo sát việc lựa chọn k

### Trả lời: Phương pháp chọn k

Để khảo sát số cụm `k`, em sử dụng phương pháp **Elbow Method**.

Ý tưởng:

1. Chạy K-means với nhiều giá trị `k`, ví dụ từ 1 đến 10.
2. Với mỗi giá trị `k`, tính tổng bình phương khoảng cách Manhattan từ các điểm đến tâm cụm tương ứng.
3. Giá trị này gọi là WCSS.
4. Vẽ biểu đồ WCSS theo `k`.
5. Chọn `k` tại vị trí đường cong bắt đầu giảm chậm lại, gọi là điểm khuỷu tay.

WCSS được tính như sau:

```text
WCSS = tổng khoảng cách Manhattan bình phương từ từng điểm đến tâm cụm của nó
```

Nếu `k` tăng thì WCSS thường giảm. Tuy nhiên, không nên chọn `k` quá lớn vì số cụm nhiều sẽ làm mô hình khó diễn giải. Vì vậy, ta chọn `k` tại điểm cân bằng giữa WCSS nhỏ và số cụm vừa phải.

### Trả lời: Dán code khảo sát k

Code tính WCSS:

```python
def compute_wcss(X, labels, centroids):
    total = 0

    for point, label in zip(X, labels):
        total += manhattan_distance(point, centroids[label]) ** 2

    return total
```

Code chạy K-means nhiều lần để lấy kết quả tốt nhất:

```python
def run_kmeans_best_of_n(X, k, n_init=20, max_iters=100):
    best_centroids = None
    best_labels = None
    best_wcss = float("inf")

    for seed in range(n_init):
        centroids, labels, wcss = kmeans_manhattan(
            X,
            k,
            max_iters=max_iters,
            random_state=seed,
        )

        if wcss < best_wcss:
            best_centroids = centroids
            best_labels = labels
            best_wcss = wcss

    return best_centroids, best_labels, best_wcss
```

Code khảo sát nhiều giá trị `k`:

```python
def elbow_method(X, k_values):
    results = []

    for k in k_values:
        centroids, labels, wcss = run_kmeans_best_of_n(X, k)
        results.append((k, centroids, labels, wcss))

    return results
```

Code vẽ biểu đồ Elbow:

```python
def save_elbow_chart(k_values, wcss_values, output_file):
    plt.figure(figsize=(7, 5))
    plt.plot(k_values, wcss_values, marker="o")
    plt.xlabel("So cum k")
    plt.ylabel("WCSS")
    plt.title("Elbow Method - Manhattan")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=160)
    plt.close()
```

### Biểu đồ Elbow

![Biểu đồ Elbow khảo sát lựa chọn k dùng Manhattan](cau3_manhattan_elbow.png)

Kết quả khảo sát WCSS:

| k | WCSS |
|---:|---:|
| 1 | 1605529.66 |
| 2 | 889593.83 |
| 3 | 436388.95 |
| 4 | 341514.69 |
| 5 | 259894.97 |
| 6 | 200407.57 |
| 7 | 169197.48 |
| 8 | 131123.98 |
| 9 | 110975.89 |
| 10 | 100478.93 |

Mức giảm WCSS khi tăng `k`:

| Tăng k | Mức giảm WCSS | Tỉ lệ giảm |
|---:|---:|---:|
| 1 -> 2 | 715935.83 | 44.59% |
| 2 -> 3 | 453204.88 | 50.95% |
| 3 -> 4 | 94874.26 | 21.74% |
| 4 -> 5 | 81619.72 | 23.90% |
| 5 -> 6 | 59487.40 | 22.89% |
| 6 -> 7 | 31210.09 | 15.57% |
| 7 -> 8 | 38073.50 | 22.50% |
| 8 -> 9 | 20148.09 | 15.37% |
| 9 -> 10 | 10496.96 | 9.46% |

### Trả lời: Lựa chọn k

Quan sát bảng WCSS và biểu đồ Elbow:

- WCSS giảm rất mạnh khi tăng `k` từ 1 đến 3.
- Sau `k = 3`, mức giảm WCSS nhỏ hơn rõ rệt so với giai đoạn đầu.
- Khi tăng từ `k = 3` lên `k = 4`, WCSS chỉ giảm thêm `94874.26`, thấp hơn nhiều so với mức giảm `715935.83` từ `k = 1` lên `k = 2` và `453204.88` từ `k = 2` lên `k = 3`.
- Với dữ liệu kinh độ và vĩ độ, `k = 3` cho kết quả phân cụm gọn, dễ quan sát và phù hợp với điểm khuỷu tay trên biểu đồ Elbow.

Vì vậy, trong bài này em chọn:

```text
k = 3
```

Kết quả cuối cùng:

```text
K duoc chon: 3
WCSS = 436388.95
```

---

## Thực thi chương trình

Lệnh chạy:

```powershell
python "2025/De1/Kmeans_Manhattan_Cau3/cau3_kmeans_manhattan.py"
```

Kết quả chạy chính:

```text
KET QUA ELBOW - MANHATTAN
  k         WCSS
  1   1605529.66
  2    889593.83
  3    436388.95
  4    341514.69
  5    259894.97
  6    200407.57
  7    169197.48
  8    131123.98
  9    110975.89
 10    100478.93

TAM CUM
Cum    Longitude     Latitude  So nuoc
  0     122.1545       8.1700       39
  1      21.2718      26.2067      115
  2     -83.7257       5.0822       46

K duoc chon: 3, WCSS = 436388.95
```

Các file kết quả:

```text
cau3_manhattan_elbow.png
cau3_manhattan_clusters.png
cau3_countries_manhattan_clustered.csv
```

---

## Kết luận

Chương trình đã hoàn thành các yêu cầu:

- Có hàm đo khoảng cách Manhattan.
- Có thuật toán K-means tự cài đặt, không dùng thư viện phân cụm có sẵn.
- Có hàm khảo sát lựa chọn `k` bằng Elbow Method.
- Có biểu đồ Elbow để chọn `k`.
- Có biểu đồ phân cụm sau khi chọn `k = 3`.
- Có file kết quả `cau3_countries_manhattan_clustered.csv` chứa nhãn cụm của từng quốc gia.


