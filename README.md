# ColdMail AI

AI-powered personalized networking assistant for internship and entry-level outreach.

## Features

- Recruiter-style cold email generation
- Personalized subject line options
- Personalization, job-match, and keyword-coverage scores
- Pandas-based keyword analysis table
- Session-state history for the current session
- Safe error handling and fallback generation
- Streamlit-ready UI with metrics, expanders, and a dashboard layout

## Tech Stack

- Python 3.11+
- Streamlit
- Google Gemini API
- Pandas

## Architecture

See [docs/architecture.md](docs/architecture.md) for the Mermaid diagram and data flow.

## How It Works

1. Enter candidate details and the target company/role.
2. Submit the form.
3. The app analyzes keyword overlap and personalization strength.
4. Gemini generates a concise, personalized outreach email.
5. Review the metrics and email.

## Gemini Integration

The app uses Gemini as the core generation engine. A strong prompt instructs the model to behave like an expert recruiter and cold-email copywriter, while preventing hallucinated facts and spammy wording.

## Prompt Engineering

- System-style recruiter persona
- Dynamic context injection with candidate and target inputs
- Anti-hallucination rules
- Structured subject + email output
- Short, polished, recruiter-friendly tone

## Installation

```bash
git clone <repository-url>
cd coldmail-ai
pip install -r requirements.txt
streamlit run app.py
```

## Environment Variables

Create a `.env` file:

```bash
GEMINI_API_KEY=your_api_key_here
```

For Streamlit Community Cloud, add `GEMINI_API_KEY` in app secrets instead of using `.env`.

## How to Add Your Own Gemini API Key

1. Get a Gemini API key from Google AI Studio.
2. Create a `.env` file in the project root.
3. Add:

```bash
GEMINI_API_KEY=your_api_key_here
```

4. Restart Streamlit.

If deploying on Streamlit Cloud, open the app settings and add the same key in Secrets as:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

## Deployment

Deploy on Streamlit Community Cloud by connecting the GitHub repository, setting secrets, and using `streamlit run app.py` as the entry point.

**Live Demo:** [ADD LIVE URL AFTER DEPLOYMENT]

## Screenshots

- Add screenshots here after deployment.

## Future Improvements

- Multiple email templates
- Better JD parsing
- Export to PDF
- CSV batch generation
- More detailed analytics
