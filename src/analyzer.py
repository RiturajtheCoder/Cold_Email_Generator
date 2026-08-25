from __future__ import annotations

import re
from collections import Counter

import pandas as pd

COMMON_SKILLS = [
    "python",
    "sql",
    "aws",
    "git",
    "github",
    "docker",
    "linux",
    "streamlit",
    "pandas",
    "numpy",
    "flask",
    "fastapi",
    "machine learning",
    "data analysis",
    "html",
    "css",
    "javascript",
    "java",
    "c++",
    "mongodb",
]


def _normalize(text: str) -> str:
    return (text or "").lower()


def _split_items(text: str) -> list[str]:
    if not text:
        return []
    parts = re.split(r"[\n,;•|]+", text)
    return [p.strip() for p in parts if p.strip()]


def analyze_personalization(candidate: dict, target: dict) -> dict:
    resume_text = " ".join(
        [
            candidate.get("technical_skills", ""),
            candidate.get("soft_skills", ""),
            candidate.get("projects", ""),
            candidate.get("internships", ""),
            candidate.get("education", ""),
            candidate.get("college", ""),
        ]
    )
    jd_text = target.get("job_description", "") or ""
    combined = _normalize(resume_text)
    jd = _normalize(jd_text)

    rows = []
    for kw in COMMON_SKILLS:
        found_resume = kw in combined
        found_jd = kw in jd
        rows.append(
            {
                "Keyword": kw.title() if kw != "c++" else "C++",
                "Found in Resume": "Yes" if found_resume else "No",
                "Found in JD": "Yes" if found_jd else "No",
                "Match": "Yes" if found_resume and found_jd else "No",
            }
        )
    df = pd.DataFrame(rows)

    matching_skills = df.loc[df["Match"] == "Yes", "Keyword"].tolist()
    relevant_skills = df.loc[(df["Found in Resume"] == "Yes") & (df["Found in JD"] == "Yes"), "Keyword"].tolist()
    keywords_in_jd = [kw for kw in COMMON_SKILLS if kw in jd] if jd else []
    covered_keywords = len([kw for kw in keywords_in_jd if kw in combined]) if keywords_in_jd else len(matching_skills)
    total_keywords = max(len(keywords_in_jd), 1) if jd else max(len(matching_skills), 1)
    keyword_coverage = int(round((covered_keywords / total_keywords) * 100))
    job_match = int(round(min(100, (len(relevant_skills) / max(len(keywords_in_jd), 1)) * 100))) if jd else min(100, len(matching_skills) * 12)

    projects = _split_items(candidate.get("projects", ""))
    matched_projects = []
    for project in projects:
        project_tokens = set(re.findall(r"[a-zA-Z0-9#+.-]+", project.lower()))
        if any(skill.lower() in project_tokens or skill.lower() in project.lower() for skill in relevant_skills):
            matched_projects.append(project)

    missing_information = []
    if not candidate.get("github_url"):
        missing_information.append("GitHub URL not provided")
    if not candidate.get("linkedin_url"):
        missing_information.append("LinkedIn URL not provided")
    if not target.get("job_description"):
        missing_information.append("Job description not provided")
    if not target.get("recruiter_name"):
        missing_information.append("Recruiter name not provided")
    if not candidate.get("projects"):
        missing_information.append("Projects not provided")

    personalization_score = min(100, int(round((job_match * 0.55) + (keyword_coverage * 0.35) + (min(len(matched_projects), 3) * 5))))
    email_word_count = 0

    return {
        "keyword_df": df,
        "matching_skills": relevant_skills,
        "matching_projects": matched_projects,
        "missing_information": ", ".join(missing_information) if missing_information else "No major missing items detected.",
        "suggested_improvements": "Add a stronger company-specific hook and one measurable project result if available.",
        "why_this_works": "The email stays concise, uses only verified inputs, and links the candidate's background to the target role.",
        "recruiter_perspective": "A recruiter would value the directness, relevance, and lack of exaggerated claims.",
        "keywords": keywords_in_jd,
        "covered_keywords": covered_keywords,
        "total_keywords": total_keywords,
        "keyword_coverage": keyword_coverage,
        "job_match_score": job_match,
        "personalization_score": personalization_score,
        "email_word_count": email_word_count,
    }
