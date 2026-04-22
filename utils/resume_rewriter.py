import google.generativeai as genai
import streamlit as st

@st.cache_data(show_spinner=False)
def rewrite_resume_logic(resume_text, job_description, api_key):
    """
    Uses Gemini to rewrite the resume text to match a job description.
    Even if the resume is unrelated, it attempts to extract transferable skills.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
You are a professional ATS Resume Consultant specializing in career pivots and resume optimization.

Your task is to rewrite the provided RESUME to perfectly match the JOB DESCRIPTION.

STRATEGY:
1. If the resume is unrelated, identify transferable skills (e.g., leadership, problem-solving, specific tools) and map them to the JD.
2. Focus on impact and quantitative results (invent realistic but plausible metrics if necessary for a fresher).
3. Use high-impact ATS keywords from the JD.
4. Ensure the tone is professional, confident, and achievement-oriented.
5. Structure the output clearly for easy parsing into a PDF.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

OUTPUT STRUCTURE:
- [FULL_NAME] (Leave placeholder if not found)
- [CONTACT_INFO] (Leave placeholder if not found)
- PROFESSIONAL SUMMARY: (3-4 sentences high-impact)
- TECHNICAL SKILLS: (Categorized, e.g., Languages, Frameworks, Tools)
- PROFESSIONAL EXPERIENCE / PROJECTS: (3-4 bullet points per item, starting with strong action verbs)
- EDUCATION: (Formatted cleanly)
- CERTIFICATIONS & AWARDS: (If applicable)

IMPORTANT: Provide only the plain text content for the new resume. Use clear headings.
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error rewriting resume: {str(e)}"
