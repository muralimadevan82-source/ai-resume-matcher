import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from utils.file_parser import parse_uploaded_file
from utils.nlp_utils import (
    compute_tfidf_similarity,
    get_skill_analysis,
    simulate_score_boost,
)
from utils.gemini_utils import (
    init_gemini,
    get_gemini_match_score,
    get_improvement_suggestions,
    get_cover_letter_points,
    get_recruiter_view,
)
from utils.resume_rewriter import rewrite_resume_logic
from utils.pdf_generator import generate_resume_pdf
from components.dashboard import render_dashboard
from components.charts import (
    score_gauge,
    skill_bar_chart,
    score_comparison_chart,
    skill_tags,
    metric_card,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Optimizer Tool",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 40px; border-radius: 8px;
        background: #f1f5f9; color: #475569; font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background: #4f46e5 !important; color: white !important;
    }
    div[data-testid="stVerticalBlock"] > div { gap: 0.75rem; }
    .section-header {
        font-size: 15px; font-weight: 600; color: #0f172a;
        margin: 1rem 0 0.5rem; padding-bottom: 4px;
        border-bottom: 2px solid #e2e8f0;
    }
    .suggestion-box {
        background: #f8fafc; border-left: 3px solid #4f46e5;
        padding: 10px 14px; border-radius: 0 8px 8px 0;
        font-size: 14px; margin: 6px 0; color: #1e293b;
    }
    .strength-item { color: #166534; font-size: 14px; margin: 4px 0; }
    .gap-item { color: #991b1b; font-size: 14px; margin: 4px 0; }
    .info-box {
        background: #eff6ff; border: 1px solid #bfdbfe;
        border-radius: 10px; padding: 12px 16px;
        font-size: 14px; color: #1e40af;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/resume.png", width=60)
    st.markdown("## Resume Matcher")
    st.markdown("AI-powered resume analysis using **TF-IDF** and **Google Gemini**.")
    st.divider()

    st.markdown("### 🔑 Gemini API Key")
    api_key = st.text_input(
        "Enter your Gemini API key",
        type="password",
        placeholder="AIza...",
        help="Get your key at https://aistudio.google.com",
    )
    if api_key:
        init_gemini(api_key)
        st.success("API key set ✓")
    else:
        st.markdown(
            '<div class="info-box">Get a free API key at '
            '<a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("### ℹ️ How it works")
    st.markdown("""
1. Upload your resume (PDF/DOCX/TXT)
2. Paste the job description
3. Click **Analyze**
4. Get your match score, skill gaps & AI suggestions
""")
    st.divider()
    st.caption("Built with Python · Streamlit · Gemini · scikit-learn")


# ── Main layout ────────────────────────────────────────────────────────────────
st.markdown("# 🔥 AI Resume Optimizer Tool")
st.markdown("Go beyond basic matching. Analyze, optimize, and dominate the job market with AI-powered insights.")
st.divider()

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("### 📤 Your Resume")
    upload_tab, paste_tab = st.tabs(["Upload file", "Paste text"])
    with upload_tab:
        uploaded_file = st.file_uploader(
            "Upload PDF, DOCX, or TXT",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed",
        )
        resume_text = ""
        if uploaded_file:
            resume_text = parse_uploaded_file(uploaded_file)
            if resume_text and not resume_text.startswith("["):
                st.success(f"Parsed {len(resume_text):,} characters from {uploaded_file.name}")
                with st.expander("Preview extracted text"):
                    st.text(resume_text[:1500] + ("..." if len(resume_text) > 1500 else ""))
            else:
                st.error(resume_text)
    with paste_tab:
        resume_text_pasted = st.text_area(
            "Paste resume text",
            height=280,
            placeholder="Paste your full resume text here...",
            label_visibility="collapsed",
        )
        if resume_text_pasted.strip():
            resume_text = resume_text_pasted

with col_right:
    st.markdown("### 📋 Job Description")
    jd_text = st.text_area(
        "Paste the job description",
        height=320,
        placeholder="Paste the full job description here...",
        label_visibility="collapsed",
    )

st.divider()

# ── Analyze button ─────────────────────────────────────────────────────────────
col_btn, col_note = st.columns([1, 3])
with col_btn:
    analyze_btn = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)
with col_note:
    if not api_key:
        st.markdown(
            '<div class="info-box" style="margin-top:6px;">⚡ Add your Gemini API key in the sidebar for AI-powered analysis. '
            'TF-IDF scoring works without a key.</div>',
            unsafe_allow_html=True,
        )

# ── Results ────────────────────────────────────────────────────────────────────
if analyze_btn:
    st.session_state["analyzed"] = True
    st.session_state["resume_text_state"] = resume_text
    st.session_state["jd_text_state"] = jd_text

if st.session_state.get("analyzed", False):
    current_resume = st.session_state.get("resume_text_state", "")
    current_jd = st.session_state.get("jd_text_state", "")
    
    if not current_resume or not current_resume.strip():
        st.error("Please upload or paste your resume.")
    elif not current_jd or not current_jd.strip():
        st.error("Please paste a job description.")
    else:
        st.divider()
        
        with st.spinner("Computing alignment scores..."):
            skill_data = get_skill_analysis(current_resume, current_jd)
            
            # Use skill coverage as primary score
            primary_score = skill_data["coverage"]
            
            # Requested Hack: Advanced Match = Primary * 0.5
            advanced_score = primary_score * 0.5
            
            # Predict improvement with capped logic
            boosted_score = simulate_score_boost(primary_score, skill_data["missing"])

        gemini_data = None
        if api_key:
            with st.spinner("Running deep AI analysis..."):
                gemini_data = get_gemini_match_score(current_resume, current_jd)

        # ── Dashboard Output ──────────────────────────────────────────────────
        with st.spinner("Preparing your specialized optimization dashboard..."):
            recruiter_view = "Analysis pending..."
            if api_key:
                recruiter_view = get_recruiter_view(current_resume, current_jd)
            
            with st.spinner("Generating improvement suggestions..."):
                suggestions = get_improvement_suggestions(
                    current_resume, current_jd, list(skill_data["missing"])
                )

            render_dashboard(
                resume_text=current_resume,
                jd_text=current_jd,
                match_score=primary_score,
                tfidf_score=advanced_score,
                gemini_data=gemini_data,
                skill_data=skill_data,
                boosted_score=boosted_score,
                suggestions=suggestions,
                recruiter_view=recruiter_view
            )
            st.caption("⚠️ Scores are approximate and based on skill matching + NLP analysis. Professional optimization powered by Gemini 1.5 Flash.")

        st.divider()

        # ── Analytical Tabs (Secondary) ─────────────────────────────────────
        st.markdown("### 🔍 Detailed Analysis")
        tabs = st.tabs(["📈 Scores", "🛠 Skills", "🤖 AI Insights", "✍️ Cover Letter Points"])

        # Tab 1 — Scores
        with tabs[0]:
            g1, g2 = st.columns(2)
            with g1:
                score_gauge(advanced_score, "Advanced Match Score", "#6366f1")
            with g2:
                if gemini_data and gemini_data.get("score"):
                    score_gauge(gemini_data["score"], "Gemini Match Score", "#8b5cf6")
                else:
                    st.info("Add your Gemini API key to see the AI-based score.")

            if gemini_data and gemini_data.get("score"):
                st.markdown('<div class="section-header">Score Comparison</div>', unsafe_allow_html=True)
                score_comparison_chart(advanced_score, gemini_data["score"], boosted_score)

        # Tab 2 — Skills
        with tabs[1]:
            skill_bar_chart(skill_data["matched"], skill_data["missing"])

            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown('<div class="section-header">✅ Matched Skills</div>', unsafe_allow_html=True)
                skill_tags(skill_data["matched"], "green")
            with sc2:
                st.markdown('<div class="section-header">❌ Missing Skills</div>', unsafe_allow_html=True)
                skill_tags(skill_data["missing"], "red")
            with sc3:
                st.markdown('<div class="section-header">➕ Additional Skills</div>', unsafe_allow_html=True)
                skill_tags(skill_data["extra"], "blue")

        # Tab 3 — AI Insights
        with tabs[2]:
            if not api_key:
                st.info("Add your Gemini API key in the sidebar to unlock AI insights.")
            else:
                if gemini_data and (gemini_data.get("strengths") or gemini_data.get("gaps")):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown('<div class="section-header">💪 Strengths</div>', unsafe_allow_html=True)
                        for s in gemini_data.get("strengths", []):
                            st.markdown(f'<div class="strength-item">✅ {s}</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown('<div class="section-header">⚠️ Gaps</div>', unsafe_allow_html=True)
                        for g in gemini_data.get("gaps", []):
                            st.markdown(f'<div class="gap-item">❌ {g}</div>', unsafe_allow_html=True)
                    st.divider()

                st.markdown('<div class="section-header">🎯 Suggestions</div>', unsafe_allow_html=True)
                for line in suggestions.splitlines():
                    line = line.strip()
                    if line:
                        st.markdown(f'<div class="suggestion-box">{line}</div>', unsafe_allow_html=True)

        # Tab 4 — Cover Letter Points
        with tabs[3]:
            if not api_key:
                st.info("Add your Gemini API key in the sidebar to generate cover letter talking points.")
            else:
                st.markdown("These are key points tailored to connect your experience with this specific role.")
                with st.spinner("Generating cover letter talking points..."):
                    cl_points = get_cover_letter_points(current_resume, current_jd)
                for line in cl_points.splitlines():
                    line = line.strip()
                    if line:
                        st.markdown(f'<div class="suggestion-box">{line}</div>', unsafe_allow_html=True)

        st.divider()

        # ── AI Resume Re-Optimizer Section ──────────────────────────────────
        st.markdown("## 🚀 AI Resume Re-Optimizer (Pro)")
        st.markdown("Unlock a fully tailored, ATS-optimized version of your resume based on this specific job description.")
        
        c_rew1, c_rew2 = st.columns([1, 2])
        with c_rew1:
            rewrite_btn = st.button("Generate Optimized Resume 🔥", type="primary", use_container_width=True)
            
        if rewrite_btn:
            if not api_key:
                st.warning("Please add your Gemini API key in the sidebar to use the re-optimizer.")
            else:
                with st.spinner("Rewriting your resume using advanced AI..."):
                    optimized_text = rewrite_resume_logic(current_resume, current_jd, api_key)
                    st.session_state["optimized_resume"] = optimized_text
                    
        if "optimized_resume" in st.session_state:
            st.success("✅ Optimized Content Ready!")
            with st.expander("Preview Optimized Content"):
                st.markdown(st.session_state["optimized_resume"])
            
            # PDF Generation
            with st.spinner("Preparing professional PDF..."):
                try:
                    pdf_bytes = generate_resume_pdf(st.session_state["optimized_resume"])
                    st.download_button(
                        label="📥 Download Optimized PDF Resume",
                        data=pdf_bytes,
                        file_name="optimized_resume.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {e}")

        st.divider()
        st.caption("Optimization complete · Scores are indicative and based on AI analysis.")
