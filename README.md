# 🌸 VJU InfoBot — Hybrid Web Chatbot Engine (Version 2)

<p align="center">
  <a href="https://github.com/NTN000/VJU-InfoBot-ver2">
    <img src="https://img.shields.io/badge/Architecture-Hybrid%20%28Rule--Based%20%2B%20LLM%29-EF4444?style=for-the-badge&logo=cpu" alt="Architecture">
    <img src="https://img.shields.io/badge/Backend-Python%20%7C%20FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="Backend">
    <img src="https://img.shields.io/badge/AI%20Core-Ollama%20%2F%20Sailor2%3A1b-F97316?style=for-the-badge&logo=ollama&logoColor=white" alt="AI Core">
    <img src="https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge" alt="License">
  </a>
</p>

---

## 📝 Tổng Quan Dự Án (Executive Summary)

**VJU InfoBot (Version 2)** là giải pháp Web Chatbot thông minh ứng dụng kiến trúc lai (**Hybrid Routing Architecture**), được phát triển nhằm tự động hóa quy trình tư vấn thông tin tuyển sinh, chương trình đào tạo, lộ trình học phí và chính sách học bổng tại **Trường Đại học Việt Nhật (VJU) - ĐHQGHN**. 

Dự án giải quyết triệt để bài toán tối ưu hóa hiệu năng phần cứng bằng cách phân tách luồng xử lý: các kịch bản tra cứu cố định được đảm bảo độ chính xác $100\%$ và tốc độ phản hồi tức thì qua lõi dữ liệu cấu trúc tích hợp máy trạng thái, trong khi các truy vấn ngôn ngữ tự nhiên tự do được định tuyến sang mô hình trí tuệ nhân tạo tạo sinh (**Generative AI LLM**) chạy hoàn toàn ngoại tuyến (**Offline/Local**).

---

## 📌 Mục Lục (Table of Contents)
- [🌸 VJU InfoBot — Hybrid Web Chatbot Engine (Version 2)](#-vju-infobot--hybrid-web-chatbot-engine-version-2)
  - [📝 Tổng Quan Dự Án (Executive Summary)](#-tổng-quan-dự-án-executive-summary)
  - [📌 Mục Lục (Table of Contents)](#-mục-lục-table-of-contents)
  - [👤 Thông Tin Nhân Sự (Contributor)](#-thông-tin-nhân-sự-contributor)
  - [🏗️ Kiến Trúc Hệ Thống \& Tư Duy Thiết Kế (System Architecture)](#️-kiến-trúc-hệ-thống--tư-duy-thiết-kế-system-architecture)
    - [1. Client-Side (Ứng dụng Web hướng trải nghiệm)](#1-client-side-ứng-dụng-web-hướng-trải-nghiệm)
    - [2. Server-Side (Luồng xử lý Định tuyến Kép)](#2-server-side-luồng-xử-lý-định-tuyến-kép)
  - [📂 Cấu Trúc Thư Mục Dự Án (Directory Structure)](#-cấu-trúc-thư-mục-dự-án-directory-structure)
  - [📊 Sơ Đồ Lớp Kỹ Thuật (System Class Diagram)](#-sơ-đồ-lớp-kỹ-thuật-system-class-diagram)
  - [🚀 Hướng Dẫn Triển Khai (Deployment Guide)](#-hướng-dẫn-triển-khai-deployment-guide)
    - [1. Điều kiện tiên quyết (Prerequisites)](#1-điều-kiện-tiên-quyết-prerequisites)
    - [2. Các bước thiết lập môi trường cục bộ](#2-các-bước-thiết-lập-môi-trường-cục-bộ)
  - [🤝 Quy Trình Đóng Góp Code (Contributing Workflow)](#-quy-trình-đóng-góp-code-contributing-workflow)
  - [📄 Giấy Phép (License)](#-giấy-phép-license)

---

## 👤 Thông Tin Nhân Sự (Contributor)

* **Sinh viên thực hiện:** Nguyễn Triều Nguyên
* **Mã số sinh viên (MSV):** 25112092 (GitHub: [@NTN000](https://github.com/NTN000))
* **Học phần nghiên cứu:** Lập trình hướng đối tượng (OOP)
* **Tổ chức:** Trường Đại học Việt Nhật - ĐHQGHN (VJU)

---

## 🏗️ Kiến Trúc Hệ Thống & Tư Duy Thiết Kế (System Architecture)

Hệ thống được module hóa nghiêm ngặt dựa trên tư duy lập trình hướng đối tượng (OOP) kết hợp kiến trúc hướng dịch vụ nhẹ, đảm bảo tính đóng gói (`Encapsulation`) và khả năng mở rộng dữ liệu linh hoạt:

### 1. Client-Side (Ứng dụng Web hướng trải nghiệm)
* **Asynchronous Data Streaming:** Sử dụng API `fetch` kết hợp cơ chế đọc luồng dữ liệu thô bất đồng bộ (`ReadableStream`), cho phép hiển thị câu trả lời từ LLM dưới dạng cuộn chữ thời gian thực (Stream text), mang lại trải nghiệm mượt mà giống như các sản phẩm AI thương mại lớn.
* **UI/UX Resiliency:** Tích hợp trạng thái chờ trực quan thông qua hiệu ứng hoạt họa ba chấm động (`.typing-dots`). Hệ thống giải phóng bộ giải mã Markdown (`marked.min.js`) để hiển thị định dạng văn bản một cách tối ưu ngay khi nhận được dữ liệu từ Server.
* **Smart Auto-scrolling:** Thiết kế thuật toán tính toán tự động cao độ vùng chat (`chat-body`), tự động cuộn xuống đáy khi có tin nhắn mới hoặc hiển thị nút điều hướng nhanh (`#scroll-bottom-btn`) dựa trên hành vi cuộn chuột của người dùng.

### 2. Server-Side (Luồng xử lý Định tuyến Kép)
* **Rule-based Processing Layer (`VJUKnowledgeBase`):** Khi nhận yêu cầu đầu vào, hệ thống ưu tiên định tuyến qua bộ kiểm tra menu số cố định kế thừa logic từ lõi dữ liệu gốc. Lớp này quản lý các trạng thái phức tạp thông qua cấu hình Máy trạng thái hữu hạn (**Finite State Machine**), đảm bảo độ chính xác $100\%$ đối với thông tin chính thống về ngành học, học phí, phương thức xét tuyển, hotline liên hệ.
* **Generative AI Layer (`OllamaAI_Engine`):** Nếu đầu vào là ngôn ngữ tự nhiên tự do nằm ngoài danh mục tĩnh (ví dụ: chào hỏi, hỏi kiến thức xã hội), yêu cầu sẽ được chuyển đổi thành chuỗi Prompt kỹ thuật cao (Prompt Engineering), sau đó chuyển tiếp tới mô hình **Sailor2:1b** đang chạy offline thông qua **Ollama Service Client** nhằm phân tích ngữ cảnh và phản hồi cá nhân hóa.

---

## 📂 Cấu Trúc Thư Mục Dự Án (Directory Structure)

```text
VJU-InfoBot-ver2-main/
├── ACTIVE/
│   ├── app.py               # Backend Gateway (Quản lý Endpoints API, Hybrid Router & Stream AI với FastAPI)
│   ├── index.html           # Frontend Web UI (Cấu trúc DOM & Layout giao diện bong bóng chat)
│   ├── script.js            # Frontend Web Engine (Xử lý Stream JS, DOM Manipulation & API Integration)
│   └── style.css            # Định dạng giao diện (Responsive Style, Animations & Bộ nhận diện thương hiệu)
├── ca.jpg                   # Tài nguyên đồ họa - Hình ảnh nền hoa anh đào chủ đạo giao diện ứng dụng
└── logo-vju-red.png         # Tài nguyên thương hiệu - Logo VJU chìm (Watermark) nền hộp chat
