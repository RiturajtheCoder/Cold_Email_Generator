# Architecture

```mermaid
flowchart TD
    U[User] --> UI[Streamlit UI]
    UI --> F[Input / Form Layer]
    F --> V[Validation]
    V --> P[Prompt Engineering Layer]
    P --> G[Gemini API]
    G --> A[AI Analysis]
    A --> PE[Personalization Engine]
    PE --> E[Email Generation]
    E --> O[Visualization / Output]
    O --> S[Shareable URL State]

    A --> D[Pandas Keyword Analysis]
    D --> PE
```

## Notes

- The app is a single Streamlit project with a small modular `src/` package.
- Pandas is used for the keyword match table and scoring support.
- Shareable URL state only stores non-sensitive target settings such as company, role, tone, and length.
