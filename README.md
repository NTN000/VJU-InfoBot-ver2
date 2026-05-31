# 🌸 VJU InfoBot — Hybrid Web Chatbot Engine (Version 2)

---

## 📝 Tổng Quan Dự Án (Executive Summary)

**VJU InfoBot (Version 2)** là giải pháp Web Chatbot thông minh ứng dụng kiến trúc lai (**Hybrid Routing Architecture**), được phát triển nhằm tự động hóa quy trình tư vấn thông tin tuyển sinh, chương trình đào tạo, lộ trình học phí và chính sách học bổng tại **Trường Đại học Việt Nhật (VJU) - ĐHQGHN**.

Dự án giải quyết triệt để bài toán tối ưu hóa hiệu năng phần cứng bằng cách phân tách luồng xử lý: các kịch bản tra cứu cố định được đảm bảo độ chính xác 100% và tốc độ phản hồi tức thì qua lõi dữ liệu cấu trúc tích hợp máy trạng thái, trong khi các truy vấn ngôn ngữ tự nhiên tự do được định tuyến sang mô hình trí tuệ nhân tạo tạo sinh (**Generative AI LLM**) chạy hoàn toàn ngoại tuyến (**Offline/Local**).

---

## 📌 Mục Lục (Table of Contents)

* [📝 Tổng Quan Dự Án (Executive Summary)](#-tổng-quan-dự-án-executive-summary)
* [👤 Thông Tin Nhân Sự (Contributor)](#-thông-tin-nhân-sự-contributor)
* [🏗️ Kiến Trúc Hệ Thống & Tư Duy Thiết Kế (System Architecture)](#️-kiến-trúc-hệ-thống--tư-duy-thiết-kế-system-architecture)
* [📂 Cấu Trúc Thư Mục Dự Án (Directory Structure)](#-cấu-trúc-thư-mục-dự-án-directory-structure)
* [📊 Sơ Đồ Lớp Kỹ Thuật (System Class Diagram)](#-sơ-đồ-lớp-kỹ-thuật-system-class-diagram)
* [🚀 Hướng Dẫn Triển Khai Nhanh (Quick Deployment)](#-hướng-dẫn-triển-khai-nhanh-quick-deployment)

---

## 👤 Thông Tin Nhân Sự (Contributor)

* **Sinh viên thực hiện:** Nguyễn Triều Nguyên
* **Mã số sinh viên (MSV):** 25112092 (GitHub: [@NTN000](https://github.com/NTN000))
* **Học phần nghiên cứu:** Lập trình hướng đối tượng (OOP)
* **Tổ chức:** Trường Đại học Việt Nhật - ĐHQGHN (VJU)

---

## 🏗️ Kiến Trúc Hệ Thống & Tư Duy Thiết Kế (System Architecture)

Hệ thống được module hóa nghiêm ngặt dựa trên tư duy lập trình hướng đối tượng (OOP) kết hợp kiến trúc hướng dịch vụ nhẹ, đảm bảo tính đóng gói (*Encapsulation*) và khả năng mở rộng dữ liệu linh hoạt:

### 1. Client-Side (Ứng dụng Web hướng trải nghiệm)
* **Asynchronous Data Streaming:** Sử dụng API `fetch` kết hợp cơ chế đọc luồng dữ liệu thô bất đồng bộ (`ReadableStream`), cho phép hiển thị câu trả lời từ LLM dưới dạng cuộn chữ thời gian thực (*Stream text*), mang lại trải nghiệm mượt mà giống như các sản phẩm AI thương mại lớn.
* **UI/UX Resiliency:** Tích hợp trạng thái chờ trực quan thông qua hiệu ứng hoạt họa ba chấm động (`.typing-dots`). Hệ thống giải phóng bộ giải mã Markdown (`marked.min.js`) để hiển thị định dạng văn bản một cách tối ưu ngay khi nhận được dữ liệu từ Server.
* **Smart Auto-scrolling:** Thiết kế thuật toán tính toán tự động cao độ vùng chat (`chat-body`), tự động cuộn xuống đáy khi có tin nhắn mới hoặc hiển thị nút điều hướng nhanh (`#scroll-bottom-btn`) dựa trên hành vi cuộn chuột của người dùng.

### 2. Server-Side (Luồng xử lý Định tuyến Kép)
* **Rule-based Processing Layer (VJUKnowledgeBase):** Khi nhận yêu cầu đầu vào, hệ thống ưu tiên định tuyến qua bộ kiểm tra menu số cố định kế thừa logic từ lõi dữ liệu gốc. Lớp này quản lý các trạng thái phức tạp thông qua cấu hình Máy trạng thái hữu hạn (*Finite State Machine*), đảm bảo độ chính xác 100% đối với thông tin chính thống về ngành học, học phí, phương thức xét tuyển, hotline liên hệ.
* **Generative AI Layer (OllamaAI_Engine):** Nếu đầu vào là ngôn ngữ tự nhiên tự do nằm ngoài danh mục tĩnh (ví dụ: chào hỏi, hỏi kiến thức xã hội), yêu cầu sẽ được chuyển đổi thành chuỗi Prompt kỹ thuật cao (*Prompt Engineering*), sau đó chuyển tiếp tới mô hình **Sailor2:1b** đang chạy offline thông qua *Ollama Service Client* nhằm phân tích ngữ cảnh và phản hồi cá nhân hóa.

---

## 📂 Cấu Trúc Thư Mục Dự Án (Directory Structure)

```text
VJU-InfoBot-ver2-main/
├── ACTIVE/
│   ├── app.py               # Backend Gateway (FastAPI)
│   ├── index.html           # Frontend Web UI
│   ├── script.js            # Frontend Web Engine
│   └── style.css            # Định dạng giao diện 
├── ca.jpg                   # Hình ảnh nền hoa anh đào
└── logo-vju-red.png         # Logo VJU chìm nền hộp chat
'''
📊 Sơ Đồ Lớp Kỹ Thuật (System Class Diagram)

<img width="2165" height="1684" alt="mermaid-diagram-2026-05-31-235611" src="https://github.com/user-attachments/assets/c9930216-bda2-4f02-bda9-f9921dbcd428" />


🚀 Hướng Dẫn Triển Khai Nhanh (Quick Deployment)
Đảm bảo máy đã cài Python >= 3.10 và Ollama (đã chạy lệnh ollama run sailor2:1b), sau đó mở Terminal tại thư mục dự án và thực hiện chuỗi lệnh sau để cài đặt thư viện, khởi chạy máy chủ và truy cập giao diện Chatbot trên trình duyệt:

Bash
cd VJU-InfoBot-ver2/ACTIVE && pip install fastapi uvicorn httpx pydantic && python app.py
# Sau khi khởi chạy thành công, mở trình duyệt và truy cập: http://127.0.0.1:5000

🤝 Quy Trình Đóng Góp Code (Contributing Workflow)
Đẩy nhánh tính năng lên kho chứa cá nhân: git push origin feature/AmazingFeature

Mở một yêu cầu kiểm tra và tích hợp mã nguồn (Pull Request).
