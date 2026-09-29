import streamlit as st
from pypdf import PdfReader
from database import create_database, save_analysis, get_analysis_history

# ============================================================
# DATABASE
# ============================================================

create_database()

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Career & Placement Assistant",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 AI Career Assistant")
    st.write("Your career companion")

    st.divider()

    st.markdown("### 📌 Features")
    st.write("📊 Career Dashboard")
    st.write("📄 Resume Analysis")
    st.write("🎯 Job Matching")
    st.write("📚 Skill Gap")
    st.write("🎤 Interview Preparation")
    st.write("🚀 Career Roadmap")
    st.write("💾 Saved Analysis")

    st.divider()

    st.caption("Python • Streamlit • SQLite")


# ============================================================
# MAIN TITLE
# ============================================================

st.title("🤖 AI Career & Placement Assistant")

st.write(
    "Analyze your resume, match it with jobs, identify skill gaps "
    "and get a personalized career roadmap."
)

st.divider()


# ============================================================
# LOAD HISTORY
# ============================================================

history = get_analysis_history()


# ============================================================
# DASHBOARD
# ============================================================

st.header("📊 Career Dashboard")

if history:

    latest = history[0]

    latest_resume_score = latest[2]
    latest_job_match = latest[4]
    latest_skills = latest[3]

    if latest_skills:
        skill_count = len(
            [x for x in latest_skills.split(",") if x.strip()]
        )
    else:
        skill_count = 0

    total_analyses = len(history)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📄 Resume Score",
            f"{latest_resume_score}/100"
        )

    with col2:
        st.metric(
            "🎯 Job Match",
            f"{latest_job_match}%"
        )

    with col3:
        st.metric(
            "🛠️ Skills Found",
            skill_count
        )

    with col4:
        st.metric(
            "💾 Saved Analyses",
            total_analyses
        )

else:

    st.info(
        "Upload a resume and save an analysis to see your dashboard."
    )


# ============================================================
# MODE SELECTION
# ============================================================

mode = st.radio(
    "Choose your career stage:",
    ["Looking for a Job", "Already Placed"],
    horizontal=True
)


# ============================================================
# JOB SEEKER
# ============================================================

if mode == "Looking for a Job":

    st.header("📄 Resume Analysis")

    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"]
    )

    resume_text = ""
    detected_skills = []
    score = 0
    match_percentage = 0
    missing_skills = []
    job_description = ""

    # --------------------------------------------------------
    # RESUME UPLOAD
    # --------------------------------------------------------

    if uploaded_file is not None:

        try:

            reader = PdfReader(uploaded_file)

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    resume_text += text

            st.success("✅ Resume uploaded successfully!")

        except Exception:

            st.error("❌ Unable to read the PDF.")
            st.stop()


        # ----------------------------------------------------
        # SKILLS DATABASE
        # ----------------------------------------------------

        skills = [
            "python",
            "c++",
            "java",
            "sql",
            "numpy",
            "pandas",
            "streamlit",
            "machine learning",
            "deep learning",
            "data analysis",
            "data visualization",
            "statistics",
            "git",
            "github",
            "html",
            "css",
            "javascript",
            "communication",
            "problem solving"
        ]

        resume_lower = resume_text.lower()


        # ----------------------------------------------------
        # DETECT SKILLS
        # ----------------------------------------------------

        for skill in skills:

            if skill in resume_lower:
                detected_skills.append(skill)


        # ----------------------------------------------------
        # RESUME SCORE
        # ----------------------------------------------------

        score = min(
            100,
            int((len(detected_skills) / len(skills)) * 100)
        )


        # ====================================================
        # RESUME METRICS
        # ====================================================

        st.subheader("📊 Resume Overview")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📄 Resume Score",
                f"{score}/100"
            )

        with col2:

            st.metric(
                "🎯 Job Match",
                f"{match_percentage}%"
                if job_description.strip()
                else "—"
            )

        with col3:

            st.metric(
                "🛠️ Skills Found",
                len(detected_skills)
            )


        # ----------------------------------------------------
        # DETECTED SKILLS
        # ----------------------------------------------------

        st.subheader("🛠️ Detected Skills")

        if detected_skills:

            st.success(
                ", ".join(detected_skills)
            )

        else:

            st.warning(
                "No matching technical skills were detected."
            )


        # ----------------------------------------------------
        # RESUME SUGGESTIONS
        # ----------------------------------------------------

        st.subheader("💡 Resume Suggestions")

        if score >= 70:

            st.success(
                "Your resume contains a good number of relevant skills."
            )

        elif score >= 40:

            st.warning(
                "Your resume is average. Consider adding more relevant technical skills."
            )

        else:

            st.error(
                "Your resume needs improvement. Add technical skills and projects."
            )


        # ----------------------------------------------------
        # SMART RESUME FEEDBACK
        # ----------------------------------------------------

        st.subheader("🤖 Smart Resume Feedback")

        if score >= 70:
            st.success(
                "Your technical skill section looks strong. Keep adding projects and role-specific skills."
            )
        elif score >= 40:
            st.warning(
                "Your technical skill section is average. Add more relevant skills and practical projects."
            )
        else:
            st.error(
                "Your technical skill section needs improvement. Focus on core technical skills and projects."
            )

        if "python" not in detected_skills:
            st.write("• Consider adding Python projects.")

        if "sql" not in detected_skills:
            st.write("• Add SQL knowledge and database projects.")

        if "pandas" not in detected_skills:
            st.write("• Learn Pandas for data analysis.")

        if "git" not in detected_skills:
            st.write("• Add Git/GitHub to your technical skills.")


        # ====================================================
        # JOB DESCRIPTION
        # ====================================================

        st.divider()

        st.header("🎯 Job Description Analyzer")

        job_description = st.text_area(
            "Paste the Job Description here:",
            height=180,
            placeholder="Paste the job description..."
        )


        if job_description:

            job_lower = job_description.lower()

            job_skills = []

            for skill in skills:

                if skill in job_lower:
                    job_skills.append(skill)


            st.subheader("🔎 Skills Required by Job")

            if job_skills:

                st.write(
                    ", ".join(job_skills)
                )

            else:

                st.info(
                    "No predefined skills detected."
                )


            # ------------------------------------------------
            # MATCHED SKILLS
            # ------------------------------------------------

            matched_skills = []

            for skill in job_skills:

                if skill in detected_skills:
                    matched_skills.append(skill)


            # ------------------------------------------------
            # MISSING SKILLS
            # ------------------------------------------------

            missing_skills = []

            for skill in job_skills:

                if skill not in detected_skills:
                    missing_skills.append(skill)


            # ------------------------------------------------
            # JOB MATCH
            # ------------------------------------------------

            if len(job_skills) > 0:

                match_percentage = int(
                    (len(matched_skills) / len(job_skills)) * 100
                )

            else:

                match_percentage = 0


            # ------------------------------------------------
            # JOB MATCH METRICS
            # ------------------------------------------------

            st.subheader("🎯 Resume ↔ Job Match")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Job Match",
                    f"{match_percentage}%"
                )

            with col2:

                st.metric(
                    "Matched Skills",
                    len(matched_skills)
                )


            # ------------------------------------------------
            # MATCHED SKILLS
            # ------------------------------------------------

            st.write("### ✅ Matched Skills")

            if matched_skills:

                st.success(
                    ", ".join(matched_skills)
                )

            else:

                st.warning(
                    "No matching skills found."
                )


            # ------------------------------------------------
            # MISSING SKILLS
            # ------------------------------------------------

            st.write("### ❌ Missing Skills")

            if missing_skills:

                st.error(
                    ", ".join(missing_skills)
                )

            else:

                st.success(
                    "No major missing skills detected."
                )


            # ------------------------------------------------
            # SAVE ANALYSIS
            # ------------------------------------------------

            st.divider()

            if st.button(
                "💾 Save My Analysis",
                use_container_width=True
            ):

                save_analysis(
                    uploaded_file.name,
                    score,
                    detected_skills,
                    match_percentage,
                    missing_skills
                )

                st.success(
                    "✅ Your analysis has been saved successfully!"
                )


        # ====================================================
        # PERSONALIZED CAREER ROADMAP
        # ====================================================

        st.divider()

        st.header("🚀 Personalized Career Roadmap")

        st.write(
            "Based on your resume and missing skills, "
            "here is a suggested learning path:"
        )

        if missing_skills:

            st.subheader("📌 Step 1 — Improve Missing Skills")

            for skill in missing_skills:

                st.write(
                    f"🔹 Learn **{skill.title()}**"
                )


            st.subheader("📌 Step 2 — Build Projects")

            st.write(
                "🔹 Build at least 2 practical projects using your new skills."
            )

            st.write(
                "🔹 Upload projects to GitHub."
            )


            st.subheader("📌 Step 3 — Interview Preparation")

            st.write(
                "🔹 Practice Python, SQL and role-specific technical questions."
            )

            st.write(
                "🔹 Practice HR interview questions."
            )


            st.subheader("📌 Step 4 — Apply for Jobs")

            st.write(
                "🔹 Apply for internships and entry-level jobs matching your skills."
            )

            st.write(
                "🔹 Keep improving your resume based on job descriptions."
            )

        else:

            st.success(
                "🎉 Your current resume matches the detected job requirements!"
            )

            st.write(
                "Next focus on projects, interview preparation and job applications."
            )


        # ====================================================
        # SKILL GAP ANALYSIS
        # ====================================================

        st.divider()

        st.header("📚 Skill Gap Analysis")

        if missing_skills:

            st.write(
                "Skills you should focus on learning:"
            )

            for skill in missing_skills:

                st.write(
                    f"🔹 {skill.title()}"
                )

        else:

            st.info(
                "Enter a Job Description to see your skill gap."
            )


        # ====================================================
        # INTERVIEW PREPARATION
        # ====================================================

        st.divider()

        st.header("🎤 Interview Preparation")

        difficulty = st.selectbox(
            "Select Difficulty",
            ["Easy", "Medium", "Hard"]
        )


        question_bank = {

            "python": [
                "What is Python?",
                "What is the difference between a list and tuple?",
                "What are functions in Python?"
            ],

            "sql": [
                "What is SQL?",
                "What is a primary key?",
                "What is the difference between WHERE and HAVING?"
            ],

            "pandas": [
                "What is Pandas?",
                "What is a DataFrame?",
                "How do you handle missing values in Pandas?"
            ],

            "numpy": [
                "What is NumPy?",
                "What is an array?",
                "Why is NumPy used in data science?"
            ],

            "machine learning": [
                "What is Machine Learning?",
                "What is supervised learning?",
                "What is overfitting?"
            ],

            "data analysis": [
                "What is data analysis?",
                "What are the steps involved in data analysis?",
                "Why is data cleaning important?"
            ],

            "git": [
                "What is Git?",
                "What is GitHub?",
                "What is git commit?"
            ]
        }


        available_questions = []

        for skill in detected_skills:

            if skill in question_bank:

                available_questions.extend(
                    question_bank[skill]
                )


        if available_questions:

            st.write(
                f"### 📝 {difficulty} Level Questions"
            )

            for i, question in enumerate(
                available_questions[:5],
                start=1
            ):

                st.write(
                    f"**Q{i}. {question}**"
                )

        else:

            st.info(
                "Add technical skills to your resume to get relevant interview questions."
            )


        # ====================================================
        # HR QUESTIONS
        # ====================================================

        st.subheader("👤 HR Interview Questions")

        hr_questions = [
            "Tell me about yourself.",
            "Why should we hire you?",
            "What are your strengths?",
            "What are your weaknesses?",
            "Where do you see yourself in five years?"
        ]

        for i, question in enumerate(
            hr_questions,
            start=1
        ):

            st.write(
                f"**Q{i}. {question}**"
            )


        # ====================================================
        # INTERVIEW TIPS
        # ====================================================

        st.subheader("💡 Interview Tips")

        st.write("• Understand your resume properly.")
        st.write("• Practice basic Python and SQL.")
        st.write("• Explain your projects clearly.")
        st.write("• Be confident while answering HR questions.")
        st.write("• If you don't know an answer, be honest.")


# ============================================================
# ALREADY PLACED
# ============================================================

else:

    st.header("🚀 Career Growth Roadmap")

    role = st.selectbox(
        "Select your current role:",
        [
            "Software Developer",
            "Data Analyst",
            "Data Scientist",
            "AI/ML Engineer",
            "Business Analyst"
        ]
    )


    experience = st.selectbox(
        "Select your experience:",
        [
            "0–1 Years",
            "1–2 Years",
            "2–4 Years",
            "4+ Years"
        ]
    )


    st.subheader("📈 Recommended Career Roadmap")


    roadmap = {

        "Software Developer": [
            "Strengthen Data Structures & Algorithms",
            "Learn SQL and Databases",
            "Build real-world projects",
            "Learn Git and GitHub",
            "Prepare for technical interviews"
        ],

        "Data Analyst": [
            "Strengthen SQL",
            "Learn Advanced Excel",
            "Learn Pandas and NumPy",
            "Learn Power BI or Tableau",
            "Build Data Analytics projects"
        ],

        "Data Scientist": [
            "Strengthen Python",
            "Learn Statistics",
            "Learn Machine Learning",
            "Learn Pandas and NumPy",
            "Build Machine Learning projects"
        ],

        "AI/ML Engineer": [
            "Strengthen Python",
            "Learn Machine Learning",
            "Learn Deep Learning",
            "Learn NLP and Computer Vision",
            "Build AI projects"
        ],

        "Business Analyst": [
            "Learn Excel",
            "Strengthen SQL",
            "Learn Data Visualization",
            "Improve Communication Skills",
            "Learn Business Analysis techniques"
        ]
    }


    for step in roadmap[role]:

        st.write(
            f"🔹 {step}"
        )


    st.info(
        f"Career roadmap generated for a {role} with {experience} experience."
    )


# ============================================================
# SAVED ANALYSIS HISTORY
# ============================================================

st.divider()

st.header("💾 Saved Analysis History")

history = get_analysis_history()


if history:

    for record in history:

        resume_name = record[1]
        resume_score = record[2]
        skills_found = record[3]
        job_match = record[4]
        missing = record[5]

        with st.expander(
            f"📄 {resume_name}"
        ):

            st.write(
                f"**Resume Score:** {resume_score}/100"
            )

            st.write(
                f"**Job Match:** {job_match}%"
            )

            st.write(
                f"**Skills:** {skills_found}"
            )

            st.write(
                f"**Missing Skills:** {missing}"
            )

else:

    st.info(
        "No saved analysis yet."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 AI Career & Placement Assistant | "
    "Python + Streamlit + SQLite"
)    
    
