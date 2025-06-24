import requests
import config
import os

def send_slack_notification(message):
    webhook_url = config.SLACK_WEBHOOK_URL

    if not webhook_url:
        print("Lỗi: Webhook URL bị trống.")
        return

    payload = {'text': message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Gửi thông báo Slack thành công.")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gửi thông báo Slack: {e}")