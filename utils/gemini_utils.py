import google.generativeai as genai
import streamlit as st


def init_gemini(api_key: str):
    """Configure Gemini with the provided API key."""
    genai.configure(api_key=api_key)


@st.cache_data(show_spinner=False)
def get_gemini_match_score(resume_text: str, jd_text: str) -> dict:
    """Ask Gemini for a contextual match score and reasoning."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""You are an expert ATS (Applicant Tracking System) and career coach.

Analyze how well this resume matches the job description below.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{jd_text[:2000]}

Respond in this exact format (no markdown, plain text only):
SCORE: <number 0-100>
SUMMARY: <2-3 sentence overall assessment>
STRENGTHS: <bullet points of strong matches, one per line starting with ->
GAPS: <bullet points of key gaps, one per line starting with ->
"""
    try:
        response = model.generate_content(prompt)
        return _parse_gemini_response(response.text)
    except Exception as e:
        return {"error": str(e), "score": None}


@st.cache_data(show_spinner=False)
def get_improvement_suggestions(resume_text: str, jd_text: str, missing_skills: list) -> str:
    """Get actionable resume improvement suggestions from Gemini."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    missing_str = ", ".join(missing_skills[:15]) if missing_skills else "none identified"
    prompt = f"""You are an expert resume coach. Given the resume and job description below, provide specific, actionable improvements.

RESUME (excerpt):
{resume_text[:2500]}

JOB DESCRIPTION (excerpt):
{jd_text[:1500]}

MISSING SKILLS DETECTED: {missing_str}

Provide 5-7 specific, actionable suggestions to improve this resume for this role.
Format each suggestion as:
[SECTION] Action item — specific detail on what to add/change/remove.

Focus on: wording improvements, missing keywords, quantifying achievements, restructuring sections.
Do not use markdown headers or asterisks. Plain text only."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Could not generate suggestions: {e}"


@st.cache_data(show_spinner=False)
def get_cover_letter_points(resume_text: str, jd_text: str) -> str:
    """Generate key talking points for a cover letter."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""Based on the resume and job description, generate 4-5 compelling talking points for a cover letter.
Each point should connect a specific resume achievement to a job requirement.

RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{jd_text[:1500]}

Format as numbered points. Be specific and concise. Plain text only, no markdown."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Could not generate cover letter points: {e}"


@st.cache_data(show_spinner=False)
def get_recruiter_view(resume_text: str, jd_text: str) -> str:
    """Get the 'What Recruiter Sees' perspective from Gemini."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""You are a technical recruiter. Analyze the resume and job description.
    
    Tell me exactly what the recruiter sees and thinks.
    Your response MUST follow this exact structure (no markdown headings):
    
    👉 Not just code
    👉 They see:
    
    ✔ <Point 1: e.g. Problem solving>
    ✔ <Point 2: e.g. Resume improvement system>
    ✔ <Point 3: e.g. AI understanding>
    ✔ <Point 4: e.g. Visualization/Presentation skills>
    
    RESUME: {resume_text[:2000]}
    JD: {jd_text[:1500]}
    
    Only provide the bullet points using the 👉 and ✔ emojis. No other text."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Recruiter was unavailable: {e}"


def _parse_gemini_response(text: str) -> dict:
    """Parse structured Gemini response into a dict."""
    result = {"score": None, "summary": "", "strengths": [], "gaps": [], "raw": text}
    lines = text.strip().splitlines()
    current_section = None
    buffer = []

    for line in lines:
        line = line.strip()
        if line.startswith("SCORE:"):
            try:
                result["score"] = float(line.replace("SCORE:", "").strip())
            except ValueError:
                pass
        elif line.startswith("SUMMARY:"):
            result["summary"] = line.replace("SUMMARY:", "").strip()
            current_section = "summary"
        elif line.startswith("STRENGTHS:"):
            current_section = "strengths"
        elif line.startswith("GAPS:"):
            current_section = "gaps"
        elif line.startswith("->") and current_section in ("strengths", "gaps"):
            result[current_section].append(line[2:].strip())
        elif current_section == "summary" and line:
            result["summary"] += " " + line

    return result
