
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

- `speaker.yml` gồm các thông tin về sample rate, bit, fftl, shiftms, các thông tin về ngưỡng lấy f0, mcep cũng nhưng công cụ dùng để phân tích

- `pair.yml` gồm các thông tin về jnt, GMM và GV

## Thư mục `data`

Chứa dữ liệu file âm thanh và model

### Thư mục `output`

Chứa các thông tin được tạo trong quá trình train

### Thư mục `wav`

Gồm các thư mục, mỗi thư mục có chứa các file ghi âm của 1 người nói

## Thư mục `list`

Chưa file text chứa tên các file được dùng để train và test

## Thư mục `src`

Mã chính của của project gồm các file:

### file `extract_features.py`

Sử dụng class FeatureExtractor có được cung cấp trong thư viện sprocket trích xuất một số loại tính năng âm thanh như F0, định kỳ, phong bì phổ, từ file wav đầu vào sau đó tổng hợp giọng nói bằng class Synthesizer với đặc trưng vừa được trích xuất.

### file `estimate_feature_statistics.py`

- F0statistics: uớc tính số liệu thống kê F0 từ danh sách các f0
- GV: Ước tính số liệu thống kê và thực hiện postfilter dựa trên phương sai toàn cục (GV) từ tập dữ liệu đầu vào

### file `estimate_twf_and_jnt.py`

- Căn chỉnh mcep w / o 0-th và im lặng
- Căn chỉnh codeap bằng cách sử dụng twf đã cho

### file `train_GMM.py`

Huấn luyện mô hình dựa trên các thông tin đã được trích xuất

### file `convert.py`

Nhận file âm thanh đầu vào và chuyển đổi bằng cách sử dụng mô hình đã huấn luyện

### file `misc.py`

Chứa các hàm hỗ trợ được sử dụng trong các file trên

### file `yml.py`

Chứa các hàm hỗ trợ đọc các file cấu hình

## file `initialize.py`

Khởi tạo các file chứa danh sách các file âm thanh phục vụ quá trình huấn luyện và kiểm tra và lưu chúng trong thư mục list

## file `train_and_convert.py`

Gọi tuần tự các hàm trích xuất đặc trưng, huấn luyện và cuối cùng là chuyển đổi các file âm thanh được xác định nhằm mục đích test
