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
| Multiclass Perceptron | `03_Multiclass_Perceptron` | `4 -> 3` | 95.56% | Cập nhật khi dự đoán sai |

## Đối chiếu yêu cầu đề bài

Đề bài yêu cầu viết chương trình phân loại hoa bằng **Logistic Regression kết hợp với lớp Softmax**, đồng thời nêu rõ mô hình phân loại hoạt động như thế nào. Phần trả lời trực tiếp yêu cầu này nằm trong báo cáo:

```text
02_Softmax_Logistic_Regression/Cau2_SoftmaxLogistic_BaoCao.md
```

Mô hình Softmax Logistic Regression trong chương trình có kiến trúc:

```text
4 -> 3
```

Hình kiến trúc:

```text
02_Softmax_Logistic_Regression/softmax_architecture_v3.png
```

Trong đó:

- 4 đầu vào tương ứng 4 đặc trưng của hoa Iris: chiều dài đài hoa, chiều rộng đài hoa, chiều dài cánh hoa, chiều rộng cánh hoa.
- 3 neuron đầu ra tương ứng 3 lớp cần phân loại:
  - neuron 0 phụ trách lớp `Iris-setosa`;
  - neuron 1 phụ trách lớp `Iris-versicolor`;
  - neuron 2 phụ trách lớp `Iris-virginica`.
- Mỗi neuron đầu ra tính một điểm số tuyến tính từ 4 đặc trưng đầu vào.
- Softmax là hàm kích hoạt tầng đầu ra, biến 3 điểm số này thành 3 xác suất có tổng bằng 1.
- Cross-Entropy là hàm mất mát, dùng để đo sai lệch giữa xác suất dự đoán và nhãn thật dạng one-hot.
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

Hình kiến trúc:

```text
01_Neural_Network/nn_architecture_v3.png
```

Ý nghĩa:

- 4 neuron đầu vào nhận 4 đặc trưng của hoa.
- 8 neuron tầng ẩn học quan hệ giữa các đặc trưng bằng phép tuyến tính kết hợp hàm kích hoạt ReLU.
- 3 neuron đầu ra tương ứng 3 loài hoa: `Iris-setosa`, `Iris-versicolor`, `Iris-virginica`.
- Softmax là hàm kích hoạt tầng đầu ra, dùng để biến 3 đầu ra thành xác suất.
- Cross-Entropy là hàm mất mát, dùng để đo sai lệch giữa xác suất dự đoán sau Softmax và nhãn thật dạng one-hot.
- Nhãn dự đoán là lớp có xác suất lớn nhất.

Mô hình này khác Softmax Logistic Regression ở chỗ có thêm tầng ẩn. Vì vậy Neural Network có khả năng học quan hệ phi tuyến tốt hơn.

### Multiclass Perceptron

Mô hình Multiclass Perceptron trong báo cáo `03_Multiclass_Perceptron` có kiến trúc:

```text
4 -> 3
```

Hình kiến trúc:

```text
03_Multiclass_Perceptron/perceptron_architecture_v3.png
```

Ý nghĩa:

- 4 đầu vào nhận 4 đặc trưng của hoa.
- 3 đầu ra tính 3 điểm số cho 3 loài hoa.
- Đầu ra 0 phụ trách `Iris-setosa`.
- Đầu ra 1 phụ trách `Iris-versicolor`.
- Đầu ra 2 phụ trách `Iris-virginica`.
- Mô hình chọn lớp có điểm số lớn nhất bằng `argmax`.
- Mô hình không dùng Softmax để chọn lớp và không dùng Cross-Entropy Loss để huấn luyện.
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
│   ├── nn_architecture_v3.png
│   ├── nn_predictions.csv
│   ├── nn_loss.png
│   ├── nn_confusion_matrix.png
│   └── nn_feature_scatter.png
├── 02_Softmax_Logistic_Regression/
│   ├── cau2_softmax_logistic.py
│   ├── Cau2_SoftmaxLogistic_BaoCao.md
│   ├── softmax_architecture_v3.png
│   ├── softmax_predictions.csv
│   ├── softmax_loss.png
│   ├── softmax_confusion_matrix.png
│   └── softmax_feature_scatter.png
└── 03_Multiclass_Perceptron/
    ├── cau2_multiclass_perceptron.py
    ├── Cau2_Perceptron_BaoCao.md
    ├── perceptron_architecture_v3.png
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

---

## Bổ sung: Data augmentation cho bài toán phân loại hoa Iris

Trong phiên bản thư mục `CNN_Cau2 data agument`, em bổ sung bước data augmentation cho tập huấn luyện `input_2.csv`.

Vì dữ liệu Iris không phải ảnh mà là dữ liệu bảng gồm 4 đặc trưng số:

```text
sepal_length, sepal_width, petal_length, petal_width
```

nên không dùng các phép augmentation ảnh như xoay, lật, crop. Thay vào đó, em tạo thêm mẫu huấn luyện bằng cách cộng nhiễu Gaussian nhỏ vào các đặc trưng số của từng lớp hoa.

Quy trình augmentation:

1. Đọc dữ liệu gốc từ `input_2.csv`.
2. Tách dữ liệu theo từng lớp: `Iris-setosa`, `Iris-versicolor`, `Iris-virginica`.
3. Với mỗi lớp, tính độ lệch chuẩn của từng đặc trưng.
4. Sinh thêm 2 bản sao nhiễu cho mỗi mẫu gốc.
5. Nhiễu được lấy theo phân phối Gaussian với biên độ nhỏ:

```text
noise = Normal(0, std_theo_lop * 0.04)
```

6. Sau khi cộng nhiễu, các giá trị đặc trưng được chặn dưới tại `0.01` để tránh giá trị âm.
7. Gộp dữ liệu gốc và dữ liệu sinh thêm thành tập huấn luyện mới.

Số lượng dữ liệu:

```text
Số mẫu gốc: 75
Số mẫu sau augmentation: 225
```

Mỗi mô hình có cấu hình augmentation riêng ngay trong file code của mô hình đó. Các tham số chính gồm:

- `enabled`: bật/tắt augmentation.
- `output_file`: tên file CSV sau augmentation của riêng mô hình.
- `copies_per_sample`: số mẫu nhân tạo sinh thêm cho mỗi mẫu gốc.
- `noise_scale`: biên độ nhiễu Gaussian so với độ lệch chuẩn từng lớp.
- `random_state`: seed để chạy lại ra cùng dữ liệu augmentation.
- `clip_min`: giá trị nhỏ nhất cho đặc trưng sau khi cộng nhiễu, tránh số âm.

File dữ liệu sau augmentation được lưu riêng theo từng mô hình:

```text
01_Neural_Network/nn_input_2_augmented.csv
02_Softmax_Logistic_Regression/softmax_input_2_augmented.csv
03_Multiclass_Perceptron/perceptron_input_2_augmented.csv
```

Ba mô hình trong thư mục này đều được train lại bằng dữ liệu sau augmentation:

| Mô hình | File code | Accuracy train sau augmentation |
|---|---|---:|
| Neural Network | `01_Neural_Network/cau2_neural_network.py` | 97.33% |
| Softmax Logistic Regression | `02_Softmax_Logistic_Regression/cau2_softmax_logistic.py` | 94.67% |
| Multiclass Perceptron | `03_Multiclass_Perceptron/cau2_multiclass_perceptron.py` | 95.56% |

Lưu ý: data augmentation chỉ áp dụng cho tập huấn luyện. Tập `output_2.csv` vẫn giữ nguyên để dự đoán, không tạo thêm mẫu dự đoán.

Các file dự đoán sau khi train bằng dữ liệu augmentation vẫn được lưu theo từng mô hình:

```text
01_Neural_Network/nn_predictions.csv
02_Softmax_Logistic_Regression/softmax_predictions.csv
03_Multiclass_Perceptron/perceptron_predictions.csv
```
