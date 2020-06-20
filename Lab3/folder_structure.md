
# Cấu trúc thư mục

```bash
|   initialize.py
|   train_and_convert.py
|
+---conf
|       pair.yml
|       speaker.yml
|
+---data
|   |   .gitkeep
|   |
|   +---output
|   |   +---anasyn
|   |   +---h5
|   |   +---jnt
|   |   +---model
|   |   +---stats
|   |   +---test
|   |   \---twf
|   \---wav
+---list
|       .gitkeep
|
+---sprocket
|
\---src
        convert.py
        estimate_feature_statistics.py
        estimate_twf_and_jnt.py
        extract_features.py
        misc.py
        train_GMM.py
        yml.py
        __init__.py
```

# Mô tả các phần

## Thư mục `conf`

Chứa các config được sử dụng bao gồm các file:

- `speaker.yml` gồm các thông tin như sau:
  - mục wav: lưu thông tin sử dụng để xử lý file âm thanh, bao gồm:
    - fs: sample rate
    - bit: số bit
    - fftl: độ dài của FFT
    - shiftms: độ dài của từng đoạn
  - mục f0: lưu các thông tin sử dụng để trích xuất đặc trưng
    - minf0: giá trị ngưỡng dưới
    - maxf0: giá trị ngưỡng trên
  - mcep:
    - dim: Kích thước của chuỗi mel-cepstrum
    - alpha: Tham số của bộ lọc tất cả các phần để chuyển đổi tần số
  - power: Giá trị của ngưỡng công suất
    - threshold: Giá trị ngưỡng
- `pair.yml` gồm các thông tin như sau:
  - jnt: Vectơ đặc trưng chung của vectơ đặc trưng ban đầu và đích bao gồm các thành phần tĩnh và delta
    - n_iter: số lần lặp
  - GMM:
    - mcep: thông tin xử lý trình tự Mel-cepstrum
      - n_mix: Số lượng thành phần hỗn hợp của GMM
      - n_iter: Số lần lặp cho thuật toán EM
      - covtype: Loại ma trận hiệp phương sai của GMM
      - cvtype: Loại kỹ thuật chuyển đổi
    - codeap: thông tin mã hóa một chuỗi chu kỳ của dạng sóng
      - n_mix: Số lượng thành phần hỗn hợp của GMM
      - n_iter: Số lần lặp cho thuật toán EM
      - covtype: Loại ma trận hiệp phương sai của GMM
      - cvtype: Loại kỹ thuật chuyển đổi
  - GV: thông tin thống kê phương sai toàn cục (GV)
    - morph_coeff: Hệ số biến đổi giữa dữ liệu và dữ liệu biến đổi GV

## Thư mục `data`

Chứa dữ liệu file âm thanh và model.

### Thư mục `output`

Chứa các thông tin được tạo trong quá trình train.

### Thư mục `wav`

Gồm các thư mục, mỗi thư mục có chứa các file ghi âm của 1 người nói.

## Thư mục `list`

Chưa file text chứa tên các file được dùng để train và test.

## Thư mục `src`

Mã chính của của project gồm các file:

### File `extract_features.py`

Sử dụng class FeatureExtractor có được cung cấp trong thư viện sprocket trong đó WORLD thông qua gói pyword được sử dụng để trích xuất tham số giọng nói và tổng hợp bộ phát âm. Các đặc trưng âm thanh như F0, mel-cepstrum và một chu kỳ đều bị loại bỏ. Các tính năng âm thanh này được lưu trữ dưới dạng tệp trong định dạng tệp HDF5 cho mỗi cách phát âm.

### File `estimate_feature_statistics.py`

- F0statistics: uớc tính số liệu thống kê F0 từ danh sách các f0
- GV: Ước tính số liệu thống kê và thực hiện postfilter dựa trên phương sai toàn cục (GV) từ tập dữ liệu đầu vào.
- Trong bước này, các số liệu thống kê phụ thuộc vào người nói như độ lệch trung bình và độ lệch chuẩn của F0 và GV của mel-cepstrum được tính toán.

### File `estimate_twf_and_jnt.py`

- Trong bước này, để xây dựng các vectơ đặc trưng chung cho mô hình GMM, ước tính căn chỉnh được thực hiện bao gồm:
  - Căn chỉnh mcep w / o 0-th và im lặng.
  - Căn chỉnh codeap bằng cách sử dụng twf đã cho.

### File `train_GMM.py`

Huấn luyện mô hình dựa trên các thông tin đã được trích xuất.

### File `convert.py`

Nhận file âm thanh đầu vào và chuyển đổi bằng cách sử dụng mô hình đã huấn luyện.

### File `misc.py`

Chứa các hàm hỗ trợ được sử dụng trong các file trên.

### File `yml.py`

Chứa các hàm hỗ trợ đọc các file cấu hình.

## File `initialize.py`

Khởi tạo các file chứa danh sách các file âm thanh phục vụ quá trình huấn luyện và kiểm tra và lưu chúng trong thư mục list.

## File `train_and_convert.py`

Gọi tuần tự các hàm trích xuất đặc trưng, huấn luyện và cuối cùng là chuyển đổi các file âm thanh được xác định nhằm mục đích test.
