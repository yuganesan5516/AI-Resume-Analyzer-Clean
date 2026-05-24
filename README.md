# AI Resume Analyzer

This is a simple AI Resume Analyzer project developed using Python and Streamlit.  
The project helps users upload resumes, compare them with job descriptions, and get ATS score analysis with AI feedback.

## Features

- Upload Resume PDF
- ATS Score Analysis
- Job Description Matching
- AI-Based Feedback
- Skill Detection
- Missing Skills Recommendation
- Charts and Analytics
- Download Report as PDF
- Login & Signup System
- Responsive UI

## Technologies Used

- Python
- Streamlit
- Groq API
- PyPDF2
- Matplotlib
- FPDF

## How to Run

### Clone Repository

```bash
git clone https://github.com/yuganesan5516/AI-Resume-Analyzer-Clean.git
```

### Open Project Folder

```bash
cd AI-Resume-Analyzer-Clean
```

### Install Requirements

```bash
pip install -r requirements.txt
```

### Add API Key

Create:

```text
.streamlit/secrets.toml
```

Add your Groq API key:

```toml
GROQ_API_KEY="YOUR_API_KEY"
```

### Run Project

```bash
streamlit run app.py
```

## Project Modules

- Resume Upload & PDF Reading
- ATS Score Calculation
- AI Feedback System
- Skill Matching
- Data Visualization
- PDF Report Generation

## Future Improvements

- More AI Features
- Better ATS Matching
- Resume Templates
- Database Support

## Author

Yuganesan

GitHub:
https://github.com/yuganesan5516
