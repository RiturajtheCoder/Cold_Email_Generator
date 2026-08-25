import streamlit as st

from src.analyzer import analyze_personalization
from src.email_generator import generate_email_bundle
from src.gemini_client import get_api_status, get_client, is_api_key_configured
from src.prompts import EMAIL_TONE_OPTIONS, EMAIL_LENGTH_OPTIONS
from src.url_state import apply_query_params, build_shareable_query_params
from src.utils import (
    copy_button_html,
    format_word_count,
    init_session_state,
    safe_truncate,
)


st.set_page_config(
    page_title="ColdMail AI",
    page_icon="📨",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            background: #07111f !important;
        }
        .stApp {
            background: linear-gradient(180deg, #08111f 0%, #0d1728 55%, #08111f 100%);
            color: #e5eefc;
        }
        [data-testid="stAppViewContainer"] > .main {
            background: linear-gradient(180deg, #08111f 0%, #0d1728 55%, #08111f 100%);
        }
        section[data-testid="stSidebar"] {
            background: #07111f;
            color: white;
        }
        .hero-card, .panel-card {
            background: rgba(8, 17, 31, 0.92);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 30px rgba(2, 6, 23, 0.35);
        }
        .hero-title {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0;
            color: #f8fbff;
        }
        .hero-subtitle {
            margin-top: 0.35rem;
            color: rgba(226, 232, 240, 0.9);
            font-size: 1rem;
        }
        .muted {
            color: #64748b;
        }
        .section-title {
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
            color: #f8fbff;
        }
        .small-note {
            font-size: 0.88rem;
            color: #64748b;
        }
        .email-box {
            background: #050b16;
            color: #e2e8f0;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            border: 1px solid rgba(255,255,255,0.08);
            white-space: pre-wrap;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            line-height: 1.6;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
            background-color: #232634 !important;
            color: #f8fafc !important;
            border-color: rgba(148, 163, 184, 0.25) !important;
        }
        .stTextInput label, .stTextArea label, .stSelectbox label, label {
            color: #f8fbff !important;
            font-weight: 600 !important;
        }
        [data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 14px;
            padding: 0.65rem 0.8rem;
        }
        [data-testid="stExpander"] {
            background: rgba(8, 17, 31, 0.88);
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.12);
        }
        .stDataFrame, [data-testid="stTable"] {
            background: rgba(8, 17, 31, 0.92) !important;
        }
        .copy-btn {
            padding: 0.55rem 0.9rem;
            border-radius: 10px;
            border: 1px solid rgba(148, 163, 184, 0.25);
            background: #111827;
            color: #f8fafc;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar() -> None:
    st.sidebar.markdown("## ColdMail AI")
    st.sidebar.caption("AI-powered personalized networking assistant")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.write(
        "Generate recruiter-friendly cold emails from your background, target company, and role."
    )
    st.sidebar.markdown("### How it works")
    st.sidebar.write("1. Fill the form\n2. Submit once\n3. Review analysis, email, and shareable URL")
    st.sidebar.markdown("### Settings")
    st.sidebar.write(f"API configured: {'Yes' if is_api_key_configured() else 'No'}")
    #st.sidebar.write(f"API status: {get_api_status()}")
    st.sidebar.caption("Sensitive candidate data is never added to the shareable URL.")


def render_metrics(scores: dict, word_count: int) -> None:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Personalization Score", f"{scores['personalization_score']}%")
    c2.metric("Job Match Score", f"{scores['job_match_score']}%")
    c3.metric("Keyword Coverage", f"{scores['covered_keywords']}/{scores['total_keywords']}")
    c4.metric("Email Word Count", format_word_count(word_count))


def run_generation(candidate: dict, target: dict, mode: str = "default") -> None:
    client = get_client()
    analysis = analyze_personalization(candidate, target)
    bundle = generate_email_bundle(client, candidate, target, analysis, mode=mode)
    st.session_state.analysis = analysis
    st.session_state.generated_email = bundle["email"]
    st.session_state.subject_lines = bundle["subject_lines"]
    st.session_state.generated_data = bundle
    st.session_state.generation_history.insert(
        0,
        {
            "timestamp": bundle["timestamp"],
            "company": target["company"],
            "role": target["role"],
            "tone": target["tone"],
            "personalization_score": analysis["personalization_score"],
            "subject": bundle["subject_lines"][0] if bundle["subject_lines"] else "",
        },
    )


def main() -> None:
    init_session_state()
    inject_css()
    sidebar()
    apply_query_params(st.session_state)

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">ColdMail AI</div>
            <div class="hero-subtitle">AI-Powered Personalized Networking Assistant for internships and entry-level outreach.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    if not is_api_key_configured():
        st.warning(
            "Gemini API key is not configured yet. You can still explore the UI, but generation will require a valid key."
        )

    col_left, col_right = st.columns([1.25, 0.75], gap="large")
    with col_left:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Candidate Profile</div>', unsafe_allow_html=True)
        with st.form("coldmail_form", clear_on_submit=False):
            c1, c2 = st.columns(2)
            with c1:
                candidate_name = st.text_input("Candidate name", value=st.session_state.candidate.get("name", ""))
                email = st.text_input("Email address", value=st.session_state.candidate.get("email", ""))
                phone = st.text_input("Phone number (optional)", value=st.session_state.candidate.get("phone", ""))
                education = st.text_input("Current degree / education", value=st.session_state.candidate.get("education", ""))
                college = st.text_input("College / university", value=st.session_state.candidate.get("college", ""))
                graduation_year = st.text_input("Graduation year", value=st.session_state.candidate.get("graduation_year", ""))
            with c2:
                github_url = st.text_input("GitHub URL (optional)", value=st.session_state.candidate.get("github_url", ""))
                linkedin_url = st.text_input("LinkedIn URL (optional)", value=st.session_state.candidate.get("linkedin_url", ""))
                portfolio_url = st.text_input("Portfolio URL (optional)", value=st.session_state.candidate.get("portfolio_url", ""))
                technical_skills = st.text_area(
                    "Technical skills (comma separated or one per line)",
                    value=st.session_state.candidate.get("technical_skills", ""),
                    height=110,
                )
                soft_skills = st.text_area(
                    "Soft skills (comma separated or one per line)",
                    value=st.session_state.candidate.get("soft_skills", ""),
                    height=110,
                )
            projects = st.text_area("Projects", value=st.session_state.candidate.get("projects", ""), height=120)
            internships = st.text_area(
                "Previous internships / experience",
                value=st.session_state.candidate.get("internships", ""),
                height=120,
            )

            st.markdown('<div class="section-title">Target Opportunity</div>', unsafe_allow_html=True)
            t1, t2 = st.columns(2)
            with t1:
                company = st.text_input("Company name", value=st.session_state.target.get("company", ""))
                role = st.text_input("Target role", value=st.session_state.target.get("role", ""))
                recruiter_name = st.text_input(
                    "Recruiter / hiring manager name (optional)",
                    value=st.session_state.target.get("recruiter_name", ""),
                )
            with t2:
                tone = st.selectbox("Preferred email tone", EMAIL_TONE_OPTIONS, index=EMAIL_TONE_OPTIONS.index(st.session_state.target.get("tone", EMAIL_TONE_OPTIONS[0])) if st.session_state.target.get("tone", EMAIL_TONE_OPTIONS[0]) in EMAIL_TONE_OPTIONS else 0)
                length = st.selectbox("Email length", EMAIL_LENGTH_OPTIONS, index=EMAIL_LENGTH_OPTIONS.index(st.session_state.target.get("length", EMAIL_LENGTH_OPTIONS[1])) if st.session_state.target.get("length", EMAIL_LENGTH_OPTIONS[1]) in EMAIL_LENGTH_OPTIONS else 1)
            job_description = st.text_area(
                "Job description (optional but recommended)",
                value=st.session_state.target.get("job_description", ""),
                height=140,
            )
            reason_interest = st.text_area(
                "Why are you interested in the company?",
                value=st.session_state.target.get("reason_interest", ""),
                height=100,
            )
            admired_item = st.text_input(
                "Specific company/project/product you admire",
                value=st.session_state.target.get("admired_item", ""),
            )

            submit = st.form_submit_button("Generate Cold Email")

        st.markdown("</div>", unsafe_allow_html=True)

        if submit:
            candidate = {
                "name": candidate_name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "education": education.strip(),
                "college": college.strip(),
                "graduation_year": graduation_year.strip(),
                "technical_skills": technical_skills.strip(),
                "soft_skills": soft_skills.strip(),
                "projects": projects.strip(),
                "internships": internships.strip(),
                "github_url": github_url.strip(),
                "linkedin_url": linkedin_url.strip(),
                "portfolio_url": portfolio_url.strip(),
            }
            target = {
                "company": company.strip(),
                "role": role.strip(),
                "recruiter_name": recruiter_name.strip(),
                "job_description": job_description.strip(),
                "reason_interest": reason_interest.strip(),
                "admired_item": admired_item.strip(),
                "tone": tone,
                "length": length,
            }

            if not candidate["name"] or not candidate["email"]:
                st.error("Please enter at least your name and email address.")
                st.stop()
            if not target["company"] or not target["role"]:
                st.error("Please enter both company name and target role.")
                st.stop()

            st.session_state.candidate = candidate
            st.session_state.target = target
            st.session_state.query_params = {
                "company": target["company"],
                "role": target["role"],
                "tone": target["tone"],
                "length": target["length"],
            }

            try:
                run_generation(candidate, target)
            except Exception as exc:
                st.error(f"Generation failed: {exc}")

    with col_right:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Shareable Link</div>', unsafe_allow_html=True)
        st.caption("Only non-sensitive fields like company, role, tone, and length are added to the URL.")
        if st.button("Generate Shareable Link"):
            query = build_shareable_query_params(st.session_state)
            st.session_state.shareable_link = query
        if st.session_state.shareable_link:
            st.code(st.session_state.shareable_link, language="text")
        #st.markdown("### API Status")
        #st.info(get_api_status())
        st.markdown("### Current Context")
        st.write(f"Company: {safe_truncate(st.session_state.target.get('company', ''))}")
        st.write(f"Role: {safe_truncate(st.session_state.target.get('role', ''))}")
        st.write(f"Tone: {st.session_state.target.get('tone', '')}")
        st.write(f"Length: {st.session_state.target.get('length', '')}")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.generated_email and st.session_state.analysis:
        st.write("")
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown("## AI Analysis")
        render_metrics(st.session_state.analysis, st.session_state.analysis.get("email_word_count", 0))
        st.progress(st.session_state.analysis["personalization_score"] / 100)

        analysis_df = st.session_state.analysis["keyword_df"]
        st.dataframe(analysis_df, use_container_width=True, hide_index=True)

        st.markdown("## Generated Email")
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.subheader("Subject Options")
            for subject in st.session_state.subject_lines:
                st.write(f"- {subject}")
        with col_b:
            st.subheader("Actions")
            if st.button("Regenerate"):
                try:
                    run_generation(st.session_state.candidate, st.session_state.target, mode="regenerate")
                    st.success("Regenerated a fresh version.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not regenerate: {exc}")
            if st.button("Make Shorter"):
                try:
                    run_generation(st.session_state.candidate, st.session_state.target, mode="shorter")
                    st.success("Generated a shorter version.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not shorten: {exc}")
            if st.button("Make More Professional"):
                try:
                    run_generation(st.session_state.candidate, st.session_state.target, mode="professional")
                    st.success("Generated a more professional version.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not revise tone: {exc}")
            if st.button("Improve Personalization"):
                try:
                    run_generation(st.session_state.candidate, st.session_state.target, mode="personalized")
                    st.success("Improved personalization.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not improve personalization: {exc}")
            st.markdown(copy_button_html(st.session_state.generated_email), unsafe_allow_html=True)

        st.markdown(f"<div class='email-box'>{st.session_state.generated_email}</div>", unsafe_allow_html=True)

        st.expander("Why this email works", expanded=False).write(st.session_state.analysis["why_this_works"])
        st.expander("Missing information", expanded=False).write(st.session_state.analysis["missing_information"])
        st.expander("Matching skills", expanded=False).write(", ".join(st.session_state.analysis["matching_skills"]) or "None detected")
        st.expander("Matching projects", expanded=False).write(", ".join(st.session_state.analysis["matching_projects"]) or "None detected")
        st.expander("Suggested improvements", expanded=False).write(st.session_state.analysis["suggested_improvements"])
        st.expander("AI recruiter perspective", expanded=False).write(st.session_state.analysis["recruiter_perspective"])
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Generation History", expanded=False):
        if st.session_state.generation_history:
            st.dataframe(st.session_state.generation_history, use_container_width=True, hide_index=True)
        else:
            st.write("No generations yet in this session.")

    st.caption("Made by Rituraj")


if __name__ == "__main__":
    main()
