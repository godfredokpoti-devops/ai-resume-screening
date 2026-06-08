from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.templating import Jinja2Templates
import pdfplumber
import tempfile
import spacy

nlp = spacy.load("en_core_web_sm")
SKILLS = [
    "Python",
    "AWS",
    "Azure",
    "GCP",
    "Terraform",
    "Kubernetes",
    "Docker",
    "Jenkins",
    "GitHub",
    "Linux",
    "FastAPI",
    "DevOps",
    "MLOps",
    "Machine Learning",
    "TensorFlow",
    "PyTorch",
    "Airflow",
    "Spark",
    "SQL",
    "MongoDB"
]

SKILL_WEIGHTS = {
    "Python": 10,
    "AWS": 10,
    "Azure": 10,
    "GCP": 10,
    "Kubernetes": 10,
    "Terraform": 8,
    "Docker": 8,
    "Jenkins": 7,
    "GitHub": 6,
    "Linux": 6,
    "FastAPI": 6,
    "DevOps": 8,
    "MLOps": 8,
    "Machine Learning": 10,
    "TensorFlow": 8,
    "PyTorch": 8,
    "Airflow": 7,
    "Spark": 7,
    "SQL": 5,
    "MongoDB": 5
}
app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )

@app.post("/upload-resume")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    resume_text = ""

    with pdfplumber.open(temp_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text

    found_skills = []
    resume_lower = resume_text.lower()

    for skill in SKILLS:
        if skill.lower() in resume_lower:
            found_skills.append(skill)

    job_lower = job_description.lower()

    required_skills = []
    for skill in SKILLS:
        if skill.lower() in job_lower:
            required_skills.append(skill)

    matched_skills = []
    for skill in required_skills:
        if skill in found_skills:
            matched_skills.append(skill)

    missing_skills = []
    for skill in required_skills:
        if skill not in found_skills:
            missing_skills.append(skill)

    total_possible_score = 0
    earned_score = 0

    for skill in required_skills:
        total_possible_score += SKILL_WEIGHTS.get(skill, 1)

    for skill in matched_skills:
        earned_score += SKILL_WEIGHTS.get(skill, 1)

    if len(required_skills) > 0:
        match_score = round((earned_score / total_possible_score) * 100)
    else:
        match_score = 0

    recommendations = []
    for skill in missing_skills:
        recommendations.append(
            f"Consider adding experience with {skill} to improve ATS match."
        )

    if match_score >= 90:
        rating = "Excellent Match"
    elif match_score >= 75:
        rating = "Good Match"
    elif match_score >= 50:
        rating = "Average Match"
    else:
        rating = "Poor Match"

    if match_score >= 90:
        score_color = "#28a745"
    elif match_score >= 75:
        score_color = "#007bff"
    elif match_score >= 50:
        score_color = "#fd7e14"
    else:
        score_color = "#dc3545"

    return templates.TemplateResponse(
        request,
        "results.html",
        {
            "filename": file.filename,
            "ats_score": match_score,
            "skills_found": found_skills,
            "missing_skills": missing_skills,
            "rating": rating,
            "score_color": score_color,
            "recommendations": recommendations,
        }
    )