import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from groq import Groq
from fpdf import FPDF
from auth import create_user, login_user
from api import analyze_resume

# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# CUSTOM CSS
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(to right, #0f172a, #020617);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1f2937;
}

/* Titles */
h1, h2, h3 {
    color: white !important;
    font-weight: bold;
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 3em;
    border: none;
    border-radius: 15px;
    background: linear-gradient(90deg,#00DBDE,#FC00FF);
    color: white;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
    box-shadow: 0 0 15px rgba(252,0,255,0.5);
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 25px rgba(0,219,222,0.8);
}

/* Text Input */
.stTextInput input {
    border-radius: 12px;
    background-color: #1e293b;
    color: white;
    border: 1px solid #334155;
}

/* Text Area */
.stTextArea textarea {
    border-radius: 12px;
    background-color: #1e293b;
    color: white;
    border: 1px solid #334155;
}

/* File Uploader */
section[data-testid="stFileUploader"] {
    background-color: #111827;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #334155;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid #1f2937;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 0 10px rgba(0,255,200,0.1);
}

/* Success Box */
.stSuccess {
    border-radius: 12px;
}

/* Error Box */
.stError {
    border-radius: 12px;
}

/* Info Box */
.stInfo {
    border-radius: 12px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #00DBDE;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
/* MOBILE RESPONSIVE */

@media screen and (max-width: 768px) {

    h1 {
        font-size: 28px !important;
        text-align: center;
    }

    h2 {
        font-size: 22px !important;
    }

    h3 {
        font-size: 18px !important;
    }

    .stButton > button {
        font-size: 16px;
        height: 2.8em;
    }

    [data-testid="metric-container"] {
        padding: 15px;
    }

    section[data-testid="stSidebar"] {
        width: 100% !important;
    }

    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .stTextInput input,
    .stTextArea textarea {
        font-size: 16px;
    }
}
/* MODERN FILE UPLOADER */

section[data-testid="stFileUploader"] {
    background: rgba(17, 24, 39, 0.8);
    border: 2px dashed #00DBDE;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    transition: 0.3s;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,219,222,0.2);
}

section[data-testid="stFileUploader"]:hover {
    border: 2px dashed #FC00FF;
    box-shadow: 0 0 30px rgba(252,0,255,0.4);
    transform: scale(1.01);
}

/* Upload Text */

section[data-testid="stFileUploader"] label div {
    font-size: 20px;
    font-weight: bold;
    color: white;
}

/* Browse files button */

section[data-testid="stFileUploader"] button {
    background: linear-gradient(90deg,#00DBDE,#FC00FF);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

# GROQ API
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# LOGIN PAGE
if not st.session_state.logged_in:

    st.title("🔐 Login System")

    menu = ["Login", "Signup"]

    choice = st.sidebar.selectbox(
        "Menu",
        menu
    )

    # SIGNUP
    if choice == "Signup":

        st.subheader("Create Account")

        new_user = st.text_input("Username")

        new_password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Signup"):

            success = create_user(
                new_user,
                new_password
            )

            if success:
                st.success("Account Created Successfully ✅")

            else:
                st.error("Username Already Exists ❌")

    # LOGIN
    elif choice == "Login":

        st.subheader("Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            result = login_user(
                username,
                password
            )

            if result:

                st.session_state.logged_in = True

                st.success("Login Successful ✅")

                st.rerun()

            else:
                st.error("Invalid Credentials ❌")

    st.stop()

# MAIN TITLE
st.title("🚀 AI Resume Analyzer")

# SIDEBAR
with st.sidebar:

    st.markdown("""
    <h1 style='text-align:center;'>
        🚀 AI Resume Analyzer
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.info("""
    Upload your resume,
    compare with job description,
    and get AI-powered ATS feedback.
    """)

    st.markdown("---")

    st.success("🔥 Built with Streamlit + Groq AI")

    st.markdown("---")

    st.markdown("""
    <div style="
        text-align:center;
        color:gray;
        font-size:14px;
    ">
    Developed by Yuganesan ⚡
    </div>
    """, unsafe_allow_html=True)

# LOGOUT
if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.rerun()

# SKILLS
skills = [
    "Python",
    "Java",
    "SQL",
    "HTML",
    "CSS",
    "Machine Learning",
    "AI"
]

# FILE UPLOAD
st.markdown("""
<h2 style='text-align:center;'>
📄 Upload Your Resume
</h2>

<p style='text-align:center;color:gray;'>
Drag and drop your resume PDF here
</p>
""", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📄 Upload Your Resume",
    type=["pdf"]
)

# JOB DESCRIPTION
job_description = st.text_area(
    "💼 Paste Job Description"
)

# SHOW JOB DESCRIPTION
if job_description:

    st.subheader("📄 Job Description")

    st.write(job_description)

resume_text = ""

# IF FILE UPLOADED
if uploaded_file is not None:

    # READ PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        resume_text += page.extract_text()

    # SHOW RESUME
    st.subheader("📄 Resume Content")

    st.text_area(
        "Resume Extracted Text",
        resume_text,
        height=250
    )

    # DETECT SKILLS
    found_skills = []

    for skill in skills:

        if skill.lower() in resume_text.lower():

            found_skills.append(skill)

    # ATS SCORE
    score = int(
        (len(found_skills) / len(skills)) * 100
    )

    # MISSING SKILLS
    missing_skills = []

    for skill in skills:

        if skill not in found_skills:

            missing_skills.append(skill)

    # METRICS
    total_skills = len(skills)

    found_count = len(found_skills)

    missing_count = len(missing_skills)

    m1, m2 = st.columns(2)
    m3, m4 = st.columns(2)

    with m1:

        st.metric(
            label="📊 ATS Score",
            value=f"{score}%"
        )

    with m2:

        st.metric(
            label="✅ Skills Found",
            value=found_count
        )

    with m3:

        st.metric(
            label="❌ Missing Skills",
            value=missing_count
        )

    with m4:

        if score >= 70:
            status = "Excellent 🔥"

        elif score >= 40:
            status = "Good 👍"

        else:
            status = "Low 😢"

        st.metric(
            label="🚀 Match Level",
            value=status
        )

    # DASHBOARD
    col1 = st.container()
    col2 = st.container()

    # LEFT
    with col1:

        st.subheader("📊 ATS Score")

        st.progress(score / 100)

        st.metric(
            label="Resume Match",
            value=f"{score}%"
        )

        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg,#00ffcc,#00cc66);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0px 0px 30px #00ffcc;
        ">

        <h1 style='color:white;'>
            Excellent Match 🔥
        </h1>

        <h2 style='color:white;'>
            {score}% ATS Score
        </h2>

        </div>
        """, unsafe_allow_html=True)

    # RIGHT
    with col2:

        st.subheader("✅ Matching Skills")

        for skill in found_skills:

            st.markdown(f"""
            <span style="
                background-color:#00cc66;
                color:white;
                padding:8px 15px;
                border-radius:15px;
                margin:5px;
                display:inline-block;
                font-weight:bold;
            ">
            {skill}
            </span>
            """, unsafe_allow_html=True)

        st.subheader("❌ Missing Skills")

        for skill in missing_skills:

            st.markdown(f"""
            <span style="
                background-color:#ff4b4b;
                color:white;
                padding:8px 15px;
                border-radius:15px;
                margin:5px;
                display:inline-block;
                font-weight:bold;
            ">
            {skill}
            </span>
            """, unsafe_allow_html=True)

        # PIE CHART
        st.subheader("📊 Skills Analysis Chart")

        matched_count = len(found_skills)

        missing_count = len(missing_skills)

        labels = ["Matched Skills", "Missing Skills"]

        sizes = [matched_count, missing_count]

        fig, ax = plt.subplots()

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        st.pyplot(fig)

    # BAR CHART
    st.subheader("📈 Skills Bar Chart")

    skill_counts = [
        1 if skill in found_skills else 0
        for skill in skills
    ]

    fig2, ax2 = plt.subplots()

    ax2.bar(
        skills,
        skill_counts
    )

    ax2.set_ylabel("Skill Match")

    ax2.set_xlabel("Skills")

    st.pyplot(fig2)

    # RECOMMENDATIONS
    st.subheader("🚀 Recommended Skills To Learn")

    for skill in missing_skills:

        st.write("👉 Learn:", skill)

    # AI ANALYZE BUTTON
    if st.button("🤖 Analyze Resume"):

        with st.spinner("Analyzing Resume..."):

            try:

                class ResumeData:

                    def __init__(
                        self,
                        resume_text,
                        job_description
                    ):

                        self.resume_text = resume_text

                        self.job_description = job_description

                data = ResumeData(
                    resume_text,
                    job_description
                )

                result = analyze_resume(data)

                st.subheader("🤖 AI Feedback")

                ai_feedback = result["feedback"]

                st.markdown(f"""
                <div style="
                background-color:#111827;
                padding:20px;
                border-radius:15px;
                border:1px solid #00ff99;
                box-shadow:0 0 15px #00ff99;
                color:white;
                font-size:16px;
                line-height:1.8;
                ">
                {ai_feedback}
                </div>
                """, unsafe_allow_html=True)

                # PDF
                pdf = FPDF()

                pdf.add_page()

                pdf.set_font(
                    "Arial",
                    size=16
                )

                pdf.cell(
                    200,
                    10,
                    txt="AI Resume Analysis Report",
                    ln=True,
                    align='C'
                )

                pdf.ln(10)

                pdf.set_font(
                    "Arial",
                    size=12
                )

                pdf.cell(
                    200,
                    10,
                    txt=f"ATS Score: {score}%",
                    ln=True
                )

                pdf.ln(5)

                pdf.cell(
                    200,
                    10,
                    txt="Detected Skills:",
                    ln=True
                )

                for skill in found_skills:

                    pdf.cell(
                        200,
                        10,
                        txt=f"- {skill}",
                        ln=True
                    )

                pdf.ln(5)

                pdf.cell(
                    200,
                    10,
                    txt="Missing Skills:",
                    ln=True
                )

                for skill in missing_skills:

                    pdf.cell(
                        200,
                        10,
                        txt=f"- {skill}",
                        ln=True
                    )

                pdf.ln(5)

                pdf.multi_cell(
                    0,
                    10,
                    txt=ai_feedback
                )

                pdf.output("resume_report.pdf")

                with open(
                    "resume_report.pdf",
                    "rb"
                ) as file:

                    st.download_button(
                        label="📄 Download Report",
                        data=file,
                        file_name="resume_report.pdf",
                        mime="application/pdf"
                    )

            except Exception as e:

                st.error(e)