import base64

def generate_text_content (prompt):
    """
    Giả lập việc tạo assey bằng cách tạo ra nội dung văn bản.
    Hàm này sẽ nhận prompt và trả về nội dung của prompt thành Base64.
    """
    print (f"Đang mã hóa prompt thành Base64: {prompt [:50]}...")

    try: 
        # Bước 1: Chuyển prompt (string) thành dạng bytes
        prompt_bytes = prompt.encode('utf-8')

        # Bước 2: Mã hóa dữ liệu bytes đó thành Base64, kết quả cũng là bytes
        base64_bytes = base64.b64encode(prompt_bytes)
        # Bước 3: Trả về chuỗi bytes đã mã hóa Base64
        # Đây chính là "sản phẩm" được chuyển đổi của chúng ta
        return base64_bytes
    except Exception as e:
        print (f"Lỗi khi đang mã hóa Base64: {e}")
        raise

