# 📄 Resume Matcher & Optimizer

An AI-powered resume analysis tool built with Python, Streamlit, and Google Gemini.

---

## Features

- **Dual scoring** — TF-IDF cosine similarity + Gemini LLM contextual scoring
- **Skill gap analysis** — matched, missing, and additional skills detection
- **AI improvement suggestions** — actionable rewording and restructuring tips
- **Cover letter talking points** — role-specific bullet points
- **Score simulation** — projected score after adding missing skills
- **PDF / DOCX / TXT** resume upload support
- **Interactive charts** — gauges, bar charts, skill tags

---

## Project Structure

```
resume_matcher/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── utils/
│   ├── nlp_utils.py           # TF-IDF scoring, skill extraction, preprocessing
│   ├── file_parser.py         # PDF, DOCX, TXT parsing
│   └── gemini_utils.py        # Google Gemini API integration
└── components/
    └── charts.py              # Plotly charts and UI components
```

---

## Quick Start

### 1. Clone / download the project

```bash
cd resume_matcher
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a Gemini API key (free)

1. Go to [https://aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API key** → **Create API key**
4. Copy the key (starts with `AIza...`)

> The app works without a Gemini key — TF-IDF scoring and skill analysis run locally. The Gemini key unlocks AI scoring, improvement suggestions, and cover letter points.

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## How to Use

1. **Sidebar** → Paste your Gemini API key
2. **Upload** your resume (PDF, DOCX, or TXT) or paste the text directly
3. **Paste** the job description you're targeting
4. Click **Analyze Resume**
5. Explore the four result tabs:
   - **Scores** — gauge charts + Gemini summary
   - **Skills** — matched vs missing skill breakdown
   - **AI Insights** — strengths, gaps, improvement suggestions
   - **Cover Letter Points** — tailored talking points

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| NLP baseline | scikit-learn TF-IDF + cosine similarity |
| AI analysis | Google Gemini 2.5 Flash |
| PDF parsing | PyPDF2 |
| DOCX parsing | python-docx |
| Charts | Plotly |
| Text processing | NLTK |

---

## Customization

**Add more skills** — Edit `TECH_SKILLS` set in `utils/nlp_utils.py`

**Change the Gemini model** — Update `"gemini-2.5-flash"` to `"gemini-1.5-pro"` in `utils/gemini_utils.py` for deeper analysis (uses more quota)

**Adjust suggestion prompts** — Edit the prompts in `utils/gemini_utils.py` to tailor output style

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| PDF shows garbled text | Try copy-pasting text into the "Paste text" tab instead |
| Gemini API error 429 | Free tier rate limit hit — wait a minute and retry |
| NLTK resource error | Run `python -c "import nltk; nltk.download('all')"` |

---

## License

MIT — free to use and modify.
