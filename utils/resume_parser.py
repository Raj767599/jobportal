import fitz  # PyMuPDF
import re

def extract_resume_data(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()

    name = extract_name(text)
    email = extract_email(text)
    skills = extract_skills(text)

    return {
        "name": name,
        "email": email,
        "skills": skills
    }

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_name(text):
    lines = text.strip().split('\n')
    return lines[0] if lines else None

def extract_skills(text):
    skills_keywords = ['Python', 'Django', 'JavaScript', 'REST', 'SQL', 'HTML', 'CSS']
    found = [kw for kw in skills_keywords if kw.lower() in text.lower()]
    return ', '.join(found)
