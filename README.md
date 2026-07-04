# Align 🚀

**Align** (formerly RAIoT) is an intelligent, full-stack platform designed to bridge the gap between a candidate's resume and the current job market. It analyzes your resume, extracts your core skills using NLP, orchestrates AI-driven job scraping, and matches you with your best opportunities in real-time.

---

## 🚀 Current Features

- **Resume Parsing**: Upload your PDF resume, and Align will extract text using PyPDF2 and identify core skills and experience level (Fresher/Experienced) using regex matching against a predefined tech stack.
- **Job Search Generation**: Based on your primary skills and level, the application dynamically constructs tailored search URLs for major platforms like Indeed, LinkedIn, Glassdoor, Wellfound, and Naukri.
- **Data Visualization**: Generates a static trend chart (using Matplotlib and Seaborn) comparing your skills against simulated demand scores.
- **Intelligent Dashboard UI**: A responsive web interface that handles resume uploads, displays your extracted profile, and presents the generated job search links.
- **Mock Authentication & Scoring**: Currently features a preliminary mock authentication system and hardcoded match scores to demonstrate the intended user flow.

---

## 🗺️ Roadmap & Future Implementations

We are actively working on realizing the full vision for Align. Here is our technical roadmap:

### Phase 1: Realize Web Scraping Capabilities
- **Implement Playwright Scraper**: Transition from URL generation to actual live scraping using `playwright.sync_api` and `playwright-stealth` to extract real job postings.
- **Data Structuring**: Parse scraped HTML using BeautifulSoup4 to clean job descriptions for deep analysis.

### Phase 2: Advanced NLP & Dynamic Scoring
- **Dynamic Skill Extraction**: Replace hardcoded tech stack regex with a true NLP-based approach (e.g., spaCy or HuggingFace models) for dynamic skill identification.
- **Algorithmic Match Scoring**: Implement a matching engine to calculate the intersection of resume skills and job requirements for a true, dynamic percentage match score.

### Phase 3: Data Persistence
- **Database Integration**: Integrate SQLite/PostgreSQL using SQLAlchemy, moving away from Flask session-based state management.
- **State Management**: Persist user profiles, job history, and application tracking in the database.

### Phase 4: Automation & Alerts
- **Background Tasks**: Implement Celery or APScheduler to run scraping jobs periodically.
- **Telegram Integration**: Fully integrate `notifier.py` with background tasks for automated daily/weekly job match alerts.

### Phase 5: System Integration (n8n, Flask, Next.js)
- Implement an automated pipeline where the Next.js frontend triggers an **n8n workflow**.
- Utilize **Apify** and **Ollama (LLM)** within n8n to intelligently scrape and parse unstructured job descriptions into a unified JSON format.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js (React 19)
- **Styling**: Tailwind CSS v4
- **Language**: TypeScript
- **Animations & Icons**: Framer Motion, Lucide React

### Backend & Data Science
- **Server**: Python 3.10+ with Flask
- **Scraping**: Playwright, BeautifulSoup4 (Planned)
- **NLP & Parsing**: PyPDF2, Regular Expressions (spaCy Planned)
- **Visualization**: Matplotlib, Seaborn, Pandas
- **Automation & Orchestration**: n8n (Node-Based Workflow Automation - Planned)
- **AI & LLMs**: Ollama (Local AI execution - Planned)
- **Database**: SQLite with SQLAlchemy (Planned)

---

## 📂 Project Structure

```
Align/
├── frontend/               # Next.js frontend application
│   ├── src/app/            # App Router pages (Dashboard, Auth, etc.)
│   ├── src/components/     # Reusable UI and layout components
│   └── src/lib/            # Types, utilities, and application state
├── app.py                  # Main Flask application entry point
├── analyzer.py             # Resume parsing and NLP skill extraction logic
├── models.py               # SQLAlchemy database models
├── visualizer.py           # Generation of skill demand trend charts
├── scraper.py              # Legacy/Fallback scraping implementations
├── instance/               # Contains the SQLite database (raiot.db)
├── uploads/                # Local storage for uploaded resumes
├── requirements.txt        # Python backend dependencies
└── run.sh                  # Shell script to orchestrate frontend & backend startup
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
Ensure you have the following installed on your system:
- **Python 3.10** or higher
- **Node.js (v18+)** and npm
- **n8n**: For workflow automation ([Installation Guide](https://docs.n8n.io/hosting/))
- **Ollama**: For local AI parsing ([Download Ollama](https://ollama.com/))
- **Apify Account**: For running the LinkedIn/job board scrapers.

### 2. Clone the Repository
```bash
git clone https://github.com/samashech/Align.git
cd Align
```

### 3. Backend Setup (Flask/Python)
Create and activate a virtual environment, then install dependencies:
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate
# Activate (Windows)
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (Required for fallback scraping)
playwright install chromium
```

### 4. Frontend Setup (Next.js)
Install the frontend dependencies:
```bash
cd frontend
npm install
cd ..
```

### 5. AI & Automation Setup (Ollama & n8n - Planned integration)
To power the future intelligent data extraction pipeline, you will need to configure the AI pipeline:

1. **Start Ollama & Pull the Model**:
   Open a terminal and ensure your local Ollama instance has the required model:
   ```bash
   ollama pull llama3.1:8b
   ```
2. **Configure n8n**:
   - Start your n8n instance.
   - Import the workflow into n8n.
   - Ensure the **Apify node** is configured with your API key.
   - Ensure the **Ollama node** points to your local instance (usually `http://localhost:11434`) and is set to use the `llama3.1:8b` model.
   - Ensure the **HTTP Request node** is configured to POST data back to `http://localhost:5000/api/n8n-webhook/jobs`.

---

## 🚀 Usage

You can run both the Next.js frontend and the Flask backend simultaneously using the provided startup script from the root directory:

```bash
chmod +x run.sh
./run.sh
```

**What this script does:**
- Starts the **Next.js frontend** in the background on `http://localhost:3000`.
- Starts the **Flask backend** in the foreground on `http://localhost:5000` so you can view live scraping logs and API activity.
- Gracefully shuts down both servers when you press `Ctrl+C`.

**Accessing the Application:**
- **Web Dashboard**: Navigate to `http://localhost:3000`
- **Backend API**: `http://localhost:5000`

---

## 👨‍💻 Authors

**Sameer, Pranav Sahu, and Saksham**  
*Automating the path to the next big opportunity.*  
Built with ❤️ for AI Engineers and Developers.