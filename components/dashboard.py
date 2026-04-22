import streamlit as st
import plotly.graph_objects as go
from components.charts import skill_tags, metric_card

def render_dashboard(resume_text, jd_text, match_score, tfidf_score, gemini_data, skill_data, boosted_score, suggestions, recruiter_view):
    """
    Renders the improved dashboard following the user's specific output requirements.
    """
    st.markdown("# 🔥 AI Resume Optimizer Tool")
    st.divider()

    # ── Scores Section ────────────────────────────────────────────────────────
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"## Match Score: {match_score:.0f}%")
        st.caption("Based on core skill alignment")
    with col_s2:
        st.markdown(f"## Advanced Match: {tfidf_score:.1f}%")
        st.caption("Contextual similarity (TF-IDF)")

    st.divider()

    # ── Skill Breakdown ───────────────────────────────────────────────────────
    st.markdown("### 📊 Skill Match Breakdown")
    
    col_m, col_mi = st.columns(2)
    with col_m:
        st.markdown("**Matched:**")
        st.code(f"{skill_data['matched']}", language="python")
    with col_mi:
        st.markdown("**Missing:**")
        st.code(f"{skill_data['missing']}", language="python")

    st.divider()

    # ── Improve Your Resume ───────────────────────────────────────────────────
    st.markdown("### 📈 Improve Your Resume Score")
    st.markdown("💡 **Add these skills to improve your score:**")
    for skill in skill_data["missing"][:10]: # Show up to 10
        st.markdown(f"➕ **{skill}**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔮 Predicted Score Improvement")
    st.markdown(f"### {match_score:.0f}% → {boosted_score:.0f}% 🚀")

    st.divider()

    # ── Visualization & Inputs ───────────────────────────────────────────────
    col_vis, col_inp = st.columns([2, 2])
    
    with col_vis:
        st.markdown("### 🥧 Visualization (Pie Chart)")
        render_pie_chart(len(skill_data["matched"]), len(skill_data["missing"]))
        
        # Calculate percentages for the label
        total = len(skill_data["matched"]) + len(skill_data["missing"])
        if total > 0:
            p_match = (len(skill_data["matched"]) / total) * 100
            p_miss = (len(skill_data["missing"]) / total) * 100
            st.markdown(f"**Matched**   → {p_match:.0f}%")
            st.markdown(f"**Missing**   → {p_miss:.0f}%")

    with col_inp:
        st.markdown("### 📄 Resume Preview")
        st.text_area("R", value=resume_text[:1000] + "...", height=150, disabled=True, label_visibility="collapsed")
        st.markdown("### 📌 JD Preview")
        st.text_area("J", value=jd_text[:1000] + "...", height=150, disabled=True, label_visibility="collapsed")

    st.divider()

    # ── AI Analysis ───────────────────────────────────────────────────────────
    st.markdown("### 🤖 AI Analysis")
    if gemini_data and gemini_data.get("summary"):
        st.info(gemini_data["summary"])
    
    st.markdown("**Recommendation:**")
    for line in suggestions.splitlines()[:5]:
        if line.strip():
            st.markdown(f"- {line.strip()}")

    st.divider()

    # ── Recruiter View ────────────────────────────────────────────────────────
    st.markdown("### 🧠 What recruiter sees")
    st.markdown('<div style="background-color: #f8fafc; padding: 2rem; border-radius: 12px; border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
    st.markdown(recruiter_view)
    st.markdown('</div>', unsafe_allow_html=True)


def render_pie_chart(matched_count, missing_count):
    """Renders a Plotly pie chart for skills."""
    if matched_count == 0 and missing_count == 0:
        st.caption("No skills to display chart.")
        return

    labels = ["Matched", "Missing"]
    values = [matched_count, missing_count]
    colors = ["#22c55e", "#ef4444"]

    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.4,
        marker_colors=colors,
        textinfo='label+percent',
        insidetextorientation='radial'
    )])
    
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)
