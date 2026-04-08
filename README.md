# RAIoT: Automated Job Market Intelligence & Matcher 🚀

**RAIoT** (Resume Analysis & Intelligent Opportunity Tracking) is a full-stack Python application that bridges the gap between a candidate's resume and the current job market. It uses NLP to analyze a user's seniority and skills, generates market trend visualizations, and provides direct application links to the top 10 job platforms.

![Python](https://img.shields.io/badge/python-3.14+-blue.svg)
![Flask](https://img.shields.io/badge/framework-Flask-green.svg)
![Playwright](https://img.shields.io/badge/automation-Playwright-orange.svg)

---

## 🌟 Key Features

- **📄 AI Resume Parser:** Automatically extracts technical skills and contact info from PDF resumes using `PyPDF2` and Regex.
- **📈 Seniority Detection:** Differentiates between **Fresher** and **Experienced** candidates to filter relevant job opportunities.
- **📊 Visual Business Intelligence:** Generates real-time bar charts of your skill demand scores using `Seaborn` and `Matplotlib`.
- **🕵️ Stealth Meta-Scraper:** Dynamically generates optimized search queries for 10+ major job boards including LinkedIn, Indeed, Glassdoor, and Wellfound.
- **🌐 Interactive Dashboard:** A clean, modern Web UI built with Flask for seamless file uploads and instant results.

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Data Science:** Pandas, Matplotlib, Seaborn
- **Automation/Scraping:** Playwright, Playwright-Stealth
- **NLP/Text Processing:** PyPDF2, Regular Expressions
- **Frontend:** HTML5, CSS3 (Modern Dark Theme), JavaScript (Fetch API)

---

## 📂 Project Structure

```text
Project RAIoT/
├── app.py              # Flask Server & Orchestrator
├── analyzer.py         # Resume Parsing & Skill Extraction
├── scraper.py          # Dynamic Job Search URL Generator
├── visualizer.py       # Data Visualization Logic
├── notifier.py         # Telegram Integration (Optional/Commented)
├── templates/          # HTML Dashboard UI
├── static/             # Generated Charts & Styles
└── uploads/            # Temporary File Processing

🚀 Getting Started
1. Prerequisites
Make sure you have Python 3.10+ installed.

2. Installation
Clone the repository and install the dependencies:

Bash
git clone [https://github.com/your-username/RAIoT.git](https://github.com/your-username/RAIoT.git)
cd RAIoT
python -m venv venv
source venv/bin/activate.fish  # Use .bash or .ps1 depending on your shell
pip install -r requirements.txt
playwright install chromium
3. Running the App
Bash
python app.py
Visit http://127.0.0.1:5000 in your browser.

🛡️ Stealth & Anti-Bot Measures
This project implements playwright-stealth and randomized user-agents to mimic human behavior, ensuring that job boards do not immediately flag the automated requests.

👨‍💻 Author
Sameer, Pranav Sahu and Saksham 
Automating the path to the next big opportunity.
