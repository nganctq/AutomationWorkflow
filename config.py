# Đây là nơi lưu trữ các cài đặt không-bí-mật của dự án.
# Các giá trị này có thể được chia sẻ công khai mà không gây nguy hiểm.

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=r"D:\PROJECT_FOR_CVs\PROMPT_ENGINEER_AUTOMATION_ENGINEER_ASSIGNMENT\athena_automation(final)\.env")

# --- Cấu hình Google ---
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

# --- Cấu hình các API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# --- Cấu hình thông báo ---
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# --- Cấu hình Email ---
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_APP_PASSWORD = os.getenv('SENDER_APP_PASSWORD')


# --- CÁC GIÁ TRỊ CỐ ĐỊNH, KHÔNG CẦN ĐỌC TỪ .ENV ---
CREDENTIALS_FILE = 'credentials.json'
DB_NAME = 'automation_log.db'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
