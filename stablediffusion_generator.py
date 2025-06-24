import base64
import requests
import config
import os
import json



def generate_image(prompt):
    """ 
    Sử dụng API của Stability.ai để tạo ảnh và trả về nội dung file ảnh.
    """
    if not isinstance(prompt, str) or not prompt.strip():
        # Nếu prompt không phải là string, hoặc là string rỗng, báo lỗi ngay
        raise ValueError("Prompt không hợp lệ hoặc bị trống.")
    
    api_key = config.STABILITY_API_KEY
    if not api_key:
        raise ValueError ("Lỗi: STABILITY_API_KEY chưa được thiết lập trong file .env")
    
    print (f"Gửi yêu cầu tới Stability.ai với prompt: '{prompt[:50]}...'")

    api_host = 'https://api.stability.ai'
    engine_id = 'stable-diffusion-v1-6'

    url = f"{api_host}/v1/generation/{engine_id}/text-to-image"

    headers = {
        "Content-Type": "application/json",
        "Accept":"application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "text_prompts": [
            {
                "text": prompt
            }
        ],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=90)
        response.raise_for_status()

        data = response.json()

        image_base64 = data["artifacts"][0]["base64"]
        image_content = base64.b64decode(image_base64)

        print ("Tạo ảnh từ Stability.ai thành công.")
        return image_content
    
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            raise Exception (f"Lỗi từ API Stability.ai: {e.response.text}") from e
        else:
            raise Exception ("Lỗi kết nối tới Stability.ai: {e}") from e

