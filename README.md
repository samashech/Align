1 # Project RAIoT: Automated Job Market Analyzer
2
3 Project RAIoT is a Python-based automation tool designed to help developers and AI
engineers stay ahead of the job market. It scrapes real-time job listings from Indeed,
extracts in-demand skills using natural language processing (NLP) techniques,
calculates a personalized match score against your profile, and visualizes the
results.
4
5 ## 🚀 Features
6
7 - **Advanced Web Scraping**: Utilizes `Playwright` with stealth configurations to
bypass anti-bot mechanisms and extract job descriptions from Indeed.
8 - **Skill Extraction**: Automatically identifies key technologies and skills (e.g.,
Python, SQL, Docker, Machine Learning) mentioned in job postings.
9 - **Match Scoring**: Compares your personal skill set against the top requirements of
the current market to provide a percentage match score.
10 - **Data Visualization**: Generates clear, professional bar charts using `Seaborn` and
`Matplotlib` to highlight trending technologies.
11 - **Telegram Notifications**: (Optional) Sends automated summaries and trend charts
directly to your Telegram chat.
12
13 ## 🛠 Tech Stack
14
15 - **Language**: Python 3.x
16 - **Scraping**: Playwright, Playwright-Stealth
17 - **Data Analysis**: Pandas, Re (Regex)
18 - **Visualization**: Matplotlib, Seaborn
19 - **API Integration**: Telegram Bot API (via Requests)
20
21 ## 📋 Prerequisites
22
23 Before running the project, ensure you have the following installed:
24 - Python 3.8+
25 - Node.js (required for Playwright)
26
27 ## ⚙ Installation
28
29 1. **Clone the repository**:
git clone https://github.com/your-username/project-raiot.git
cd project-raiot
1
2 2. **Create and activate a virtual environment**:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
1
2 3. **Install dependencies**:
pip install -r requirements.txt
1
2 ## 🚀 Usage
3
4 1. **Configure your profile**: Open `main.py` and update the `MY_PROFILE_SKILLS` list
with your current skills.
5 2. **Run the analyzer**:
python main.py

1 3. **View Results**:
2    - Check the console for your **Match Score**.
3    - Open `trend_chart.png` in the project directory to see the skill visualization.
4
5 ## 🤖 Optional: Telegram Alerts
6
7 To enable Telegram notifications:
8 1. Create a bot via [@BotFather](https://t.me/botfather) and get your
`TELEGRAM_BOT_TOKEN`.
9 2. Get your `TELEGRAM_CHAT_ID`.
10 3. Update the credentials in `notifier.py`.
11 4. Uncomment the `send_telegram_alert` call in `main.py`.
12
13 ## 📂 Project Structure
14
15 - `main.py`: The central orchestrator for the scraping, analysis, and notification
pipeline.
16 - `scraper.py`: Handles stealth browsing and job data extraction.
17 - `analyzer.py`: Contains logic for skill extraction and match score calculation.
18 - `visualizer.py`: Generates the trend charts.
19 - `notifier.py`: Manages Telegram API communications.
20 - `requirements.txt`: Lists all Python dependencies.
21
22 ## ⚠ Disclaimer
23
24 This tool is for educational purposes only. Always respect the `robots.txt` and Terms
of Service of any website you scrape. Use responsibly and avoid excessive requests.
25
26 ---
27 Built with ❤ for AI Engineers and Developers.
