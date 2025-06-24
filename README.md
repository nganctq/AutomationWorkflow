# Automation Workflow for Athena Studio

This is the solution for **Assignment 1: Automation Task** for the Prompt Engineer / Automation Engineer position at Athena Studio. This project is a robust automation workflow built with Python. It can read tasks from a Google Sheet, use various AI models to generate assets, store the results, send notifications, and create daily summary reports.

## ✨ Key Features

-   **Read Tasks from Google Sheets**: Automatically fetches a list of tasks from a specified Google Sheet.
-   **Flexible AI Model Selection**: Supports multiple AI models (OpenAI, Stable Diffusion) and includes a safe fallback mode (`demotext`).
-   **Automatic Storage in Google Drive**: Systematically stores the generated assets in a dedicated Google Drive folder.
-   **Instant Slack Notifications**: Sends real-time notifications for successful or failed tasks.
-   **Robust Logging**: Logs the details of every task's success or failure into a local SQLite database for easy querying and analysis.
-   **Daily Email Reports with Rate Analysis**: Automatically summarizes the last 24 hours of activity, generates a pie chart visualizing **success/failure rates**, and emails the report to an admin.

## 🚀 Workflow

```mermaid
graph TD
    A[📝 Google Sheets] --> B{🤖 main.py - Coordinator};
    subgraph "AI Model Selection"
        B -- "openai" --> C[OpenAI Generator];
        B -- "stable diffusion" --> D[Stable Diffusion Generator];
        B -- "default/invalid" --> E[Demo Text Generator];
    end
    
    subgraph "Process Result"
        C & D & E --> F{Success/Failure?};
    end

    F -- Success --> G[✅ Save to Google Drive];
    F -- Failure --> H[❌ Log Error];
    
    G & H --> I[📊 Log to SQLite DB];
    I --> J[📢 Send Slack Notification];

    subgraph "Daily Report (Scheduled)"
      K{⏰ reporter.py} -- Read Data --> L[📊 automation_log.db];
      L -- Analyze & Plot --> M[📈 Generate Rate Chart];
      M -- Attach --> N[✉️ Email Report to Admin];
    end
