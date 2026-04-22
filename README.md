# 📄 Resume Matcher & Optimizer
An AI-powered resume analysis and rewriting tool built with Python, Streamlit, and Google Gemini.

## ✨ Features
* **Dual Scoring** — TF-IDF cosine similarity + Gemini LLM contextual scoring.
* **Skill Gap Analysis** — Matched, missing, and additional skills detection.
* **AI Insights & Suggestions** — Actionable rewording, formatting, and restructuring tips.
* **Cover Letter Talking Points** — Tailored, role-specific bullet points to stand out.
* **Score Simulation** — Projected ATS score boost after addressing missing skills.
* **🚀 AI Resume Re-Optimizer (Pro)** — Intelligently rewrites your targeted resume to adapt specifically to the Job Description.
* **📥 PDF Generator** — Automatically formats and downloads the newly optimized resume as a clean, ATS-compliant PDF document.
* **Interactive Dashboard** — Gorgeous Streamlit interface with Plotly gauges, skill tags, and bar charts.

## 📁 Project Structure
```text
resume_matcher/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── utils/
│   ├── nlp_utils.py           # TF-IDF scoring, skill extraction, preprocessing
│   ├── file_parser.py         # PDF, DOCX, TXT parsing
│   ├── gemini_utils.py        # Google Gemini API AI analysis & cache integration
│   ├── resume_rewriter.py     # AI logic for fully rewriting the resume
│   └── pdf_generator.py       # fpdf engine for exporting clean resume PDFs
└── components/
    ├── dashboard.py           # UI layouts and interface building blocks
    └── charts.py              # Plotly charts and visual components
```

## 🚀 Quick Start
**1. Clone / download the project**
```bash
git clone https://github.com/muralimadevan82-source/ai-resume-matcher.git
cd resume_matcher
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Get a Gemini API key (free)**
* Go to [Google AI Studio](https://aistudio.google.com)
* Sign in with your Google account
* Click **Get API key** → **Create API key**
* Copy the key (starts with *AIza...*)

> *Note: The app works without a Gemini key for basic TF-IDF scoring and skill analysis natively. A Gemini key unlocks advanced AI scoring, improvement suggestions, cover letter points, and the Resume Optimizer.*

**5. Run the app**
```bash
streamlit run app.py
```
*The app opens at http://localhost:8501 in your browser.*

## 📖 How to Use
1. **Sidebar** → Paste your Google Gemini API key.
2. **Upload** your resume (PDF, DOCX, or TXT) or paste the text directly.
3. **Paste** the target Job Description (JD).
4. **Click** *Analyze Resume*.
5. **Explore** the four result tabs:
   * **Scores** — Gauge charts + Gemini summary
   * **Skills** — Matched vs missing skill breakdown
   * **AI Insights** — Strengths, gaps, improvement suggestions
   * **Cover Letter Points** — Tailored talking points
6. **Rewrite** — Scroll down to the PRO section and generate an ATS-Optimized PDF tailored perfectly to your Job Description!

## ⚙️ Tech Stack
| Layer | Technology |
|---|---|
| **UI** | Streamlit |
| **NLP baseline** | scikit-learn TF-IDF + cosine similarity |
| **AI Analysis & Rewriting** | Google Gemini 2.5 Flash |
| **PDF Formatting / Generation** | fpdf |
| **PDF/Word Parsing** | PyPDF2, python-docx |
| **Charts** | Plotly |
| **Text processing** | NLTK |

## 🛠 Troubleshooting
| Issue | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| PDF shows garbled text | Try copy-pasting text into the "Paste text" tab instead |
| **Gemini API error 429** | Built-in Streamlit cache now mitigates this! But if limit is hit, wait ~30s and click again. |
| PDF Gen: `Invalid bytearray` | Upgraded. Re-pull the latest codebase. |
| NLTK resource error | Run `python -c "import nltk; nltk.download('all')"` |
