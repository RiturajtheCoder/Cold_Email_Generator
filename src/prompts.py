EMAIL_TONE_OPTIONS = ["Professional", "Friendly", "Confident", "Concise", "Enthusiastic"]
EMAIL_LENGTH_OPTIONS = ["Short", "Medium", "Detailed"]


def build_generation_prompt(candidate: dict, target: dict, analysis: dict, mode: str = "default") -> str:
    return f"""
You are an expert technical recruiter, professional networking strategist, and cold-email copywriter specializing in personalized internship and entry-level outreach.

Write a recruiter-ready networking email. Do not act like a chatbot.

Hard rules:
- Do not invent achievements, company facts, recruiter names, or experience.
- Do not use generic filler, spammy language, buzzwords, or excessive flattery.
- Do not make the introduction long.
- Use only the facts provided.
- If something is missing, skip it gracefully.

Candidate context:
Name: {candidate.get("name", "")}
Email: {candidate.get("email", "")}
Education: {candidate.get("education", "")}
College: {candidate.get("college", "")}
Graduation year: {candidate.get("graduation_year", "")}
Technical skills: {candidate.get("technical_skills", "")}
Soft skills: {candidate.get("soft_skills", "")}
Projects: {candidate.get("projects", "")}
Internships/experience: {candidate.get("internships", "")}
GitHub: {candidate.get("github_url", "")}
LinkedIn: {candidate.get("linkedin_url", "")}
Portfolio: {candidate.get("portfolio_url", "")}

Target context:
Company: {target.get("company", "")}
Role: {target.get("role", "")}
Recruiter/Hiring manager: {target.get("recruiter_name", "")}
Job description: {target.get("job_description", "")}
Reason for interest: {target.get("reason_interest", "")}
Admired company/project/product: {target.get("admired_item", "")}
Tone: {target.get("tone", "")}
Length: {target.get("length", "")}
Mode: {mode}

Analysis signals:
Relevant skills: {analysis.get("matching_skills", [])}
Relevant projects: {analysis.get("matching_projects", [])}
Missing info: {analysis.get("missing_information", "")}
Keywords: {analysis.get("keywords", [])}

Output format exactly:
Subject options:
1. ...
2. ...
3. ...

Email:
...
"""
