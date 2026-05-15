from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np


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


def elbow_method(X, k_values):
    results = []

    for k in k_values:
        centroids, labels, wcss = run_kmeans_best_of_n(X, k)
        results.append((k, centroids, labels, wcss))

    return results


def find_data_file():
    current_dir = Path(__file__).resolve().parent
    project_dir = current_dir.parents[2]
    candidates = [
        current_dir / "Countries.csv",
        current_dir / "Countries-exercise.csv",
        project_dir / "Countries.csv",
        project_dir / "Countries-exercise.csv",
    ]

    for file_path in candidates:
        if file_path.exists():
            return file_path

    raise FileNotFoundError("Khong tim thay Countries.csv hoac Countries-exercise.csv")


def load_country_data(file_path):
    rows = []

    with open(file_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            row["Longitude"] = float(row["Longitude"])
            row["Latitude"] = float(row["Latitude"])
            rows.append(row)

    X = np.array([[row["Longitude"], row["Latitude"]] for row in rows], dtype=float)
    return rows, X


def save_clustered_csv(rows, labels, output_file):
    fieldnames = list(rows[0].keys())

    if "Cluster" not in fieldnames:
        fieldnames.append("Cluster")

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row, label in zip(rows, labels):
            output_row = row.copy()
            output_row["Cluster"] = int(label)
            writer.writerow(output_row)


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


def save_cluster_chart(X, labels, centroids, output_file):
    plt.figure(figsize=(8, 5))
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="tab10", s=35)
    plt.scatter(centroids[:, 0], centroids[:, 1], c="black", marker="x", s=180)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(f"K-Means Manhattan Clustering (k={len(centroids)})")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=160)
    plt.close()


def print_elbow_results(elbow_results):
    print("KET QUA ELBOW - MANHATTAN")
    print(f"{'k':>3} {'WCSS':>12}")

    for k, _, _, wcss in elbow_results:
        print(f"{k:>3} {wcss:>12.2f}")


def print_cluster_summary(data, centroids, labels):
    print()
    print("TAM CUM")
    print(f"{'Cum':>3} {'Longitude':>12} {'Latitude':>12} {'So nuoc':>8}")

    for cluster_id, centroid in enumerate(centroids):
        count = int(np.sum(labels == cluster_id))
        print(f"{cluster_id:>3} {centroid[0]:>12.4f} {centroid[1]:>12.4f} {count:>8}")

    print()
    print("20 DONG DU LIEU DA PHAN CUM DAU TIEN")
    print(f"{'name':>25} {'Longitude':>12} {'Latitude':>12} {'Cluster':>8}")

    for row, label in zip(data[:20], labels[:20]):
        print(
            f"{row['name']:>25} "
            f"{row['Longitude']:>12.6f} "
            f"{row['Latitude']:>12.6f} "
            f"{int(label):>8}"
        )


def main():
    current_dir = Path(__file__).resolve().parent
    data_file = find_data_file()
    data, X = load_country_data(data_file)

    k_values = list(range(1, 11))
    elbow_results = elbow_method(X, k_values)
    wcss_values = [item[3] for item in elbow_results]

    chosen_k = 3
    centroids, labels, wcss = run_kmeans_best_of_n(X, chosen_k)

    elbow_image = current_dir / "cau3_manhattan_elbow.png"
    cluster_image = current_dir / "cau3_manhattan_clusters.png"
    output_csv = current_dir / "cau3_countries_manhattan_clustered.csv"

    save_elbow_chart(k_values, wcss_values, elbow_image)
    save_cluster_chart(X, labels, centroids, cluster_image)
    save_clustered_csv(data, labels, output_csv)

    print(f"File du lieu: {data_file}")
    print_elbow_results(elbow_results)
    print_cluster_summary(data, centroids, labels)
    print()
    print(f"Da luu bieu do elbow: {elbow_image}")
    print(f"Da luu bieu do phan cum: {cluster_image}")
    print(f"Da luu ket qua phan cum: {output_csv}")
    print(f"K duoc chon: {chosen_k}, WCSS = {wcss:.2f}")


if __name__ == "__main__":
    main()
