import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def score_gauge(score: float, label: str = "Match Score", color: str = "#4f46e5"):
    """Render a circular gauge chart for a score."""
    if score >= 75:
        bar_color = "#22c55e"
    elif score >= 50:
        bar_color = "#f59e0b"
    else:
        bar_color = "#ef4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"size": 40, "color": "#1e293b"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
            "bar": {"color": bar_color, "thickness": 0.25},
            "bgcolor": "white",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "#fee2e2"},
                {"range": [40, 70], "color": "#fef9c3"},
                {"range": [70, 100], "color": "#dcfce7"},
            ],
            "threshold": {
                "line": {"color": bar_color, "width": 3},
                "thickness": 0.75,
                "value": score,
            },
        },
        title={"text": label, "font": {"size": 15, "color": "#64748b"}},
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(
        height=230,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)


def skill_bar_chart(matched: set, missing: set):
    """Horizontal bar chart showing matched vs missing skill counts."""
    categories = ["Matched skills", "Missing skills"]
    counts = [len(matched), len(missing)]
    colors = ["#22c55e", "#ef4444"]

    fig = go.Figure(go.Bar(
        x=counts,
        y=categories,
        orientation="h",
        marker_color=colors,
        text=counts,
        textposition="inside",
        insidetextanchor="middle",
    ))
    fig.update_layout(
        height=140,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(tickfont=dict(size=13)),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def score_comparison_chart(tfidf_score: float, gemini_score: float, boosted_score: float):
    """Bar chart comparing TF-IDF, Gemini, and projected scores."""
    labels = ["TF-IDF Score", "Gemini Score", "Projected Score"]
    values = [tfidf_score, gemini_score, boosted_score]
    colors = ["#6366f1", "#8b5cf6", "#22c55e"]

    fig = go.Figure(go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
    ))
    fig.update_layout(
        height=280,
        yaxis=dict(range=[0, 110], showgrid=True, gridcolor="#f1f5f9"),
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def skill_tags(skills: set, color: str = "blue"):
    """Render skills as colored pill tags."""
    color_map = {
        "green": ("🟢", "#dcfce7", "#166534"),
        "red": ("🔴", "#fee2e2", "#991b1b"),
        "blue": ("🔵", "#dbeafe", "#1e40af"),
        "gray": ("⚪", "#f1f5f9", "#475569"),
    }
    icon, bg, fg = color_map.get(color, color_map["blue"])
    if not skills:
        st.caption("None detected.")
        return
    pills_html = "".join(
        f'<span style="background:{bg};color:{fg};padding:4px 10px;border-radius:999px;'
        f'font-size:13px;margin:3px;display:inline-block;">{s}</span>'
        for s in sorted(skills)
    )
    st.markdown(f'<div style="line-height:2.2;">{pills_html}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: str = "", color: str = "#4f46e5"):
    """Small metric card with optional delta."""
    delta_html = f'<div style="font-size:12px;color:#64748b;margin-top:2px;">{delta}</div>' if delta else ""
    st.markdown(
        f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;text-align:center;border-top:3px solid {color};">'
        f'<div style="font-size:13px;color:#64748b;margin-bottom:4px;">{label}</div>'
        f'<div style="font-size:28px;font-weight:600;color:#0f172a;">{value}</div>'
        f'{delta_html}</div>',
        unsafe_allow_html=True,
    )
