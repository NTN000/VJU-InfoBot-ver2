document.addEventListener("DOMContentLoaded", function () {
  const chatBubble = document.getElementById("chat-bubble");
  const chatWidget = document.getElementById("chat-widget");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const chatBody = document.getElementById("chat-body");
  const clearBtn = document.getElementById("clear-btn");
  

  const scrollBottomBtn = document.getElementById("scroll-bottom-btn"); 

  function getCurrentTime() {
      const now = new Date();
      return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
  }


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
 

  if (chatBubble && chatWidget) {
      chatBubble.addEventListener("click", function (e) {
          e.stopPropagation();
          chatWidget.classList.toggle("active");
      });
  }
 

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
 

  async function sendMessage() {
      const messageText = userInput.value.trim();
      if (!messageText) return;
 
      appendMessage(messageText, "user-message");
      userInput.value = ""; 
 
   
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
              contentSpan.innerHTML = ""; 
              
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
 

  function appendMessage(text, className, isHTML = false) {
      const messageDiv = document.createElement("div");
      messageDiv.className = `message ${className}`;
      
      const contentWrapper = document.createElement("div");
      contentWrapper.className = "message-wrapper";

      const textSpan = document.createElement("span");
      textSpan.className = "message-content";
      
    
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

  
  if (chatBody && scrollBottomBtn) {
      
      chatBody.addEventListener("scroll", function () {
         
          const distanceFromBottom = chatBody.scrollHeight - chatBody.scrollTop - chatBody.clientHeight;


          if (distanceFromBottom > 150) {
              scrollBottomBtn.classList.add("visible");
          } else {
              scrollBottomBtn.classList.remove("visible");
          }
      });

 
      scrollBottomBtn.addEventListener("click", function (e) {
          e.stopPropagation();
          chatBody.scrollTo({
              top: chatBody.scrollHeight,
              behavior: "smooth"
          });
      });
  }
});