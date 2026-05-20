import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from groq import Groq
from fpdf import FPDF
from auth import create_user, login_user
from api import analyze_resume

# GROQ API KEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
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

st.title("🚀 AI Resume Analyzer")
# Logout Button
if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.rerun()

# Skills List
skills = [
    "Python",
    "Java",
    "SQL",
    "HTML",
    "CSS",
    "Machine Learning",
    "AI",
]

# Upload Resume
uploaded_file = st.file_uploader(
    "📄 Upload Your Resume",
    type=["pdf"]
)

# Job Description
job_description = st.text_area(
    "💼 Paste Job Description"
)
# Show Job Description
if job_description:
    st.subheader("📄 Job Description")
    st.write(job_description)

resume_text = ""

if uploaded_file is not None:

    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    # Resume Content
    st.subheader("📄 Resume Content")

    st.text_area(
        "Resume Extracted Text",
        resume_text,
        height=250
    )   

    # Skill Detection
    found_skills = []

    for skill in skills:
        if skill.lower() in resume_text.lower():
            found_skills.append(skill)

    # ATS Score
    score = int(
        (len(found_skills) / len(skills)) * 100
    )

    # Missing Skills
    missing_skills = []

    for skill in skills:
        if skill not in found_skills:
            missing_skills.append(skill)
    # Dashboard Metrics

    total_skills = len(skills)
    found_count = len(found_skills)
    missing_count = len(missing_skills)

    m1, m2, m3, m4 = st.columns(4)

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
    col1, col2 = st.columns(2)

    # LEFT SIDE
    with col1:

        st.subheader("📊 ATS Score")

        st.progress(score / 100)

        st.metric(
            label="Resume Match",
            value=f"{score}%"
        )

        # Color Card
        if score >= 70:
            bg_color = "#00FFAA"
            text = "Excellent Match 🔥"

        elif score >= 40:
            bg_color = "#FFD700"
            text = "Good Match 👍"

        else:
            bg_color = "#FF4B4B"
            text = "Low Match 😢"

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
    # RIGHT SIDE
    with col2:

        st.subheader("✅ Detected Skills")

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
        # Pie Chart
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

        # Bar Chart

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

                

    # Recommendations
    st.subheader(
        "🚀 Recommended Skills To Learn"
    )

    for skill in missing_skills:
        st.write("👉 Learn:", skill)

    # AI Analyze Button
    # AI Analyze Button
    if st.button("🤖 Analyze Resume"):

        try:
            result = analyze_resume(
                resume_text,
                job_description
            )

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

            # PDF Download Feature

            pdf = FPDF()
            pdf.add_page()

            pdf.set_font("Arial", size=16)
            pdf.cell(
                200,
                10,
                txt="AI Resume Analysis Report",
                ln=True,
                align='C'
            )

            pdf.ln(10)

            pdf.set_font("Arial", size=12)

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

            with open("resume_report.pdf", "rb") as file:

                st.download_button(
                    label="📄 Download Report",
                    data=file,
                    file_name="resume_report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(e)