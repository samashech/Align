import PyPDF2
import re

def analyze_resume(pdf_path):
    # 1. Initialize the 'text' variable as an empty string
    text = "" 
    
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                # 2. Add content to the 'text' variable
                extracted = page.extract_text()
                if extracted:
                    text += extracted.lower()
    except Exception as e:
        print(f"Error reading PDF: {e}")

    # Logic for Level Detection
    exp_words = ["senior", "lead", "manager", "years experience", "5+"]
    level = "Experienced" if any(w in text for w in exp_words) else "Fresher"

    # Expanded Skill Library
    tech_stack = ["python", "aws", "docker", "react", "sql", "flask", "fastapi", "git", "linux"]
    
    found_skills = []
    for skill in tech_stack:
        # 3. Now 'text' is defined, so this line won't crash!
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.append(skill.capitalize())
            
    return {
        "level": level, 
        "skills": found_skills if found_skills else ["Python"]
    }
