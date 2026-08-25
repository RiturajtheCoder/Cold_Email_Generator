from __future__ import annotations

import re
from datetime import datetime

from src.prompts import build_generation_prompt


def _fallback_email(candidate: dict, target: dict, analysis: dict) -> dict:
    name = candidate.get("name", "there")
    company = target.get("company", "your team")
    role = target.get("role", "the role")
    intro_skill = (analysis.get("matching_skills") or [None])[0]
    skill_text = f"I've built experience around {intro_skill.lower()}." if intro_skill else "I’d love to bring my background and projects to the role."
    subject_lines = [
        f"Interest in {role} at {company} - {name}",
        f"{name} | {role} Application Interest",
        f"Exploring {role} Opportunities at {company}",
    ]
    email = (
        f"Hi {target.get('recruiter_name') or 'Hiring Team'},\n\n"
        f"My name is {name}, and I’m reaching out about the {role} opportunity at {company}. "
        f"{skill_text} {candidate.get('reason_interest') or 'I am especially interested in this opportunity because it aligns with my background and goals.'}\n\n"
        f"My relevant background includes {candidate.get('technical_skills') or 'technical skills'} and work on {candidate.get('projects') or 'projects'}.\n\n"
        f"If my background is a fit, I’d appreciate the chance to connect briefly.\n\n"
        f"Best regards,\n{name}\n{candidate.get('email', '')}"
    )
    return {
        "subject_lines": subject_lines,
        "email": email,
        "raw_text": email,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mode": "fallback",
    }


def _parse_response(text: str) -> tuple[list[str], str]:
    subject_lines = []
    body = text.strip()
    subject_match = re.search(r"Subject options:\s*(.+?)\n\nEmail:\s*(.+)", body, flags=re.I | re.S)
    if subject_match:
        subj_block = subject_match.group(1)
        body = subject_match.group(2).strip()
        for line in subj_block.splitlines():
            line = line.strip("-• \t")
            line = re.sub(r"^\d+\.\s*", "", line)
            if line:
                subject_lines.append(line)
    return subject_lines[:3], body


def generate_email_bundle(client, candidate: dict, target: dict, analysis: dict, mode: str = "default") -> dict:
    prompt = build_generation_prompt(candidate, target, analysis, mode=mode)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        text = getattr(response, "text", "") or ""
        if not text:
            raise ValueError("Gemini returned an empty response.")
        subjects, email = _parse_response(text)
        if not subjects:
            subjects = [
                f"Interest in {target.get('role', 'the role')} at {target.get('company', 'the company')}",
                f"{candidate.get('name', 'Candidate')} | {target.get('role', 'Role')} Interest",
                f"Exploring Opportunities at {target.get('company', 'the company')}",
            ]
        word_count = len(email.split())
        analysis["email_word_count"] = word_count
        return {
            "subject_lines": subjects,
            "email": email,
            "raw_text": text,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "mode": mode,
        }
    except Exception:
        bundle = _fallback_email(candidate, target, analysis)
        analysis["email_word_count"] = len(bundle["email"].split())
        return bundle
