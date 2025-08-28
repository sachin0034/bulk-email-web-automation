# Automated Web Form Filler for Bulk Newsletter Signups

## 📌 Overview
This project is an **automated bulk form filler** that allows users to upload a CSV file containing multiple email addresses and automatically sign them up for newsletters across different websites.  
The tool leverages automated browser navigation to detect email input fields, fill them with the provided emails, and submit the forms sequentially.  

It is designed for **seamless, hands-free bulk operations** with robust error handling and automatic browser lifecycle management.

---

## 🚀 Key Features
- **CSV Upload** – Import a CSV file containing email addresses.
- **Multi-site Support** – Provide one or multiple target website URLs for signup.
- **Automated Field Detection** – Locates email input fields dynamically using selectors, attributes, and heuristics.
- **Bulk Submission** – Sequentially submits all emails to all target sites.
- **Error Handling** – Retries on failures, skips inaccessible sites, and logs issues.
- **Browser Lifecycle Management** – Automatically launches, runs, and closes browser sessions.
- **Scalable Workflow** – Handles large lists of emails with queue-based execution.

---

## 🛠️ Tech Stack
- **Language**: Python / Node.js (depending on implementation choice)
- **Libraries/Frameworks**:  
  - `Selenium` or `Playwright` for browser automation  
  - `Pandas` (Python) or `csv-parser` (Node.js) for CSV handling  
  - `Logging` for error tracking  
- **Execution Environment**: Desktop or Server-based automation
