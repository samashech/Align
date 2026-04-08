import os
from flask import Flask, render_template, request, jsonify
from analyzer import analyze_resume
from scraper import get_dynamic_job_links
from visualizer import generate_chart

# Keep the import but comment it out so Python doesn't look for it yet
# from notifier import send_telegram_alert 

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

# Ensure required directories exist for the dashboard to function
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

@app.route('/')
def index():
    """Serves the main dashboard HTML."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles resume upload, analysis, and job matching."""
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the resume to the uploads folder
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 1. Run Analysis: Logic to detect Fresher vs Experienced
    user_profile = analyze_resume(filepath)
    
    # 2. Build Search Links: Generates top 10 sites based on seniority
    jobs = get_dynamic_job_links(user_profile['skills'], user_profile['level'])

    # 3. Create Visualization: Saves trend_chart.png to /static/
    chart_path = generate_chart(user_profile['skills'])

    # 4. NOTIFIER (Deactivated for now)
    # ---------------------------------------------------------
    # msg = f"🚀 RAIoT Match Found!\nLevel: {user_profile['level']}\nSkills: {', '.join(user_profile['skills'])}"
    # try:
    #     send_telegram_alert(msg, chart_path)
    # except Exception as e:
    #     print(f"Notifier failed: {e}")
    # ---------------------------------------------------------

    # Return results to the HTML dashboard via JSON
    return jsonify({
        "level": user_profile['level'],
        "skills": user_profile['skills'],
        "jobs": jobs,
        "chart_url": "/static/trend_chart.png"
    })

if __name__ == '__main__':
    # debug=True allows the server to auto-reload when you change code
    app.run(debug=True)
