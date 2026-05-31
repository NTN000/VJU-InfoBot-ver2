import os
import json
import logging
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
import httpx
import uvicorn  

app = FastAPI()


OLLAMA_URL = "http://localhost:11434/api/chat"  
MODEL_NAME = "sailor2:1b"  


ai_chat_history = []  


MENU_1_TUYEN_SINH = (
    "Năm 2026, Trường Đại học Việt Nhật (VJU) - ĐHQGHN tuyển 800 chỉ tiêu cho 9 chương trình đào tạo "
    "(gồm các ngành kỹ thuật, công nghệ và khoa học xã hội). Trường áp dụng 06 phương thức xét tuyển, "
    "chủ yếu thực hiện tại cơ sở Hòa Lạc và Mỹ Đình.\n"
    "Các thông tin tuyển sinh chi tiết bao gồm:\n\n"
    "📌 Các Ngành Đào Tạo\n"
    "- Nhật Bản học\n"
    "- Đổi mới và phát triển toàn cầu\n"
    "- Công nghệ kỹ thuật Chip bán dẫn\n"
    "- Khoa học và Kỹ thuật máy tính\n"
    "- Kỹ thuật cơ điện tử\n"
    "- Điều khiển thông minh và tự động hóa\n"
    "- Nông nghiệp thông minh và bền vững\n"
    "- Kỹ thuật Xây dựng\n"
    "- Công nghệ thực phẩm và sức khỏe\n\n"
    "📌 Phương thức xét tuyển (06 phương thức)\n"
    "1. Xét tuyển thẳng và ưu tiên xét tuyển theo quy chế của Bộ GD&ĐT.\n"
    "2. Xét tuyển dựa trên kết quả thi tốt nghiệp THPT năm 2026.\n"
    "3. Xét tuyển kết quả thi Đánh giá năng lực (HSA) của ĐHQGHN.\n"
    "4. Xét tuyển dựa trên chứng chỉ ngoại ngữ kết hợp điểm thi tốt nghiệp THPT.\n"
    "5. Xét tuyển bằng điểm kỳ thi chuẩn hóa SAT (Mỹ).\n"
    "6. Xét tuyển thông qua đánh giá hồ sơ và phỏng vấn.\n\n"
    "🔙 Bấm phím '0' để QUAY LẠI Màn hình chính"
)

MENU_2_NGANH_HOC = (
    "Thông tin: Trường Đại học Việt Nhật (VJU) - ĐHQGHN hiện đang đào tạo các ngành đại học chính quy bao gồm:\n\n"
    "1. Công nghệ kỹ thuật Chip bán dẫn\n"
    "2. Khoa học và Kỹ thuật máy tính\n"
    "3. Nhật Bản học\n"
    "4. Đổi mới và phát triển toàn cầu\n"
    "5. Nông nghiệp thông minh và bền vững\n"
    "6. Kỹ thuật Xây dựng\n"
    "7. Điều khiển thông minh và tự động hóa\n\n"
    "🏠 Bấm '0' để Quay lại Màn hình chính (Main Menu)\n\n"
    "Nhập lựa chọn (1-7 hoặc 0):"
)
NGANH_DETAILS = {
    "1": (
        "🔍 CHI TIẾT: CÔNG NGHỆ KỸ THUẬT CHIP BÁN DẪN (Mới)\n\n"
        "📋 Thông tin chung:\n"
        "- Mã ngành: 7510301\n"
        "- Thời gian đào tạo: 4.5 năm (Hệ Kỹ sư Chất lượng cao)\n"
        "- Khối xét tuyển: A00, A01, D01\n"
        "- Học phí: 58.000.000 VNĐ/năm\n\n"
        "💡 Đặc điểm nổi bật:\n"
        "- Chương trình phối hợp với các Đại học lớn tại Nhật Bản (ĐH Tokyo, ĐH Osaka).\n"
        "- Thực hành tại các phòng Lab chuẩn quốc tế về thiết kế vi mạch (IC Design).\n\n"
        "💼 Cơ hội nghề nghiệp:\n"
        "- Kỹ sư thiết kế vi mạch phần cứng, kỹ sư sản xuất Chip bán dẫn tại Intel, Samsung, Synopsys...\n"
        "----------------------------------------\n"
        "↩️ Bấm 'C' để quay lại danh sách ngành học\n"
        "🏠 Bấm '0' để về thẳng Màn hình chính"
    ),
    "2": (
        "🔍 CHI TIẾT: KHOA HỌC VÀ KỸ THUẬT MÁY TÍNH\n\n"
        "📋 Thông tin chung:\n"
        "- Mã ngành: 7480204\n"
        "- Thời gian đào tạo: 4 năm (Hệ Cử nhân Chất lượng cao)\n"
        "- Khối xét tuyển: A00, A01, D01\n"
        "- Học phí: 58.000.000 VNĐ/năm\n\n"
        "💡 Đặc điểm nổi bật:\n"
        "- Đào tạo chuyên sâu về Trí tuệ nhân tạo (AI), Khoa học dữ liệu (Data Science), IoT.\n"
        "- Học phần chuyên ngành giảng dạy hoàn toàn bằng tiếng Anh.\n\n"
        "💼 Cơ hội nghề nghiệp:\n"
        "- Lập trình viên Full-stack, Kỹ sư AI/Machine Learning, Chuyên viên phân tích dữ liệu tại FPT, Viettel, VNG...\n"
        "----------------------------------------\n"
        "↩️ Bấm 'C' để quay lại danh sách ngành học\n"
        "🏠 Bấm '0' để về thẳng Màn hình chính"
    ),
    "3": (
        "🔍 CHI TIẾT: NGÀNH NHẬT BẢN HỌC\n\n"
        "📋 Thông tin chung:\n"
        "- Mã ngành: 7220212\n"
        "- Thời gian đào tạo: 4 năm\n"
        "- Khối xét tuyển: D01, D06, A01\n"
        "- Học phí: 58.000.000 VNĐ/năm\n\n"
        "💡 Đặc điểm nổi bật:\n"
        "- Học ngôn ngữ (chuẩn N2/N1) kết hợp nghiên cứu văn hóa, kinh tế và quản trị kiểu Nhật.\n"
        "- Cơ hội trao đổi 1 năm học tập thực tế tại Nhật Bản.\n\n"
        "💼 Cơ hội nghề nghiệp:\n"
        "- Biên-phiên dịch viên cao cấp, Chuyên viên đối ngoại, Nhân sự trong tập đoàn Nhật Bản.\n"
        "----------------------------------------\n"
        "↩️ Bấm 'C' để quay lại danh sách ngành học\n"
        "🏠 Bấm '0' để về thẳng Màn hình chính"
    ),
    "4": (
        "🔍 CHI TIẾT: ĐỔI MỚI VÀ PHÁT TRIỂN TOÀN CẦU\n\n"
        "📋 Thông tin chung:\n"
        "- Mã ngành: 7310101\n"
        "- Thời gian đào tạo: 4 năm\n"
        "- Khối xét tuyển: A01, D01, D03\n"
        "- Học phí: 58.000.000 VNĐ/năm\n\n"
        "💡 Đặc điểm nổi bật:\n"
        "- Chương trình liên ngành Kinh tế quốc tế, Chính sách công và Quản trị bền vững.\n"
        "💼 Cơ hội nghề nghiệp:\n"
        "- Chuyên viên điều phối dự án tại các tổ chức quốc tế (NGO, UN, WB) hoặc tập đoàn đa quốc gia.\n"
        "----------------------------------------\n"
        "↩️ Bấm 'C' để quay lại danh sách ngành học\n"
        "🏠 Bấm '0' để về thẳng Màn hình chính"
    ),
    "5": (
        "🔍 CHI TIẾT: NÔNG NGHIỆP THÔNG MINH VÀ BỀN VỮNG\n\n"
        "📋 Thông tin chung:\n"
        "- Mã ngành: 7620101\n"
        "- Thời gian đào tạo: 4 năm\n"
        "- Khối xét tuyển: B00, A00, D01\n"
        "- Học phí: 58.000.000 VNĐ/năm\n\n"
        "💡 Đặc điểm nổi bật:\n"
        "- Ứng dụng công nghệ 4.0 (Cảm biến, IoT, Drone) vào quản lý nông nghiệp xanh.\n"
        "💼 Cơ hội nghề nghiệp:\n"
        "- Kỹ sư nghiên cứu sản phẩm sinh học, Quản lý trang trại công nghệ cao.\n"
        "----------------------------------------\n"
        "↩️ Bấm 'C' để quay lại danh sách ngành học\n"
        "🏠 Bấm '0' để về thẳng Màn hình chính"
    ),
    "6": (
        "🔍 CHI TIẾT: KỸ THUẬT XÂY DỰNG\n\n"
        "📋 Thông tin chung:\n"
        "- Mã ngành: 7580201\n"
        "- Thời gian đào tạo: 4.5 năm (Hệ Kỹ sư Chất lượng cao)\n"
        "- Khối xét tuyển: A00, A01, D01\n"
        "- Học phí: 58.000.000 VNĐ/năm\n\n"
        "💡 Đặc điểm nổi bật:\n"
        "- Tiếp cận công nghệ xây dựng hiện đại, quản lý dự án công trình bền vững và giảm nhẹ thiên tai theo tiêu chuẩn Nhật Bản.\n"
        "💼 Cơ hội nghề nghiệp:\n"
        "- Kỹ sư thiết kế, giám sát thi công, quản lý dự án tại các tập đoàn xây dựng Việt Nam và Nhật Bản.\n"
        "----------------------------------------\n"
        "↩️ Bấm 'C' để quay lại danh sách ngành học\n"
        "🏠 Bấm '0' để về thẳng Màn hình chính"
    ),
    "7": (
        "🔍 CHI TIẾT: ĐIỀU KHIỂN THÔNG MINH VÀ TỰ ĐỘNG HÓA\n\n"
        "📋 Thông tin chung:\n"
        "- Mã ngành: 7520217\n"
        "- Thời gian đào tạo: 4.5 năm (Hệ Kỹ sư Chất lượng cao)\n"
        "- Khối xét tuyển: A00, A01, D01\n"
        "- Học phí: 58.000.000 VNĐ/năm\n\n"
        "💡 Đặc điểm nổi bật:\n"
        "- Đào tạo chuyên sâu về Robot thông minh, hệ thống nhúng, xe tự hành và tối ưu hóa dây chuyền sản xuất tự động.\n"
        "💼 Cơ hội nghề nghiệp:\n"
        "- Kỹ sư thiết kế robot, vận hành hệ thống tự động hóa trong các nhà máy thông minh (Smart Factory).\n"
        "----------------------------------------\n"
        "↩️ Bấm 'C' để quay lại danh sách ngành học\n"
        "🏠 Bấm '0' để về thẳng Màn hình chính"
    )
}

MENU_3_HOC_PHI = (
    "Học phí của Trường Đại học Việt Nhật (VJU) dao động từ 25.000.000 VNĐ - 58.000.000 VNĐ/năm và cố định toàn khóa.\n\n"
    "1. Học phí chi tiết\n"
    "- Nhóm 58.000.000 VNĐ/năm: Nhật Bản học, Khoa học & Kỹ thuật máy tính, Chip bán dẫn, Cơ điện tử...\n"
    "- Nhóm 25.000.000 VNĐ/năm: Các chương trình định hướng khoa học cơ bản.\n\n"
    "2. Các chính sách học bổng\n"
    "- Học bổng VJU: Các mức từ 25%, 50%, 100% đến 100%++.\n"
    "- Học bổng Doanh nghiệp: Quỹ Zensho, Mitsubishi tài trợ và hỗ trợ thực tập tại Nhật.\n\n"
    "🔙 Bấm phím '0' để QUAY LẠI Màn hình chính"
)

MENU_4_DIA_CHI = (
    "Hiện tại, Trường Đại học Việt Nhật (VJU) - ĐHQGHN có 2 cơ sở chính tại Hà Nội:\n\n"
    "1. Cơ sở Mỹ Đình\n"
    "Địa chỉ: Đường Lưu Hữu Phước, Khu dân cư Mỹ Đình 1, phường Cầu Diễn, quận Nam Từ Liêm, Hà Nội\n\n"
    "2. Cơ sở Hòa Lạc\n"
    "Địa chỉ: Khu đô thị Đại học Quốc gia Hà Nội, xã Hòa Lạc, huyện Thạch Thất, Hà Nội\n\n"
    "🔙 Bấm phím '0' để QUAY LẠI Màn hình chính"
)

MENU_5_LIEN_HE = (
    "📞 Thông tin liên lạc chính\n"
    "Hotline tuyển sinh: 0966 954 736, 0969 638 426\n"
    "Email tuyển sinh: admission@vju.ac.vn\n\n"
    "🏢 Văn phòng hỗ trợ sinh viên\n"
    "- Cơ sở Mỹ Đình: Phòng 510, Tòa nhà Trường Đại học Việt Nhật.\n"
    "- Cơ sở Hòa Lạc: Phòng 103, Tòa nhà Trụ sở, Khu QGHN-04.\n\n"
    "🔙 Bấm phím '0' để QUAY LẠI Màn hình chính"
)

current_state = "MAIN_MENU"

class ChatMessage(BaseModel):
    message: str

def get_main_menu_string():
    return (
        "Xin chào, tôi là chatbot VJU.\n"
        "Hiện tại tôi có thể trả lời các câu hỏi về:\n"
        "1. Thông tin tuyển sinh\n"
        "2. Thông tin về các ngành học\n"
        "3. Mức học phí và chính sách học bổng\n"
        "4. Địa chỉ các cơ sở của trường\n"
        "5. Thông tin liên lạc và các dịch vụ hỗ trợ sinh viên\n"
        "6. Trò chuyện vui vẻ với AI 🎉\n"
        "7. Exit (Thoát chương trình)\n\n"
        "Nhập lựa chọn của bạn (1-7):"
    )

@app.get("/api/init-menu")
async def init_menu():
    global current_state, ai_chat_history
    current_state = "MAIN_MENU"
    ai_chat_history = []  
    return {"response": get_main_menu_string()}


@app.post("/api/chat-stream")
async def chat_stream_endpoint(data: ChatMessage):
    """Giữ nguyên logic tạo luồng stream từ Ollama theo định dạng StreamingResponse của bạn"""
    return StreamingResponse(response_generator(data.message.strip()), media_type="text/plain; charset=utf-8")

async def response_generator(user_msg: str):
    global current_state, ai_chat_history
    user_msg_upper = user_msg.upper()

    if current_state == "MAIN_MENU":
        if user_msg == "1":
            current_state = "VIEWING_STATIC_INFO"
            yield MENU_1_TUYEN_SINH
        elif user_msg == "2":
            current_state = "SUB_MENU_NGANH"
            yield MENU_2_NGANH_HOC
        elif user_msg == "3":
            current_state = "VIEWING_STATIC_INFO"
            yield MENU_3_HOC_PHI
        elif user_msg == "4":
            current_state = "VIEWING_STATIC_INFO"
            yield MENU_4_DIA_CHI
        elif user_msg == "5":
            current_state = "VIEWING_STATIC_INFO"
            yield MENU_5_LIEN_HE
        elif user_msg == "6":
            current_state = "AI_CHAT_MODE"
            ai_chat_history = []
            yield (
                "🤖 Đã bật Chế độ Trò chuyện vui vẻ với AI Sailor!\n"
                "Chữ sẽ chạy ra từng từ mượt mà (Có lưu ngữ cảnh).\n"
                "(Gõ '0' hoặc 'quay lai' để trở về Menu VJU)."
            )
        elif user_msg == "7":
            yield "Cảm ơn bạn đã sử dụng VJU InfoBot. Chúc bạn một ngày tốt lành! 👋"
        else:
            yield "Lựa chọn không hợp lệ. Vui lòng nhập từ 1 đến 7 tương ứng với menu chính."

    elif current_state == "AI_CHAT_MODE":
        if user_msg in ["0", "quay lai", "quay lại"]:
            current_state = "MAIN_MENU"
            ai_chat_history = []
            yield get_main_menu_string()
        else:
            system_message = {
                "role": "system",
                "content": "Bạn là trợ lý ảo VJU InfoBot. Hãy trả lời thân thiện, ngắn gọn bằng tiếng Việt (2-3 câu)."
            }
            ai_chat_history.append({"role": "user", "content": user_msg})
            
            payload = {
                "model": MODEL_NAME,
                "messages": [system_message] + ai_chat_history,
                "stream": True  
            }
            
            full_reply = ""
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    async with client.stream("POST", OLLAMA_URL, json=payload) as response:
                        if response.status_code == 200:
                            async for chunk in response.aiter_lines():
                                if chunk:
                                    try:
                                        chunk_data = json.loads(chunk)
                                        content = chunk_data.get("message", {}).get("content", "")
                                        if content:
                                            full_reply += content
                                            yield content  
                                            await asyncio.sleep(0.01) 
                                    except Exception:
                                        continue
                ai_chat_history.append({"role": "assistant", "content": full_reply})
            except Exception as e:
                yield "Hệ thống AI đang bận, vui lòng thử lại sau!"

    elif current_state == "VIEWING_STATIC_INFO":
        if user_msg == "0":
            current_state = "MAIN_MENU"
            yield get_main_menu_string()
        else:
            yield "Vui lòng bấm phím '0' để quay lại Màn hình chính."

    elif current_state == "SUB_MENU_NGANH":
        if user_msg in NGANH_DETAILS:
            current_state = "VIEWING_NGANH_DETAIL"
            yield NGANH_DETAILS[user_msg]
        elif user_msg == "0":
            current_state = "MAIN_MENU"
            yield get_main_menu_string()
        else:
            yield "Lựa chọn không hợp lệ. Hãy nhập số ngành (1-7) hoặc '0' để quay lại."

    elif current_state == "VIEWING_NGANH_DETAIL":
        if user_msg_upper == "C":
            current_state = "SUB_MENU_NGANH"
            yield MENU_2_NGANH_HOC
        elif user_msg == "0":
            current_state = "MAIN_MENU"
            yield get_main_menu_string()
        else:
            yield "Bấm 'C' để quay lại danh sách ngành hoặc '0' để về Màn hình chính."

def remove_vietnamese_accents(text: str) -> str:
    """Hàm hỗ trợ ép chữ thường và loại bỏ toàn bộ dấu tiếng Việt bám theo văn bản - GIỮ NGUYÊN"""
    accents = {
        'a': 'áàảãạâấầẩẫậăắằẳẵặ',
        'e': 'éèẻẽẹêếềểễệ',
        'i': 'íìỉĩị',
        'o': 'óòỏõọôốồổỗộơớờởỡợ',
        'u': 'úùủũụưứừửữự',
        'y': 'ýỳỷỹỵ',
        'd': 'đ'
    }
    text = text.lower()
    for char, accent_chars in accents.items():
        for accent_char in accent_chars:
            text = text.replace(accent_char, char)
    return text
    
@app.post("/chat")
async def chat_endpoint(data: ChatMessage):
    global current_state, ai_chat_history
    user_msg = data.message.strip()
    user_msg_upper = user_msg.upper()

    try:
       
        if current_state == "MAIN_MENU":
            if user_msg == "1":
                current_state = "VIEWING_STATIC_INFO"
                return {"response": str(MENU_1_TUYEN_SINH)}
            elif user_msg == "2":
                current_state = "SUB_MENU_NGANH"
                return {"response": str(MENU_2_NGANH_HOC)}
            elif user_msg == "3":
                current_state = "VIEWING_STATIC_INFO"
                return {"response": str(MENU_3_HOC_PHI)}
            elif user_msg == "4":
                current_state = "VIEWING_STATIC_INFO"
                return {"response": str(MENU_4_DIA_CHI)}
            elif user_msg == "5":
                current_state = "VIEWING_STATIC_INFO"
                return {"response": str(MENU_5_LIEN_HE)}
            elif user_msg == "6":
                current_state = "AI_CHAT_MODE"
                ai_chat_history = []
                return {
                    "response": (
                        "🤖 Đã bật Chế độ Trò chuyện với AI Sailor!\n\n"
                        "Tin nhắn hiện nguyên một cục mượt mà và lưu ngữ cảnh.\n\n"
                        "(Gõ '0' hoặc 'quay lai' để về Menu VJU)."
                    )
                }
            elif user_msg == "7":
                return {"response": "Cảm ơn bạn đã sử dụng VJU InfoBot. Chúc bạn một ngày tốt lành! 👋"}
            else:
                return {"response": "Lựa chọn không hợp lệ. Vui lòng nhập từ 1 đến 7."}

       
        elif current_state == "AI_CHAT_MODE":
            if user_msg in ["0", "quay lai", "quay lại"]:
                current_state = "MAIN_MENU"
                ai_chat_history = []
                return {"response": str(get_main_menu_string())}
            else:
                system_message = {
                    "role": "system",
                    "content": "Bạn là trợ lý ảo VJU InfoBot. Hãy trả lời thân thiện, ngắn gọn bằng tiếng Việt."
                }
                ai_chat_history.append({"role": "user", "content": user_msg})
                
                payload = {
                    "model": MODEL_NAME,
                    "messages": [system_message] + ai_chat_history,
                    "stream": False
                }
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(OLLAMA_URL, json=payload)
                    if response.status_code == 200:
                        result = response.json()
                        ai_reply = result.get("message", {}).get("content", "")
                        ai_chat_history.append({"role": "assistant", "content": ai_reply})
                        return {"response": str(ai_reply)}
                    else:
                        return {"response": "Hệ thống AI đang bận, vui lòng thử lại sau!"}

      
        elif current_state == "VIEWING_STATIC_INFO":
            if user_msg == "0":
                current_state = "MAIN_MENU"
                return {"response": str(get_main_menu_string())}
            else:
                return {"response": "Vui lòng bấm phím '0' để quay lại Màn hình chính."}

       
        elif current_state == "SUB_MENU_NGANH":
            if user_msg in NGANH_DETAILS:
                current_state = "VIEWING_NGANH_DETAIL"
                return {"response": str(NGANH_DETAILS[user_msg])}
            elif user_msg == "0":
                current_state = "MAIN_MENU"
                return {"response": str(get_main_menu_string())}
            else:
                return {"response": "Lựa chọn không hợp lệ. Hãy nhập từ 1-7 hoặc '0'."}

        elif current_state == "VIEWING_NGANH_DETAIL":
            if user_msg_upper == "C":
                current_state = "SUB_MENU_NGANH"
                return {"response": str(MENU_2_NGANH_HOC)}
            elif user_msg == "0":
                current_state = "MAIN_MENU"
                return {"response": str(get_main_menu_string())}
            else:
                return {"response": "Bấm 'C' để quay lại danh sách ngành hoặc '0' để về Màn hình chính."}
                
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")
        return {"response": "Có lỗi xảy ra trên máy chủ xử lý dữ liệu."}


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)


@app.get("/")
async def get_index():
    index_path = os.path.join(current_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Không tìm thấy file index.html")


@app.get("/{file_name}")
async def get_root_images(file_name: str):
    allowed_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".ico")
    if file_name.lower().endswith(allowed_extensions):
        # Kiểm tra tại thư mục cha chat_bot_VJU2
        parent_image_path = os.path.join(parent_dir, file_name)
        if os.path.exists(parent_image_path):
            return FileResponse(parent_image_path)
        
        # Kiểm tra tại thư mục ACTIVE hiện tại
        current_image_path = os.path.join(current_dir, file_name)
        if os.path.exists(current_image_path):
            return FileResponse(current_image_path)
            
    raise HTTPException(status_code=404, detail=f"Không tìm thấy file {file_name}")


@app.post("/api/reset-chat")
async def reset_chat():
    global current_state, ai_chat_history
    current_state = "MAIN_MENU"
    ai_chat_history = []  
    return {"response": get_main_menu_string()}  


@app.get("/static/{file_name}")
async def get_static_image(file_name: str):
    image_path = os.path.join(parent_dir, file_name)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    raise HTTPException(status_code=404, detail=f"Không tìm thấy file {file_name}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)