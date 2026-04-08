# RAIoT: Automated Job Market Intelligence & Matcher 🚀

**RAIoT** (Resume Analysis & Intelligent Opportunity Tracking) is a full-stack Python application that bridges the gap between a candidate's resume and the current job market. It uses NLP to analyze a user's seniority and skills, generates market trend visualizations, and provides direct application links to the top 10 job platforms.

---

## 🌟 Key Features

* **📄 AI Resume Parser:** Extracts technical skills and contact info from PDF resumes.
* **📈 Seniority Detection:** Differentiates between **Fresher** and **Experienced** candidates.
* **📊 Visual Intelligence:** Generates bar charts of skill demand scores using Seaborn.
* **🕵️ Stealth Meta-Scraper:** Generates optimized search queries for 10+ major job boards.
* **🌐 Interactive Dashboard:** Modern Web UI built with Flask for seamless file uploads.

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Data Science:** Pandas, Matplotlib, Seaborn
* **Automation:** Playwright, Playwright-Stealth
* **NLP:** PyPDF2, Regular Expressions

---

## 📂 Project Structure

```text
Project RAIoT/
├── app.py              # Flask Server & Orchestrator
├── analyzer.py         # Resume Parsing & Skill Extraction
├── scraper.py          # Dynamic Job Search URL Generator
├── visualizer.py       # Data Visualization Logic
├── templates/          # HTML Dashboard UI
├── static/             # Generated Charts & Styles
└── uploads/            # Temporary File Processing

🚀 Getting Started
1. Prerequisites
Make sure you have Python 3.10+ installed.

2. Installation
Clone the repository and install the dependencies:
git clone [https://github.com/samashech/Auto-Job-analyzer.git](https://github.com/samashech/Auto-Job-analyzer.git)
cd RAIoT
python -m venv venv
source venv/bin/activate.fish 
pip install -r requirements.txt
playwright install chromium
3. Running the App
python app.py
Visit http://127.0.0.1:5000 in your browser.

🛡️ Stealth & Anti-Bot Measures
This project implements playwright-stealth and randomized user-agents to mimic human behavior, ensuring that job boards do not immediately flag the automated requests.

👨‍💻 Authors
Sameer, Pranav Sahu, and Saksham Automating the path to the next big opportunity.
