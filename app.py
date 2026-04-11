import os
import json
import time
import threading
from queue import Queue, Empty
from flask import Flask, render_template, request, jsonify, send_from_directory, Response, session
from analyzer import analyze_resume
from scraper import get_dynamic_job_links
from visualizer import generate_chart
from models import db, User, JobMatch

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raiot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'raiot-secret-key-2026'
db.init_app(app)

# Global stores for real-time job streaming
# Key: user_id, Value: {'jobs': [], 'scraping': bool, 'queue': Queue, 'finished': bool}
scraping_state = {}

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

# Create tables inside the app context
with app.app_context():
    db.create_all()

def background_scrape_job(user_id, skills, level, job_type, experience_level, location):
    """Background thread to scrape jobs and push to SSE queue."""
    # Create app context for database operations
    with app.app_context():
        state = scraping_state.get(user_id)
        if not state:
            print(f"⚠️ No scraping state for user {user_id}")
            return
        
        print(f"🚀 Starting background scrape for user {user_id}")
        print(f"   Skills: {len(skills)}, Level: {level}, Type: {job_type}")
        
        state['scraping'] = True
        state['total_skills'] = len(skills)
        state['processed_skills'] = 0
        
        try:
            # Scrape jobs - this will take time
            print(f"🔍 Calling scraper.get_dynamic_job_links()...")
            jobs = get_dynamic_job_links(skills, level, job_type, experience_level, location)
            print(f"✅ Scraper returned {len(jobs)} jobs")

            # Save each job to database and stream to client
            for idx, job in enumerate(jobs):
                new_match = JobMatch(
                    user_id=user_id,
                    title=job.get('title', f"{level} Role"),
                    company=job.get('company', 'Various Companies'),
                    url=job.get('url', '#'),
                    source=job.get('name', job.get('source', 'Web Scraper')),
                    job_type=job_type,
                    relevance_score=job.get('relevance_score', 0)
                )
                db.session.add(new_match)
                db.session.commit()
                
                print(f"   💾 Saved job {idx+1}/{len(jobs)}: {job.get('title', 'N/A')}")

                # Add to state
                state['jobs'].append(job)
                state['processed_skills'] = min(idx + 1, len(skills))

                # Push to SSE queue
                state['queue'].put({
                    'type': 'job',
                    'data': job,
                    'total_jobs': len(state['jobs'])
                })

            # Signal completion
            state['scraping'] = False
            state['processed_skills'] = len(skills)
            state['queue'].put({
                'type': 'complete',
                'data': {'total_jobs': len(state['jobs'])}
            })
            
            print(f"✅ Scraping complete for user {user_id}: {len(state['jobs'])} jobs saved")

        except Exception as e:
            print(f"❌ Error scraping for user {user_id}: {e}")
            import traceback
            traceback.print_exc()
            state['scraping'] = False
            state['queue'].put({
                'type': 'error',
                'data': {'message': str(e)}
            })

        # Mark as done
        state['finished'] = True


@app.route('/')
def index():
    """Serves the main dashboard HTML."""
    return render_template('index.html')

@app.route('/complete-profile')
def complete_profile():
    """Serves the Complete Your Profile page."""
    return render_template('complete_profile.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serves uploaded resumes."""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/stream-jobs/<int:user_id>')
def stream_jobs(user_id):
    """Server-Sent Events endpoint for real-time job streaming."""
    def event_stream():
        state = scraping_state.get(user_id)
        if not state:
            yield f"data: {json.dumps({'type': 'error', 'data': {'message': 'No scraping session found'}})}\n\n"
            return

        # Send initial state immediately
        yield f"data: {json.dumps({
            'type': 'init',
            'data': {
                'jobs': state['jobs'],
                'scraping': state['scraping'],
                'processed_skills': state.get('processed_skills', 0),
                'total_skills': state.get('total_skills', 0),
                'total_jobs': len(state['jobs'])
            }
        })}\n\n"

        # Stream new jobs as they come in
        while not state.get('finished', False):
            try:
                message = state['queue'].get(timeout=5)  # 5 second timeout
                yield f"data: {json.dumps(message)}\n\n"
            except Empty:
                # Timeout - send heartbeat
                yield f": heartbeat\n\n"
                continue
            except GeneratorExit:
                break
    
    return Response(event_stream(), mimetype='text/event-stream')

@app.route('/get-jobs/<int:user_id>')
def get_jobs(user_id):
    """Get all jobs for a user from database OR live scraping state."""
    print(f"📊 Fetching jobs for user {user_id}...")
    
    # First try to get from live scraping state
    state = scraping_state.get(user_id)
    if state and len(state['jobs']) > 0:
        print(f"   ✅ Found {len(state['jobs'])} jobs in live scraping state")
        return jsonify({
            'jobs': state['jobs'],
            'total': len(state['jobs']),
            'source': 'live_state'
        })
    
    # Fallback to database
    jobs = JobMatch.query.filter_by(user_id=user_id).order_by(JobMatch.relevance_score.desc()).all()
    print(f"   📁 Found {len(jobs)} jobs in database")
    
    jobs_data = [{
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'url': job.url,
        'source': job.source,
        'job_type': job.job_type,
        'relevance_score': job.relevance_score
    } for job in jobs]
    
    return jsonify({
        'jobs': jobs_data,
        'total': len(jobs_data),
        'source': 'database'
    })

@app.route('/debug-jobs/<int:user_id>')
def debug_jobs(user_id):
    """Debug endpoint to check jobs in database."""
    jobs = JobMatch.query.filter_by(user_id=user_id).all()
    state = scraping_state.get(user_id)
    
    return jsonify({
        'user_id': user_id,
        'jobs_in_db': len(jobs),
        'jobs_in_state': len(state['jobs']) if state else 0,
        'scraping': state['scraping'] if state else False,
        'finished': state['finished'] if state else False,
        'sample_jobs': [{
            'title': j.title,
            'source': j.source,
            'score': j.relevance_score
        } for j in jobs[:5]]
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles resume upload, starts background scraping, redirects to profile page."""
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the resume to the uploads folder
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 1. Run NLP Analysis to get dynamic skills and profile
    user_profile = analyze_resume(filepath)

    # Extract desired job type from request if user provided one (default: "Full-time")
    job_type = request.form.get('job_type', 'Full-time')
    experience_level = request.form.get('experience_level', '')
    preferred_location = request.form.get('preferred_location', '')

    # Phase 1: Save User to SQLite Database
    user = User(
        name=user_profile.get('name', 'Applicant'),
        email=user_profile.get('email', ''),
        phone=user_profile.get('phone', ''),
        level=user_profile['level'],
        skills=", ".join(user_profile['skills'])
    )
    db.session.add(user)
    db.session.commit()

    # Initialize scraping state for this user
    scraping_state[user.id] = {
        'jobs': [],
        'scraping': True,
        'finished': False,
        'queue': Queue(),
        'total_skills': len(user_profile['skills']),
        'processed_skills': 0
    }

    # Start background scraping
    scrape_thread = threading.Thread(
        target=background_scrape_job,
        args=(user.id, user_profile['skills'], user_profile['level'], 
              job_type, experience_level if experience_level else user_profile['level'],
              preferred_location),
        daemon=True
    )
    scrape_thread.start()

    # Return profile data and redirect info
    return jsonify({
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "level": user.level,
        "skills": user_profile['skills'],
        "job_type": job_type,
        "experience_level": experience_level,
        "preferred_location": preferred_location,
        "resume_url": f"/uploads/{file.filename}",
        "redirect": "/complete-profile"
    })

@app.route('/update-profile', methods=['POST'])
def update_profile():
    """Update user profile with completed information."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Update user fields
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'job_type' in data:
        user.level = data['job_type']
    if 'location' in data:
        user.phone = user.phone  # Keep phone, store location separately if needed
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "user_id": user.id,
        "name": user.name
    })

@app.route('/fetch_jobs', methods=['POST'])
def fetch_jobs():
    """Handles fetching jobs based on manually entered skills."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    skills_str = data.get('skills', '')
    level = data.get('level', 'Experienced')
    job_type = data.get('job_type', 'Full-time')

    # Parse skills
    skills = [s.strip() for s in skills_str.split(',')] if skills_str else []
    skills = [s for s in skills if s] # Remove empty strings

    # Build Search Links using the Scraper
    jobs = get_dynamic_job_links(skills, level, job_type)

    # Generate Visualization
    chart_path = generate_chart(skills) if skills else None

    return jsonify({
        "skills": skills,
        "jobs": jobs,
        "chart_url": "/static/trend_chart.png" if chart_path else None
    })

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
