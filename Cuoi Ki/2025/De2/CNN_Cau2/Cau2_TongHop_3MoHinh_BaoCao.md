# Câu 2 - Tổng hợp 3 mô hình học máy

Theo yêu cầu ôn tập của thầy:

```text
Học máy: regression and classification
(perceptron, NN, logistic)
Không sử dụng thư viện ngoài tính toán sẵn, có thể dùng numpy và matplotlib
```

Em đã cài đặt 3 mô hình phân loại hoa Iris:

| Mô hình | Thư mục | Kiến trúc | Accuracy train | Ghi chú |
|---|---|---|---:|---|
| Neural Network | `01_Neural_Network` | `4 -> 8 -> 3` | 97.33% | Mô hình chính, kết quả tốt nhất |
| Softmax Logistic Regression | `02_Softmax_Logistic_Regression` | `4 -> 3` | 94.67% | Logistic đa lớp, dễ giải thích |
| Multiclass Perceptron | `03_Multiclass_Perceptron` | `4 -> 3` | 96.00% | Cập nhật khi dự đoán sai |

## Đối chiếu yêu cầu đề bài

Đề bài yêu cầu viết chương trình phân loại hoa bằng **Logistic Regression kết hợp với lớp Softmax**, đồng thời nêu rõ mô hình phân loại hoạt động như thế nào. Phần trả lời trực tiếp yêu cầu này nằm trong báo cáo:

```text
02_Softmax_Logistic_Regression/Cau2_SoftmaxLogistic_BaoCao.md
```

Mô hình Softmax Logistic Regression trong chương trình có kiến trúc:

```text
4 -> 3
```

Trong đó:

- 4 đầu vào tương ứng 4 đặc trưng của hoa Iris: chiều dài đài hoa, chiều rộng đài hoa, chiều dài cánh hoa, chiều rộng cánh hoa.
- 3 neuron đầu ra tương ứng 3 lớp cần phân loại:
  - neuron 0 phụ trách lớp `Iris-setosa`;
  - neuron 1 phụ trách lớp `Iris-versicolor`;
  - neuron 2 phụ trách lớp `Iris-virginica`.
- Mỗi neuron đầu ra tính một điểm số tuyến tính từ 4 đặc trưng đầu vào.
- Lớp Softmax biến 3 điểm số này thành 3 xác suất có tổng bằng 1.
- Mẫu hoa được gán vào lớp có xác suất lớn nhất.

Công thức tổng quát:

```text
Z = XW + b
y_hat = softmax(Z)
label = argmax(y_hat)
```

Vì bài toán có 3 loài hoa nên không dùng Logistic Regression nhị phân với sigmoid, mà dùng Softmax Logistic Regression để phân loại nhiều lớp.

## Giải thích nhanh các mô hình còn lại

### Neural Network

Mô hình Neural Network trong báo cáo `01_Neural_Network` có kiến trúc:

```text
4 -> 8 -> 3
```

Ý nghĩa:

- 4 neuron đầu vào nhận 4 đặc trưng của hoa.
- 8 neuron tầng ẩn học quan hệ giữa các đặc trưng bằng phép tuyến tính kết hợp hàm ReLU.
- 3 neuron đầu ra tương ứng 3 loài hoa: `Iris-setosa`, `Iris-versicolor`, `Iris-virginica`.
- Softmax biến 3 đầu ra thành xác suất.
- Nhãn dự đoán là lớp có xác suất lớn nhất.

Mô hình này khác Softmax Logistic Regression ở chỗ có thêm tầng ẩn. Vì vậy Neural Network có khả năng học quan hệ phi tuyến tốt hơn.

### Multiclass Perceptron

Mô hình Multiclass Perceptron trong báo cáo `03_Multiclass_Perceptron` có kiến trúc:

```text
4 -> 3
```

Ý nghĩa:

- 4 đầu vào nhận 4 đặc trưng của hoa.
- 3 đầu ra tính 3 điểm số cho 3 loài hoa.
- Đầu ra 0 phụ trách `Iris-setosa`.
- Đầu ra 1 phụ trách `Iris-versicolor`.
- Đầu ra 2 phụ trách `Iris-virginica`.
- Mô hình chọn lớp có điểm số lớn nhất bằng `argmax`.
- Khi dự đoán sai, trọng số của lớp đúng được tăng lên, trọng số của lớp dự đoán sai bị giảm xuống.

Mô hình này không dùng Softmax để huấn luyện như Logistic Regression. Softmax trong file Perceptron chỉ dùng để quy đổi điểm số thành dạng confidence dễ xem khi lưu kết quả.

## Cấu trúc thư mục

```text
CNN_Cau2/
├── input_2.csv
├── output_2.csv
├── 01_Neural_Network/
│   ├── cau2_neural_network.py
│   ├── Cau2_NeuralNetwork_BaoCao.md
│   ├── nn_predictions.csv
│   ├── nn_loss.png
│   ├── nn_confusion_matrix.png
│   └── nn_feature_scatter.png
├── 02_Softmax_Logistic_Regression/
│   ├── cau2_softmax_logistic.py
│   ├── Cau2_SoftmaxLogistic_BaoCao.md
│   ├── softmax_predictions.csv
│   ├── softmax_loss.png
│   ├── softmax_confusion_matrix.png
│   └── softmax_feature_scatter.png
└── 03_Multiclass_Perceptron/
    ├── cau2_multiclass_perceptron.py
    ├── Cau2_Perceptron_BaoCao.md
    ├── perceptron_predictions.csv
    ├── perceptron_mistakes.png
    ├── perceptron_confusion_matrix.png
    └── perceptron_feature_scatter.png
```

## Lệnh chạy

Neural Network:

```powershell
python "2025/De2/CNN_Cau2/01_Neural_Network/cau2_neural_network.py"
```

Softmax Logistic Regression:

```powershell
python "2025/De2/CNN_Cau2/02_Softmax_Logistic_Regression/cau2_softmax_logistic.py"
```

Multiclass Perceptron:

```powershell
python "2025/De2/CNN_Cau2/03_Multiclass_Perceptron/cau2_multiclass_perceptron.py"
```

## Nhận xét

Neural Network cho kết quả tốt nhất vì có tầng ẩn để học quan hệ phi tuyến giữa các đặc trưng. Softmax Logistic Regression đơn giản và dễ giải thích, nhưng vì là mô hình tuyến tính nên kết quả thấp hơn. Multiclass Perceptron cũng là mô hình tuyến tính, nhưng luật cập nhật khi dự đoán sai giúp mô hình đạt kết quả khá tốt trên dữ liệu Iris.

Nếu cần chọn một mô hình để trình bày chính trong bài nộp, em chọn:

```text
Neural Network tự cài đặt bằng NumPy
```

Lý do:

- Nằm đúng nhóm `NN` mà thầy yêu cầu.
- Không dùng thư viện học máy có sẵn.
- Có loss, gradient descent, forward propagation, backward propagation.
- Có biểu đồ loss, confusion matrix và biểu đồ phân bố dữ liệu.
- Có accuracy cao nhất trong 3 mô hình.
