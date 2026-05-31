document.addEventListener("DOMContentLoaded", function () {
  const chatBubble = document.getElementById("chat-bubble");
  const chatWidget = document.getElementById("chat-widget");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const chatBody = document.getElementById("chat-body");
  const clearBtn = document.getElementById("clear-btn");
  
  // NÂNG CẤP BƯỚC 3: Đồng bộ chính xác với ID nút cuộn "#scroll-bottom-btn" trong CSS của bạn
  const scrollBottomBtn = document.getElementById("scroll-bottom-btn"); 

  function getCurrentTime() {
      const now = new Date();
      return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
  }

  // 1. Tự động lấy câu chào Menu Chính từ Server
  async function loadInitialMenu() {
      try {
          const response = await fetch("/api/init-menu");
          if (response.ok) {
              const data = await response.json();
              appendMessage(data.response, "bot-message");
          }
      } catch (error) {
          console.error("Lỗi lấy câu chào ban đầu:", error);
      }
  }
  loadInitialMenu();
 
  // 2. Click vào bong bóng tròn để đóng/mở khung chat widget
  if (chatBubble && chatWidget) {
      chatBubble.addEventListener("click", function (e) {
          e.stopPropagation();
          chatWidget.classList.toggle("active");
      });
  }
 
  // 3. Tính năng click nút Thùng rác để Xóa lịch sử chat
  if (clearBtn) {
      clearBtn.addEventListener("click", async function (e) {
          e.stopPropagation();
          if (confirm("Bạn có muốn xóa sạch toàn bộ đoạn hội thoại này không?")) {
              try {
                  const response = await fetch("/api/reset-chat", { method: "POST" });
                  if (response.ok) {
                      chatBody.innerHTML = ''; 
                      const data = await response.json();
                      appendMessage(data.response, "bot-message");
                  }
              } catch (error) {
                  chatBody.innerHTML = ''; 
                  loadInitialMenu();
              }
          }
      });
  }
 
  // 4. Hàm gửi tin nhắn nhận dữ liệu STREAM (Đã nâng cấp dấu 3 chấm động)
  async function sendMessage() {
      const messageText = userInput.value.trim();
      if (!messageText) return;
 
      appendMessage(messageText, "user-message");
      userInput.value = ""; 
 
      // NÂNG CẤP: Thay đổi "..." tĩnh bằng cấu trúc HTML 3 chấm động (.typing-dots) nhấp nháy, bật cờ isHTML = true
      const placeholderBubble = appendMessage(
          `<div class="typing-dots"><span></span><span></span><span></span></div>`, 
          "bot-message",
          true
      );
 
      try {
          const response = await fetch("/api/chat-stream", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ message: messageText })
          });
 
          if (response.ok) {
              const contentSpan = placeholderBubble.querySelector(".message-content");
              contentSpan.innerHTML = ""; // Xóa hiệu ứng 3 chấm khi AI bắt đầu trả chữ ra
              
              const reader = response.body.getReader();
              const decoder = new TextDecoder('utf-8');
              let fullResponseText = "";
 
              while (true) {
                  const { value, done } = await reader.read();
                  if (done) break;
 
                  const chunk = decoder.decode(value, { stream: true });
                  fullResponseText += chunk;
 
                  if (typeof marked !== "undefined" && typeof marked.parse === "function") {
                      contentSpan.innerHTML = marked.parse(fullResponseText);
                  } else {
                      contentSpan.innerHTML = fullResponseText.replace(/\n/g, "<br>");
                  }
                  chatBody.scrollTop = chatBody.scrollHeight;
              }
          } else {
              placeholderBubble.querySelector(".message-content").innerText = "Lỗi kết nối máy chủ!";
          }
      } catch (error) {
          console.error("Error:", error);
          placeholderBubble.querySelector(".message-content").innerText = "Không thể kết nối chatbot.";
      }
      chatBody.scrollTop = chatBody.scrollHeight;
  }
 
  // 5. Hàm appendMessage nâng cấp (Thêm tham số isHTML để tương thích với cấu trúc hiển thị thời gian và markdown của bạn)
  function appendMessage(text, className, isHTML = false) {
      const messageDiv = document.createElement("div");
      messageDiv.className = `message ${className}`;
      
      const contentWrapper = document.createElement("div");
      contentWrapper.className = "message-wrapper";

      const textSpan = document.createElement("span");
      textSpan.className = "message-content";
      
      // Xử lý thông minh: Nếu truyền hiệu ứng 3 chấm dạng HTML thì render thẳng, ngược lại render văn bản/markdown
      if (isHTML) {
          textSpan.innerHTML = text;
      } else if (className === "bot-message" && typeof marked !== "undefined" && typeof marked.parse === "function") {
          textSpan.innerHTML = marked.parse(text);
      } else {
          textSpan.innerHTML = text.replace(/\n/g, "<br>");
      }
      
      const timeSpan = document.createElement("span");
      timeSpan.className = "timestamp";
      timeSpan.innerText = getCurrentTime();

      contentWrapper.appendChild(textSpan);
      contentWrapper.appendChild(timeSpan);
      messageDiv.appendChild(contentWrapper);
      chatBody.appendChild(messageDiv);
      chatBody.scrollTop = chatBody.scrollHeight;
      return messageDiv;
  }
 
  if (sendBtn) sendBtn.addEventListener("click", sendMessage);
  if (userInput) {
      userInput.addEventListener("keypress", function (e) {
          if (e.key === "Enter") sendMessage();
      });
  }

  // ==========================================================================
  // NÂNG CẤP BƯỚC 3: XỬ LÝ ẨN/HIỆN QUA CLASS `.visible` VÀ CUỘN MƯỢT CHO NÚT ĐỎ
  // ==========================================================================
  if (chatBody && scrollBottomBtn) {
      // Lắng nghe sự kiện lướt chuột trong khung nội dung chatBody
      chatBody.addEventListener("scroll", function () {
          // Tính toán khoảng cách thực tế từ vị trí thanh cuộn hiện tại tới đáy
          const distanceFromBottom = chatBody.scrollHeight - chatBody.scrollTop - chatBody.clientHeight;

          // Nếu lướt ngược lên trên cách đáy hơn 150px -> Thêm class .visible để hiển thị, ngược lại xóa đi
          if (distanceFromBottom > 150) {
              scrollBottomBtn.classList.add("visible");
          } else {
              scrollBottomBtn.classList.remove("visible");
          }
      });

      // Bắt sự kiện khi người dùng click vào nút đỏ -> Cuộn mượt mà xuống dưới cùng
      scrollBottomBtn.addEventListener("click", function (e) {
          e.stopPropagation();
          chatBody.scrollTo({
              top: chatBody.scrollHeight,
              behavior: "smooth"
          });
      });
  }
});