# Technical Design

## 1. Problem Statement

Build an AI-powered Streamlit application that generates personalized cold emails for recruiters using company and role context.

## 2. Objectives

- Generate recruiter-style networking emails.
- Keep the UX polished and easy to use.
- Support shareable URLs for non-sensitive target settings.
- Avoid hallucinations and preserve user-provided facts.

## 3. System Architecture

- `app.py` drives the Streamlit UI.
- `src/gemini_client.py` manages API configuration.
- `src/prompts.py` constructs specialized prompts.
- `src/analyzer.py` computes keyword matches and personalization scores.
- `src/email_generator.py` handles Gemini output and fallback generation.
- `src/url_state.py` manages query parameters.
- `src/utils.py` handles session defaults and small UI helpers.

## 4. Data Flow

User input -> validation -> analysis -> prompt construction -> Gemini generation -> parsing -> metrics -> history/output.

## 5. Streamlit UI Architecture

- Main input form
- KPI metrics row
- Keyword analysis table
- Generated email panel
- Expanders for explanations
- History section

## 6. Gemini API Integration

The app uses the official `google-genai` SDK and calls Gemini only after form submission.

## 7. Prompt Engineering Strategy

- Recruiter/copywriter persona
- Dynamic candidate and target context
- Anti-hallucination constraints
- Structured output format
- Mode-based refinements for regeneration

## 8. Personalization Algorithm

- Match resume text and job description against a common skill keyword list.
- Compute keyword coverage, job match, and a combined personalization score.
- Detect relevant projects when they mention matched skills.

## 9. Keyword Analysis

Pandas stores the match table with columns for resume presence, JD presence, and overlap.

## 10. Session-State Management

Session state keeps candidate data, target data, generated output, scores, and generation history.

## 11. Query Parameter Strategy

Only safe, non-sensitive fields are written to `st.query_params`:

- company
- role
- tone
- length

## 12. Error Handling

The app shows friendly Streamlit messages for missing keys, invalid inputs, API errors, and malformed model output.

## 13. Security

- API key is never hardcoded.
- Local secrets use `.env`.
- Streamlit Cloud secrets use `st.secrets`.
- Candidate personal data is not placed into the URL.

## 14. Deployment Architecture

The project is ready for Streamlit Community Cloud with a minimal dependency set and environment-based configuration.
