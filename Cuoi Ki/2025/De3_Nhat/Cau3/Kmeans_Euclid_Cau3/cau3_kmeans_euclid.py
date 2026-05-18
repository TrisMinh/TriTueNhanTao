from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np


DATA_LIST = [
    ["Vietnam", 105.8342, 21.0278],
    ["Japan", 138.2529, 36.2048],
    ["South Korea", 127.7669, 35.9078],
    ["Australia", 133.7751, -25.2744],
    ["France", 2.2137, 46.2276],
    ["Germany", 10.4515, 51.1657],
    ["United Kingdom", -3.436, 55.3781],
    ["Italy", 12.5674, 41.8719],
    ["Spain", -3.7492, 40.4637],
    ["United States", -95.7129, 37.0902],
    ["Canada", -106.3468, 56.1304],
    ["Brazil", -51.9253, -14.235],
    ["Argentina", -63.6167, -38.4161],
    ["South Africa", 22.9375, -30.5595],
    ["Egypt", 30.8025, 26.8206],
    ["India", 78.9629, 20.5937],
    ["Thailand", 100.9925, 15.87],
    ["Singapore", 103.8198, 1.3521],
    ["New Zealand", 174.886, -40.9006],
    ["Russia", 105.3188, 61.524],
]


def euclidean_distance(point_a, point_b):
    return np.sqrt(np.sum((point_a - point_b) ** 2))


def load_country_data(data_list):
    rows = []

    for name, longitude, latitude in data_list:
        rows.append({
            "name": name,
            "Longitude": float(longitude),
            "Latitude": float(latitude),
        })

    X = np.array([[row["Longitude"], row["Latitude"]] for row in rows], dtype=float)
    return rows, X


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


def compute_wcss(X, labels, centroids):
    total = 0

    for point, label in zip(X, labels):
        total += euclidean_distance(point, centroids[label]) ** 2

    return total


def kmeans_euclid(X, k, max_iters=100, random_state=42):
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


def run_kmeans_best_of_n(X, k, n_init=30, max_iters=100):
    best_centroids = None
    best_labels = None
    best_wcss = float("inf")

    for seed in range(n_init):
        centroids, labels, wcss = kmeans_euclid(
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


def elbow_method(X, k_values):
    results = []

    for k in k_values:
        centroids, labels, wcss = run_kmeans_best_of_n(X, k)
        results.append((k, centroids, labels, wcss))

    return results


def choose_k_by_elbow(elbow_results):
    points = np.array([[k, wcss] for k, _, _, wcss in elbow_results], dtype=float)
    start = points[0]
    end = points[-1]
    line = end - start
    line_norm = np.linalg.norm(line)

    if line_norm == 0:
        return int(points[0][0])

    distances = []

    for point in points:
        numerator = abs(line[0] * (start[1] - point[1]) - line[1] * (start[0] - point[0]))
        distance = numerator / line_norm
        distances.append(distance)

    best_index = int(np.argmax(distances))
    return int(points[best_index][0])


def save_clustered_csv(rows, labels, output_file):
    fieldnames = ["name", "Longitude", "Latitude", "Cluster"]

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row, label in zip(rows, labels):
            output_row = row.copy()
            output_row["Cluster"] = int(label)
            writer.writerow(output_row)


def save_elbow_chart(k_values, wcss_values, chosen_k, output_file):
    plt.figure(figsize=(7, 5))
    plt.plot(k_values, wcss_values, marker="o")
    plt.axvline(chosen_k, color="red", linestyle="--", label=f"k chon = {chosen_k}")
    plt.xlabel("So cum k")
    plt.ylabel("WCSS")
    plt.title("Elbow Method - Euclid")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=160)
    plt.close()


def save_cluster_chart(X, labels, centroids, rows, output_file):
    plt.figure(figsize=(9, 5.5))
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="tab10", s=45)
    plt.scatter(centroids[:, 0], centroids[:, 1], c="black", marker="x", s=180)

    for row in rows:
        plt.annotate(
            row["name"],
            (row["Longitude"], row["Latitude"]),
            fontsize=7,
            xytext=(3, 3),
            textcoords="offset points",
        )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(f"K-Means Euclid Clustering (k={len(centroids)})")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=160)
    plt.close()


def print_distance_example():
    vietnam = np.array([105.8342, 21.0278])
    japan = np.array([138.2529, 36.2048])
    distance = euclidean_distance(vietnam, japan)

    print("MINH HOA KHOANG CACH EUCLID")
    print("Vietnam = (105.8342, 21.0278)")
    print("Japan   = (138.2529, 36.2048)")
    print("d(Vietnam, Japan) = sqrt((105.8342 - 138.2529)^2 + (21.0278 - 36.2048)^2)")
    print(f"                   = {distance:.4f}")


def print_elbow_results(elbow_results):
    print()
    print("KET QUA KHAO SAT K - ELBOW")
    print(f"{'k':>3} {'WCSS':>12}")

    for k, _, _, wcss in elbow_results:
        print(f"{k:>3} {wcss:>12.2f}")


def print_cluster_summary(rows, centroids, labels):
    print()
    print("TAM CUM")
    print(f"{'Cum':>3} {'Longitude':>12} {'Latitude':>12} {'So nuoc':>8}")

    for cluster_id, centroid in enumerate(centroids):
        count = int(np.sum(labels == cluster_id))
        print(f"{cluster_id:>3} {centroid[0]:>12.4f} {centroid[1]:>12.4f} {count:>8}")

    print()
    print("KET QUA PHAN CUM")
    print(f"{'name':>18} {'Longitude':>12} {'Latitude':>12} {'Cluster':>8}")

    for row, label in zip(rows, labels):
        print(
            f"{row['name']:>18} "
            f"{row['Longitude']:>12.4f} "
            f"{row['Latitude']:>12.4f} "
            f"{int(label):>8}"
        )


def main():
    current_dir = Path(__file__).resolve().parent
    rows, X = load_country_data(DATA_LIST)

    k_values = list(range(1, 11))
    elbow_results = elbow_method(X, k_values)
    wcss_values = [item[3] for item in elbow_results]

    chosen_k = choose_k_by_elbow(elbow_results)
    centroids, labels, wcss = run_kmeans_best_of_n(X, chosen_k)

    elbow_image = current_dir / "cau3_euclid_elbow.png"
    cluster_image = current_dir / "cau3_euclid_clusters.png"
    output_csv = current_dir / "cau3_countries_euclid_clustered.csv"

    save_elbow_chart(k_values, wcss_values, chosen_k, elbow_image)
    save_cluster_chart(X, labels, centroids, rows, cluster_image)
    save_clustered_csv(rows, labels, output_csv)

    print_distance_example()
    print_elbow_results(elbow_results)
    print()
    print(f"K duoc chon theo elbow: {chosen_k}")
    print_cluster_summary(rows, centroids, labels)
    print()
    print(f"Da luu bieu do elbow: {elbow_image}")
    print(f"Da luu bieu do phan cum: {cluster_image}")
    print(f"Da luu ket qua phan cum: {output_csv}")
    print(f"K duoc chon: {chosen_k}, WCSS = {wcss:.2f}")


if __name__ == "__main__":
    main()
