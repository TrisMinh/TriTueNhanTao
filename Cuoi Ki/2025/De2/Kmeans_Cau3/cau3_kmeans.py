from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def euclidean_distance(point_a, point_b):
    return np.sqrt(np.sum((point_a - point_b) ** 2))


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
    data = pd.read_csv(file_path)
    X = data[["Longitude", "Latitude"]].values
    return data, X


def save_elbow_chart(k_values, wcss_values, output_file):
    plt.figure(figsize=(7, 5))
    plt.plot(k_values, wcss_values, marker="o")
    plt.xlabel("So cum k")
    plt.ylabel("WCSS")
    plt.title("Elbow Method")
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
    plt.title(f"K-Means Clustering (k={len(centroids)})")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=160)
    plt.close()


def print_elbow_results(elbow_results):
    print("KET QUA ELBOW")
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
    print(data[["name", "Longitude", "Latitude", "Cluster"]].head(20).to_string(index=False))


def main():
    current_dir = Path(__file__).resolve().parent
    data_file = find_data_file()
    data, X = load_country_data(data_file)

    k_values = list(range(1, 11))
    elbow_results = elbow_method(X, k_values)
    wcss_values = [item[3] for item in elbow_results]

    chosen_k = 5
    centroids, labels, wcss = run_kmeans_best_of_n(X, chosen_k)
    data["Cluster"] = labels

    elbow_image = current_dir / "cau3_elbow.png"
    cluster_image = current_dir / "cau3_clusters.png"
    output_csv = current_dir / "cau3_countries_clustered.csv"

    save_elbow_chart(k_values, wcss_values, elbow_image)
    save_cluster_chart(X, labels, centroids, cluster_image)
    data.to_csv(output_csv, index=False)

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
