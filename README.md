# RadarGUI – Realtime Radar Visualization & Simulator

## 1. Giới thiệu

**RadarGUI** là ứng dụng hiển thị radar thời gian thực, hỗ trợ cả **radar giả lập (Simulator)** và **radar thật qua UART**.  
Ứng dụng được thiết kế để chạy ổn định trên:

- **PC (Windows / Linux)** với PyQt6  
- **Raspberry Pi 4** với PyQt5  
  → *không cần viết lại code, không cần Qt6 trên Pi*

Dự án tập trung vào:
- Kiến trúc realtime nhẹ (soft real-time)
- Tách biệt rõ UI – Model – IO
- Dễ mở rộng cho radar thật (STM32 / MCU)

---

## 2. Kiến trúc tổng thể

┌──────────────┐
│ Simulator    │
│ UART Input   │
└──────┬───────┘
       │ frame (dict)
       ▼
┌──────────────────┐
│ FrameBuffer (1)  │   ← overwrite buffer
└────────┬─────────┘
         ▼
┌──────────────────┐
│ RadarModel       │
│ - update state   │
│ - snapshot       │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ RadarCanvas (UI) │
│ MainWindow       │
└──────────────────┘
Nguyên tắc thiết kế

    Model là ranh giới thread

    UI không đọc dữ liệu trực tiếp từ UART

    Mọi nguồn dữ liệu → frame chuẩn → buffer → model

    Frame cũ bị drop, chỉ hiển thị trạng thái mới nhất (đúng với radar)
3. Tính năng chính
3.1. Radar hiển thị

    Đường quét quay liên tục

    Lưới radar theo range mode

    Hiển thị mục tiêu (target)

    Marker tương tác bằng chuột

    Auto-scale & hysteresis

3.2. Simulator

    Thêm / xóa mục tiêu

    Điều chỉnh:

        góc

        cự ly

        tốc độ

        hướng bay

    Điều khiển:

        START / STOP

        TX ON / OFF (toggle)

        Sweep angle

        Sweep speed (0–16 deg/s)

        Reset simulator về trạng thái ban đầu

3.3. Tín hiệu thật (UART)

    Đọc UART bất đồng bộ

    Parse frame nhị phân

    Ghi vào buffer giống simulator

    Không ảnh hưởng UI

4. Chuẩn dữ liệu Frame (Frame Contract)

Model nhận frame chuẩn dạng Python dict:
frame = {
    "angle": float,        # góc quét hiện tại (deg)
    "speed": float,        # tốc độ quét (deg/s)
    "range_mode": int,     # mode tầm xa
    "ranges": list[float],# danh sách mục tiêu (km)
    "power": list[float], # cường độ (optional)
    "status": {
        "tx_on": bool
    }
}
Simulator và UART phải tạo frame đúng cấu trúc này.