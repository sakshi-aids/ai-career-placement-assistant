import sqlite3


def create_database():

    conn = sqlite3.connect("career_assistant.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            resume_score INTEGER,
            detected_skills TEXT,
            job_match INTEGER,
            missing_skills TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(
    resume_name,
    resume_score,
    detected_skills,
    job_match,
    missing_skills
):

    conn = sqlite3.connect("career_assistant.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resume_analysis
        (
            resume_name,
            resume_score,
            detected_skills,
            job_match,
            missing_skills
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        resume_name,
        resume_score,
        ", ".join(detected_skills),
        job_match,
        ", ".join(missing_skills)
    ))

    conn.commit()
    conn.close()


def get_analysis_history():

    conn = sqlite3.connect("career_assistant.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM resume_analysis
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data