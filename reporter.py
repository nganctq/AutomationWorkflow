import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from datetime import datetime, timedelta
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os


def generate_daily_report_chart():
    """Đọc log từ DB, tạo biểu đồ tròn thể hiện TỶ LỆ % và lưu thành file ảnh."""
    print("Bắt đầu tạo báo cáo hàng ngày...")
    conn = sqlite3.connect(config.DB_NAME)
    
    yesterday = datetime.now() - timedelta(days=1)
    query = f"SELECT status FROM logs WHERE timestamp >= '{yesterday.strftime('%Y-%m-%d %H:%M:%S')}'"
    
    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()

    if df.empty:
        print("Không có log nào trong 24 giờ qua để tạo báo cáo.")
        return None, None

    summary = df['status'].value_counts()
    
     # --- Chuẩn bị dữ liệu và Font ---
    labels = summary.index
    sizes = summary.values
    color_map = {'success': '#28a745', 'failed': '#dc3545'}
    colors = [color_map.get(status, 'gray') for status in labels]
    explode = [0.05 if status == 'failed' else 0 for status in labels]

    try:
        font = FontProperties(family='serif', name='Times New Roman')
    except:
        font = FontProperties()

    # --- Bắt đầu vẽ ---
    plt.style.use('seaborn-v0_8-deep')
    fig, ax = plt.subplots(figsize=(12, 8)) 

    wedges, _, autotexts = ax.pie(sizes, 
                                      colors=colors,
                                      autopct='%1.1f%%',
                                      startangle=140,
                                      explode=explode,
                                      shadow=True,
                                      pctdistance=0.85, # Đẩy % vào gần tâm hơn một chút
                                      textprops=dict(fontproperties=font, color="white", size=16, weight="bold")) # Tăng size lên 16}
    

    # --- Tạo Chú thích (Legend) ---
    legend_labels = [f'{label.capitalize()} - {count} tasks' for label, count in summary.items()]
    ax.legend(wedges, legend_labels,
              title="Status Breakdown",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              prop={'family': font.get_family(), 'size': 14},
              title_fontproperties={'family': font.get_family(), 'size': 16, 'weight': 'bold'})

    total_tasks = summary.sum()
    report_date = datetime.now().strftime('%d-%m-%Y')
    title_text = f'Success & Failure Rate ({report_date})\nTotal Tasks: {total_tasks}'
    
    # Sử dụng suptitle và điều chỉnh vị trí bằng tham số y
    plt.suptitle(title_text, 
                 fontsize=22, 
                 fontweight='bold', 
                 fontproperties=font,
                 y=0.98) # Điều chỉnh vị trí theo chiều dọc

    ax.axis('equal')
    
    chart_path = 'daily_summary.png'
    plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white') 
    print(f"Đã lưu biểu đồ báo cáo hoàn thiện tại: {chart_path}")
    
    return chart_path, summary

def send_report_email(chart_path, summary):
    """Gửi email báo cáo có đính kèm biểu đồ."""
    if not chart_path or not all([config.ADMIN_EMAIL, config.SENDER_EMAIL, config.SENDER_APP_PASSWORD]):
        print("Thiếu thông tin email trong file .env. Không thể gửi báo cáo.")
        return

    msg = MIMEMultipart()
    msg['Subject'] = f"Daily Automation Report - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = config.SENDER_EMAIL
    msg['To'] = config.ADMIN_EMAIL

    success_count = summary.get('success', 0)
    failed_count = summary.get('failed', 0)
    body = (f"Hello Admin,\n\n"
            f"Here is the summary for the past 24 hours:\n\n"
            f"- Successful Tasks: {success_count}\n"
            f"- Failed Tasks: {failed_count}\n\n"
            f"Best regards,\nAutomation Bot")
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(chart_path, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(chart_path))
            msg.attach(img)
    except FileNotFoundError:
        print(f"Lỗi: không tìm thấy file biểu đồ tại {chart_path}")
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(config.SENDER_EMAIL, config.SENDER_APP_PASSWORD)
            smtp.send_message(msg)
        print(f"Gửi email báo cáo thành công tới {config.ADMIN_EMAIL}.")
    except smtplib.SMTPAuthenticationError:
        print("Lỗi xác thực email. Vui lòng kiểm tra SENDER_EMAIL và SENDER_APP_PASSWORD.")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")
