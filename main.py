import google_services
import notifier
import database
import time
import config
import reporter
# Import các module AI để tạo file
import openai_generator
import stablediffusion_generator
import text_generator

def process_tasks():
    """
    Luồng công việc: Lấy task, điều phối đến model AI phù hợp và xử lý kết quả.
    """
    print("Bắt đầu quá trình xử lý tác vụ ...")
    database.setup_database()

    try:
        # Lấy danh sách task từ Google Sheet
        tasks = google_services.get_all_tasks()
    except Exception as e:
        # Nếu không đọc được sheet, báo lỗi và dừng chương trình
        print (f"Lỗi: Không thể đọc Google Sheets. Dừng chương trình. \n Error: {e}")
        notifier.send_slack_notification(f"Lỗi: Không thể đọc Google Sheets. Dừng chương trình. \n Error: {e}")
        return
    
    # --- BƯỚC KIỂM TRA MỚI ---
    pending_tasks = [task for task in tasks if isinstance(task.get('Status'), str) and task.get('Status').lower() == 'pending']

    if not pending_tasks:
        print("\n Không có task nào ở trạng thái 'pending' để xử lý. Chương trình kết thúc.")
        return # Dừng hàm ở đây
    print(f"Tìm thấy {len(pending_tasks)} task 'pending'. Bắt đầu xử lý...")
    
    # Duyệt qua từng task để xử lý
    for idx, task in enumerate (tasks):
        task_id = task.get('TaskID')
        status = task.get('Status')

        # Bỏ qua các task không ở trạng thái 'pending'
        if not isinstance(status,str) or status.lower() != 'pending':
            continue # Bỏ qua
        description = str(task.get('InputDescription', '')).strip()

        # Lấy lựa chọn Model từ cột 'AIModel', nếu để trống thì mặc định là 'Stable Diffusion'
        raw_model_choice = str(task.get('AIModel', '')).strip().lower() # Lấy giá trị thô, mặc định là chuỗi rỗng ''

        # Xác định model_choice cuối cùng 
        if raw_model_choice in ['openai', 'stable diffusion', 'demotext']:
            model_choice = raw_model_choice
        elif not raw_model_choice: # Nếu để trống
            model_choice = 'stable diffusion' # Mặc định chạy Stable Diffusion
        else: # Nếu nhập một giá trị không hợp lệ
            print(f"Cảnh báo: Model '{raw_model_choice}' không được hỗ trợ. Chuyển sang chế độ Demo Text.")
            model_choice = 'demotext' # Chạy chế độ an toàn nhất

        print (f"\n--- Đang xử lý Task: {task_id} với model {model_choice} ---")

        try:
            # Báo cho người dùng biết task đang được xử lý
            google_services.update_task_status(idx, "processing")
            asset_content = None
            # Model nào?
            if model_choice == 'openai':
                asset_content = openai_generator.generate_image(description)
            elif model_choice == 'stable diffusion':
                asset_content = stablediffusion_generator.generate_image(description)
            else: 
                asset_content = text_generator.generate_text_content(description)

            # Nếu asset_content được tạo thành công
            if asset_content:
                file_extension = 'txt' if model_choice == 'demotext' else 'png'
                mime_type = 'text/plain'if model_choice == 'demotext' else 'image/png'
                file_name = f"{task_id}_{model_choice.replace(' ','_')}_{description[:20].replace(' ','_')}.{file_extension}"
                output_link = google_services.upload_file_to_drive(file_name,asset_content,mime_type=mime_type)

                # Cập nhật kết quả thành công
                google_services.update_task_status(idx, "success", output_link=output_link)
                database.log_task(task_id, description,"success", output_link=output_link)
                notifier.send_slack_notification(f"Task: [{task_id}] hoàn thành! \nModel: {model_choice} \n Link: {output_link}")


        except Exception as e:
            error_message = str(e)

            # KIỂM TRA LỖI RIÊNG CHO OPENAI
            if model_choice == 'openai' and 'image_generation_user_error' in error_message:
                # Tạo một thông báo lỗi "thân thiện" hơn
                friendly_error_message = ("Gọi API OpenAI không thành công, có thể là do sự cố thanh toán"
                                          "(ví dụ: bản dùng thử miễn phí đã hết hạn hoặc không đủ tín dụng).")
                print(f"Lỗi OpenAI đã được xác định: {friendly_error_message}")
                error_message = friendly_error_message
            
            print(f"Lỗi khi xử lý task {task_id}: {error_message}")

            # Ghi nhận lỗi và cập nhật
            google_services.update_task_status(idx, "failed", error_message=error_message)
            database.log_task(task_id, description, "failed", error_message=error_message)
            notifier.send_slack_notification(f"Task: [{task_id}] thất bại! \nModel: {model_choice} \nLỗi: {error_message}")

        # Tạm dừng sau mỗi task để tránh quá tải API
        time.sleep(2)

        print ("\n Hoàn tất quá trình xử lý tác vụ.")

        print("\n--- Bắt đầu quy trình tạo và gửi báo cáo hàng ngày ---")
        try:
            chart_path, summary_data = reporter.generate_daily_report_chart()
            if chart_path and summary_data is not None:
                reporter.send_report_email(chart_path, summary_data)
            else:
                print("Không tạo báo cáo do không có dữ liệu hoặc đã xảy ra lỗi.")
        except Exception as e:
            print(f"Lỗi không mong muốn khi tạo báo cáo: {e}")
            notifier.send_slack_notification(f"Lỗi nghiêm trọng khi chạy quy trình báo cáo: {e}")

if __name__ == "__main__" :
    process_tasks()