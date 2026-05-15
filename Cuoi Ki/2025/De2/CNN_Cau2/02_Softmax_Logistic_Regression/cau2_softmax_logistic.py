from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np


CLASS_NAMES = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]


def read_training_data(file_path):
    X = []
    y_text = []

    with open(file_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)

        for row in reader:
            X.append([float(value) for value in row[:4]])
            y_text.append(row[4])

    label_to_id = {label: index for index, label in enumerate(CLASS_NAMES)}
    y = np.array([label_to_id[label] for label in y_text], dtype=int)
    return np.array(X, dtype=float), y


def read_output_data(file_path):
    X = []

    with open(file_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)

        for row in reader:
            X.append([float(value) for value in row[:4]])

    return np.array(X, dtype=float)


def one_hot_encode(y, num_classes):
    y_one_hot = np.zeros((len(y), num_classes))
    y_one_hot[np.arange(len(y)), y] = 1
    return y_one_hot


def standardize_train(X):
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    std[std == 0] = 1
    return (X - mean) / std, mean, std


def standardize_apply(X, mean, std):
    return (X - mean) / std


def add_bias_column(X):
    return np.c_[np.ones((X.shape[0], 1)), X]


def softmax(Z):
    shifted = Z - np.max(Z, axis=1, keepdims=True)
    exp_scores = np.exp(shifted)
    return exp_scores / np.sum(exp_scores, axis=1, keepdims=True)


def cross_entropy_loss(y_true_one_hot, y_pred_proba):
    eps = 1e-12
    clipped = np.clip(y_pred_proba, eps, 1 - eps)
    return -np.mean(np.sum(y_true_one_hot * np.log(clipped), axis=1))


def train_softmax_regression(X, y, epochs=5000, learning_rate=0.08):
    X_bias = add_bias_column(X)
    y_one_hot = one_hot_encode(y, len(CLASS_NAMES))
    weights = np.zeros((X_bias.shape[1], len(CLASS_NAMES)))
    history = []

    for epoch in range(1, epochs + 1):
        logits = X_bias @ weights
        probabilities = softmax(logits)
        loss = cross_entropy_loss(y_one_hot, probabilities)
        gradients = X_bias.T @ (probabilities - y_one_hot) / X_bias.shape[0]
        weights -= learning_rate * gradients

        if epoch == 1 or epoch % 500 == 0:
            history.append((epoch, loss))

    return weights, history


def predict(X, weights):
    probabilities = softmax(add_bias_column(X) @ weights)
    label_ids = np.argmax(probabilities, axis=1)
    labels = [CLASS_NAMES[label_id] for label_id in label_ids]
    return label_ids, labels, probabilities


def accuracy_score(y_true, y_pred):
    return np.mean(y_true == y_pred)


def build_confusion_matrix(y_true, y_pred):
    matrix = np.zeros((len(CLASS_NAMES), len(CLASS_NAMES)), dtype=int)

    for true_label, pred_label in zip(y_true, y_pred):
        matrix[true_label, pred_label] += 1

    return matrix


def save_loss_chart(history, output_file):
    epochs = [item[0] for item in history]
    losses = [item[1] for item in history]

    plt.figure(figsize=(7, 5))
    plt.plot(epochs, losses, marker="o", linewidth=2)
    plt.xlabel("Epoch")
    plt.ylabel("Cross-Entropy Loss")
    plt.title("Softmax Regression - Qua trinh giam loss")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=160)
    plt.close()


def save_confusion_matrix_chart(matrix, output_file):
    plt.figure(figsize=(6, 5))
    plt.imshow(matrix, cmap="Blues")
    plt.title("Softmax Regression - Confusion Matrix")
    plt.xlabel("Nhan du doan")
    plt.ylabel("Nhan that")
    plt.xticks(range(len(CLASS_NAMES)), CLASS_NAMES, rotation=25, ha="right")
    plt.yticks(range(len(CLASS_NAMES)), CLASS_NAMES)
    plt.colorbar(label="So mau")

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            color = "white" if matrix[i, j] > np.max(matrix) / 2 else "black"
            plt.text(j, i, str(matrix[i, j]), ha="center", va="center", color=color)

    plt.tight_layout()
    plt.savefig(output_file, dpi=160)
    plt.close()


def save_feature_scatter_chart(X_train, y_train, X_output, output_labels, output_file):
    plt.figure(figsize=(8, 5))
    colors = ["tab:blue", "tab:orange", "tab:green"]

    for label_id, class_name in enumerate(CLASS_NAMES):
        points = X_train[y_train == label_id]
        plt.scatter(points[:, 2], points[:, 3], c=colors[label_id], label=f"Train {class_name}", s=35, alpha=0.75)

    for label_id, class_name in enumerate(CLASS_NAMES):
        predicted_points = X_output[np.array(output_labels) == class_name]
        plt.scatter(predicted_points[:, 2], predicted_points[:, 3], c=colors[label_id], marker="x", s=90, linewidths=2, label=f"Output {class_name}")

    plt.xlabel("Chieu dai canh hoa")
    plt.ylabel("Chieu rong canh hoa")
    plt.title("Softmax Regression - Phan bo du lieu")
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=160)
    plt.close()


def save_predictions(output_rows, labels, probabilities, output_file):
    fieldnames = ["sepal_length", "sepal_width", "petal_length", "petal_width", "predicted_label", "probability"]

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row, label, proba in zip(output_rows, labels, probabilities):
            writer.writerow({
                "sepal_length": row[0],
                "sepal_width": row[1],
                "petal_length": row[2],
                "petal_width": row[3],
                "predicted_label": label,
                "probability": f"{np.max(proba):.6f}",
            })


def main():
    current_dir = Path(__file__).resolve().parent
    data_dir = current_dir.parent
    train_file = data_dir / "input_2.csv"
    predict_file = data_dir / "output_2.csv"

    X_train, y_train = read_training_data(train_file)
    X_output = read_output_data(predict_file)
    X_train_scaled, mean, std = standardize_train(X_train)
    X_output_scaled = standardize_apply(X_output, mean, std)

    weights, history = train_softmax_regression(X_train_scaled, y_train)
    train_pred_ids, _, _ = predict(X_train_scaled, weights)
    _, output_labels, output_probabilities = predict(X_output_scaled, weights)
    accuracy = accuracy_score(y_train, train_pred_ids)
    matrix = build_confusion_matrix(y_train, train_pred_ids)

    save_predictions(X_output, output_labels, output_probabilities, current_dir / "softmax_predictions.csv")
    save_loss_chart(history, current_dir / "softmax_loss.png")
    save_confusion_matrix_chart(matrix, current_dir / "softmax_confusion_matrix.png")
    save_feature_scatter_chart(X_train, y_train, X_output, output_labels, current_dir / "softmax_feature_scatter.png")

    print("SOFTMAX LOGISTIC REGRESSION")
    print("Kien truc: 4 -> 3")
    print(f"Loss cuoi: {history[-1][1]:.6f}")
    print(f"Accuracy train: {accuracy * 100:.2f}%")
    print("Nhan du doan 30 mau:")

    for index, (label, proba) in enumerate(zip(output_labels, output_probabilities), start=1):
        print(f"{index:>2}. {label:<16} {np.max(proba):.6f}")


if __name__ == "__main__":
    main()
