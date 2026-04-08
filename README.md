<<<<<<< HEAD
# RAIoT: Automated Job Market Intelligence & Matcher 🚀

**RAIoT** (Resume Analysis & Intelligent Opportunity Tracking) is a full-stack Python application that bridges the gap between a candidate's resume and the current job market.

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Data Science:** Pandas, Matplotlib, Seaborn
* **Automation:** Playwright, Playwright-Stealth
* **NLP:** PyPDF2, Regular Expressions

---

## 📂 Project Structure

<b>Project RAIoT/ <br>
├── app.py              # Flask Server<br>
├── analyzer.py         # Resume Parsing<br>
├── scraper.py          # Search URL Generator<br>
├── visualizer.py       # Data Visualization<br>
├── templates/          # HTML UI<br>
├── static/             # Charts<br>
└── uploads/            # Temp storage<br>
🚀<b> Getting Started </b>
1. <b>Prerequisites</b>
Make sure you have Python 3.10+ installed.

2.<b> Installation</b>
Run these commands in your terminal:

Bash<br>
git clone [https://github.com/samashech/Auto-Job-analyzer.git](https://github.com/samashech/Auto-Job-analyzer.git)<br>
cd RAIoT<br>
python -m venv venv<br>
source venv/bin/activate.fish<br>
pip install -r requirements.txt<br>
playwright install chromium<br>
3. Running the App<br>
Bash<br>
python app.py<br>
Visit http://127.0.0.1:5000 in your browser.<br>

🛡️ <b>Stealth & Anti-Bot Measures</b><br>
This project implements playwright-stealth and randomized user-agents to mimic human behavior.<br>

👨‍💻 <b>Authors</b><br>
<b>Sameer, Pranav Sahu, and Saksham</b><br>
Automating the path to the next big opportunity.<br>
=======
# Project RAIoT: Automated Job Market Analyzer

Project RAIoT is a Python-based automation tool designed to help developers and AI engineers stay ahead of the job market. It scrapes real-time job listings from Indeed, extracts in-demand skills using natural language processing (NLP) techniques, calculates a personalized match score against your profile, and visualizes the results.

## 🚀 Features

- **Advanced Web Scraping**: Utilizes `Playwright` with stealth configurations to bypass anti-bot mechanisms and extract job descriptions from Indeed.
- **Skill Extraction**: Automatically identifies key technologies and skills (e.g., Python, SQL, Docker, Machine Learning) mentioned in job postings.
- **Match Scoring**: Compares your personal skill set against the top requirements of the current market to provide a percentage match score.
- **Data Visualization**: Generates clear, professional bar charts using `Seaborn` and `Matplotlib` to highlight trending technologies.
- **Telegram Notifications**: (Optional) Sends automated summaries and trend charts directly to your Telegram chat.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Scraping**: Playwright, Playwright-Stealth
- **Data Analysis**: Pandas, Re (Regex)
- **Visualization**: Matplotlib, Seaborn
- **API Integration**: Telegram Bot API (via Requests)

## 📋 Prerequisites

Before running the project, ensure you have the following installed:
- Python 3.8+
- Node.js (required for Playwright)

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/project-raiot.git
   cd project-raiot
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

## 🚀 Usage

1. **Configure your profile**: Open `main.py` and update the `MY_PROFILE_SKILLS` list with your current skills.
2. **Run the analyzer**:
   ```bash
   python main.py
   ```
3. **View Results**: 
   - Check the console for your **Match Score**.
   - Open `trend_chart.png` in the project directory to see the skill visualization.

## 🤖 Optional: Telegram Alerts

To enable Telegram notifications:
1. Create a bot via [@BotFather](https://t.me/botfather) and get your `TELEGRAM_BOT_TOKEN`.
2. Get your `TELEGRAM_CHAT_ID`.
3. Update the credentials in `notifier.py`.
4. Uncomment the `send_telegram_alert` call in `main.py`.

## 📂 Project Structure

- `main.py`: The central orchestrator for the scraping, analysis, and notification pipeline.
- `scraper.py`: Handles stealth browsing and job data extraction.
- `analyzer.py`: Contains logic for skill extraction and match score calculation.
- `visualizer.py`: Generates the trend charts.
- `notifier.py`: Manages Telegram API communications.
- `requirements.txt`: Lists all Python dependencies.

## ⚠️ Disclaimer

This tool is for educational purposes only. Always respect the `robots.txt` and Terms of Service of any website you scrape. Use responsibly and avoid excessive requests.

---
Built with ❤️ for AI Engineers and Developers.
d1cd916 (modified)
