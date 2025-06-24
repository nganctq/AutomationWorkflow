import gspread 
from google.oauth2.service_account import Credentials # Đối tượng chứa thông tin xác thực
from googleapiclient.discovery import build # Thư viện cấp thấp để build các service
from googleapiclient.http import MediaIoBaseUpload # Công cụ chuyên để upload file
import io # Để làm việc với dữ liệu file trong bộ nhớ
import config


# --- HÀM XÁC THỰC ---
def get_credentials():
    """Tạo đối tượng credential từ file JSON."""
    creds = Credentials.from_service_account_file(
        config.CREDENTIALS_FILE,
        scopes = config.SCOPES
    )
    return creds 

# --- CÁC HÀM CHO GOOGLE SHEETS ---
def get_sheet_client():
    """Xác thực và trả về một client để làm việc với Google Sheet.
        Từ đối tượng client này, có thể mở các file, đọc dữ liệu, v.v."""
    creds = get_credentials()
    client = gspread.authorize(creds)
    return client 

def get_all_tasks():
    """Đọc toàn bộ dữ liệu từ Google Sheet."""
    sheet = get_sheet_client().open_by_key(config.GOOGLE_SHEET_ID).sheet1
    tasks = sheet.get_all_records()
    return tasks

def update_task_status(row_index, status, output_link="", error_message=""):
    """Cập nhật trạng thái của một tác vụ trong Goggle Sheet"""
    sheet = get_sheet_client().open_by_key(config.GOOGLE_SHEET_ID).sheet1
    sheet.update_cell(row_index + 2, 6, status) # Cột F là cột 6
    sheet.update_cell(row_index + 2, 7, output_link) # Cột G là cột 7
    sheet.update_cell(row_index + 2, 8, error_message) # Cột H là cột 8

# --- CÁC HÀM CHO GOOGLE DRIVE ---
def get_drive_service():
    """Xác thực và trả về một service để làm việc với Google Drive."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_drive(file_name, file_content, mime_type='image/png'):
    """Upload một file lên thư mục đã chỉ định trong Google Drive."""
    drive_service = get_drive_service()
    
    file_metadata = {
        'name': file_name,
        'parents': [config.GOOGLE_DRIVE_FOLDER_ID]
    }
    media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=mime_type, resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id, webViewLink').execute()
    print(f"File uploaded: {file.get('webViewLink')}")
    return file.get('webViewLink')