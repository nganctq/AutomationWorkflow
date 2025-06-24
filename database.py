import sqlite3
import config
from datetime import datetime

# --- HÀM 1: SETUP ---
def setup_database():
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,
            description TEXT,
            status TEXT,
            output_link TEXT,
            error_message TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# --- HÀM 2: LOGGING ----
def log_task (task_id, description, status, output_link=None,error_message=None):
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO logs (task_id, description, status, output_link, error_message, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (task_id, description, status, output_link, error_message, datetime.now()))
    conn.commit()
    conn.close()
    print (f"Logged task {task_id} with status {status}")