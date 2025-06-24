from openai import OpenAI
import os
import requests
from openai import OpenAI, APIError, RateLimitError
import config
# GÁN CỨNG API KEY 
MY_API_KEY = config.OPENAI_API_KEY

# Khởi tạo client với key đã gán cứng
client = OpenAI(api_key=MY_API_KEY)

def generate_image(prompt):
    """Sử dụng DALL-E 3 để tạo ảnh từ prompt và trả về nội dung file ảnh."""
    print (f"Gửi yêu cầu tới OpenAI với prompt: '{prompt[:50]}...'")
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="url" # Yêu cầu OpenAI trả về một URL của ảnh 
        )
        image_url = response.data[0].url
        print(f"Nhận được URL ảnh: {image_url}")

        # Tải nội dung ảnh từ URL
        image_response = requests.get(image_url, timeout=60)
        image_response.raise_for_status() # Báo lỗi nếu tải thất bại

        return image_response.content # Trả về DỮ LIỆU THÔ (bytes) của ảnh
    
    except APIError as e: # Có thể bắt lỗi cụ thể hơn
        print(f"Lỗi từ API của OpenAI: {e}")
        raise 
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tải ảnh từ URL: {e}")
        raise 