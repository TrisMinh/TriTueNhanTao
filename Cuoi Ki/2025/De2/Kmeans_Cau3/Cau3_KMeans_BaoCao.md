# Câu 3: Phân cụm dữ liệu Countries bằng K-means

## a) Xây dựng hàm đo khoảng cách sử dụng độ đo Euclid

### Trả lời: Minh họa tính khoảng cách

Trong thuật toán K-means, để biết một điểm dữ liệu thuộc cụm nào, ta cần tính khoảng cách từ điểm đó đến từng tâm cụm.

Với dữ liệu `Countries.csv`, mỗi quốc gia được biểu diễn bởi 2 thuộc tính:

- `Longitude`: kinh độ
- `Latitude`: vĩ độ

Giả sử có hai điểm:

```text
A = (x1, y1)
B = (x2, y2)
```

Khoảng cách Euclid giữa hai điểm được tính bằng công thức:

```text
d(A, B) = sqrt((x1 - x2)^2 + (y1 - y2)^2)
```

Ví dụ:

```text
A = (2, 3)
B = (5, 7)

d(A, B) = sqrt((2 - 5)^2 + (3 - 7)^2)
        = sqrt(9 + 16)
        = 5
```

Trong K-means, điểm dữ liệu sẽ được gán vào cụm có tâm cụm gần nó nhất theo khoảng cách Euclid.

### Trả lời: Dán code hàm tính khoảng cách

```python
def euclidean_distance(point_a, point_b):
    return np.sqrt(np.sum((point_a - point_b) ** 2))
```

## b) Xây dựng hàm chứa thuật toán K-means để phân cụm

### Trả lời: Dán code về hàm

```python
def initialize_centroids(X, k, rng):
    indices = rng.choice(len(X), size=k, replace=False)
    return X[indices].copy()


def assign_clusters(X, centroids):
    labels = []

    for point in X:
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
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


def kmeans(X, k, max_iters=100, random_state=42):
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
```

### Giải thích chương trình

Thuật toán K-means hoạt động theo các bước chính:

1. Chọn ngẫu nhiên `k` điểm làm tâm cụm ban đầu.
2. Tính khoảng cách Euclid từ mỗi điểm dữ liệu đến từng tâm cụm.
3. Gán mỗi điểm vào cụm có tâm gần nhất.
4. Cập nhật lại tâm cụm bằng trung bình cộng các điểm trong cụm.
5. Lặp lại bước 2 đến bước 4 cho đến khi tâm cụm không thay đổi nhiều hoặc đạt số vòng lặp tối đa.

Trong bài này, dữ liệu dùng để phân cụm là hai cột:

```text
Longitude, Latitude
```

Sau khi chạy K-means, mỗi quốc gia sẽ được gán thêm một nhãn cụm `Cluster`.

Biểu đồ phân cụm:

![Biểu đồ phân cụm](cau3_clusters.png)

## c) Xây dựng hàm khảo sát việc lựa chọn k

### Trả lời: Dán code về hàm và giải thích cách lựa chọn k phù hợp

Để chọn số cụm `k`, ta dùng phương pháp Elbow. Ý tưởng là chạy K-means với nhiều giá trị `k`, sau đó tính tổng bình phương khoảng cách từ các điểm đến tâm cụm của nó.

Giá trị này gọi là WCSS:

```text
WCSS = tổng khoảng cách bình phương từ từng điểm đến tâm cụm tương ứng
```

Nếu `k` tăng thì WCSS sẽ giảm. Tuy nhiên, ta không nên chọn `k` quá lớn. Ta chọn `k` tại vị trí đường cong bắt đầu giảm chậm lại, gọi là điểm khuỷu tay.

Code tính WCSS:

```python
def compute_wcss(X, labels, centroids):
    total = 0

    for point, label in zip(X, labels):
        total += euclidean_distance(point, centroids[label]) ** 2

    return total
```

Code chạy Elbow:

```python
def run_kmeans_best_of_n(X, k, n_init=20, max_iters=100):
    best_centroids = None
    best_labels = None
    best_wcss = float("inf")

    for seed in range(n_init):
        centroids, labels, wcss = kmeans(X, k, max_iters=max_iters, random_state=seed)

        if wcss < best_wcss:
            best_centroids = centroids
            best_labels = labels
            best_wcss = wcss

    return best_centroids, best_labels, best_wcss


def elbow_method(X, k_values):
    results = []

    for k in k_values:
        centroids, labels, wcss = run_kmeans_best_of_n(X, k)
        results.append((k, centroids, labels, wcss))

    return results
```

Biểu đồ Elbow:

![Biểu đồ elbow](cau3_elbow.png)

### Trả lời: Dán kết quả với k

Kết quả khảo sát WCSS:

| k | WCSS |
|---:|---:|
| 1 | 1184443.06 |
| 2 | 565269.22 |
| 3 | 264675.95 |
| 4 | 205635.32 |
| 5 | 151819.98 |
| 6 | 123190.06 |
| 7 | 101082.70 |
| 8 | 79332.18 |
| 9 | 66944.27 |
| 10 | 61108.94 |

Quan sát bảng và biểu đồ Elbow, WCSS giảm rất mạnh khi tăng `k` từ 1 đến 3. Sau đó WCSS vẫn giảm nhưng tốc độ giảm chậm hơn. Trong bài này em chọn:

```text
k = 5
```

Để giải thích rõ hơn, ta xét mức giảm WCSS khi tăng `k`:

| Tăng k | Mức giảm WCSS | Tỉ lệ giảm |
|---:|---:|---:|
| 1 -> 2 | 619173.84 | 52.28% |
| 2 -> 3 | 300593.27 | 53.18% |
| 3 -> 4 | 59040.63 | 22.31% |
| 4 -> 5 | 53815.34 | 26.17% |
| 5 -> 6 | 28629.92 | 18.86% |
| 6 -> 7 | 22107.36 | 17.95% |
| 7 -> 8 | 21750.52 | 21.52% |
| 8 -> 9 | 12387.91 | 15.62% |
| 9 -> 10 | 5835.33 | 8.72% |

Thuật toán không tự biết chắc chắn `k = 5` là tốt nhất. Phương pháp Elbow chỉ giúp ta khảo sát nhiều giá trị `k`, tính WCSS và vẽ biểu đồ. Sau đó người làm bài quan sát điểm mà đường cong bắt đầu bớt dốc để chọn `k` phù hợp.

Lý do em chọn `k = 5`:

- WCSS tại `k = 5` đã giảm nhiều so với các giá trị k nhỏ.
- Sau `k = 5`, mức giảm WCSS giảm rõ rệt: từ `53815.34` khi tăng `4 -> 5` xuống còn `28629.92` khi tăng `5 -> 6`.
- Với dữ liệu kinh độ và vĩ độ của các quốc gia, `k = 5` cho kết quả phân cụm dễ quan sát trên bản đồ phân tán.

Tâm các cụm khi chọn `k = 5`:

| Cụm | Longitude | Latitude | Số nước |
|---:|---:|---:|---:|
| 0 | -161.0289 | -18.2036 | 7 |
| 1 | 45.9784 | 9.9238 | 53 |
| 2 | 130.3144 | 9.5931 | 33 |
| 3 | 6.9566 | 36.6158 | 68 |
| 4 | -69.8508 | 9.2617 | 39 |

Kết luận: với `k = 5`, thuật toán K-means chia dữ liệu quốc gia thành 5 nhóm dựa trên vị trí địa lý gồm kinh độ và vĩ độ. Kết quả phân cụm được lưu trong file `cau3_countries_clustered.csv`.

## File chương trình

Chương trình đầy đủ nằm trong file:

```text
cau3_kmeans.py
```

Các file kết quả:

```text
cau3_elbow.png
cau3_clusters.png
cau3_countries_clustered.csv
```
