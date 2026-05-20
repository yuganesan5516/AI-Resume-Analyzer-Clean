from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str

@app.get("/")
def home():
    return {
        "message": "hi salai FastAPI Backend Running 🚀"
    }

@app.post("/analyze")
def analyze_resume(data: ResumeRequest):

    prompt = f"""
    Analyze this resume and job description.

    Resume:
    {data.resume_text}

    Job Description:
    {data.job_description}

    Give:
    1. ATS Score
    2. Matching Skills
    3. Missing Skills
    4. Suggestions
    """

    chat_completion = (
        client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
    )

    return {
        "feedback":
        chat_completion
        .choices[0]
        .message
        .content
    }