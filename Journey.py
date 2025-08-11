"""
Journey Map Demo — Full UI with Updated Personas
------------------------------------------------
Interface updated to align with Supply Wisdom customer-research personas.
Run:
  pip install streamlit plotly pandas
  streamlit run demo_app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ------------------------------
# Page setup
# ------------------------------
st.set_page_config(page_title="Journey Map Demo", layout="wide")
st.title("🗺️ Journey Map Demo — Supply Wisdom TPRM")
st.caption("Interface aligned with updated buyer & user personas.")
st.info("🚀 DEMO MODE: All filters and controls visible, core functionality working")

# ------------------------------
# Hardcoded demo data (one touchpoint per persona)
# ------------------------------
DEMO_DATA = [
    {
        "stage": "Reporting & Audit",
        "persona": "Risk Executive",
        "label": "End-to-end audit-evidence automation",
        "sentiment": 0.55,
        "frequency": 30,
        "confidence": 0.85,
        "emoji": "🙂"
    },
    {
        "stage": "Use — Alerts & Triage",
        "persona": "Info Security Executive",
        "label": "Real-time exploit monitoring integration",
        "sentiment": 0.30,
        "frequency": 40,
        "confidence": 0.82,
        "emoji": "🙂"
    },
    {
        "stage": "Approval & Onboarding",
        "persona": "Operating Executive",
        "label": "Shorten vendor onboarding cycles",
        "sentiment": 0.65,
        "frequency": 50,
        "confidence": 0.88,
        "emoji": "😄"
    },
    {
        "stage": "Evaluation & RFx",
        "persona": "Procurement Executive",
        "label": "Risk-balanced sourcing optimization",
        "sentiment": 0.40,
        "frequency": 45,
        "confidence": 0.78,
        "emoji": "🙂"
    },
    {
        "stage": "Onboarding (Healthcare)",
        "persona": "Procurement/Onboarding Specialist",
        "label": "Embed risk intel in RFx",
        "sentiment": 0.45,
        "frequency": 35,
        "confidence": 0.80,
        "emoji": "🙂"
    },
    {
        "stage": "Discover Need",
        "persona": "TPRM Champion / Product Owner",
        "label": "Govern repeatable TPRM program",
        "sentiment": 0.35,
        "frequency": 25,
        "confidence": 0.83,
        "emoji": "🙂"
    },
    {
        "stage": "Continuous Monitoring",
        "persona": "Analyst",
        "label": "Automate alert triage workflows",
        "sentiment": 0.25,
        "frequency": 55,
        "confidence": 0.77,
        "emoji": "🙂"
    },
]

# Pre-laid coordinates for instant layout (one per touchpoint)
COORDINATES = [
    {"x": 0, "y": 0},
    {"x": 1, "y": 1},
    {"x": 2, "y": 2},
    {"x": 3, "y": 3},
    {"x": 4, "y": 4},
    {"x": 5, "y": 5},
    {"x": 6, "y": 6},
]

# Journey stages (x-axis) and updated personas (y-axis)
STAGES = [
    "Discover Need", "Evaluation & RFx", "Approval & Onboarding", "Continuous Monitoring",
    "Use — Alerts & Triage", "Reporting & Audit", "Remediation & Supplier Mgmt",
    "Onboarding (Healthcare)", "Compliance & Oversight", "Renewal & Expansion"
]
PERSONAS = [
    "Risk Executive",
    "Info Security Executive",
    "Operating Executive",
    "Procurement Executive",
    "Procurement/Onboarding Specialist",
    "TPRM Champion / Product Owner",
    "Analyst",
]

# Legacy green-theme map (for reference; unused)
THEMES_ORDER = [
    "Real-time Intelligence", "Process Automation", "Compliance Support",
    "ROI & Efficiency", "Legacy Pain Points", "Risk Coverage", "Time Savings",
]
THEME_MAP = {}

# Blue-heatmap theme mapping for new labels
THEME_MAP_BLUE = {
    "End-to-end audit-evidence automation": ["audit artifacts", "soc2 evidence"],
    "Real-time exploit monitoring integration": ["external intel", "operational"],
    "Shorten vendor onboarding cycles": ["time savings", "process automation"],
    "Risk-balanced sourcing optimization": ["vendor comparison", "cost savings"],
    "Embed risk intel in RFx": ["questionnaire alternative", "external intel"],
    "Govern repeatable TPRM program": ["operational", "real-time intelligence"],
    "Automate alert triage workflows": ["audit artifacts", "operational"],
}

HEATMAP_THEMES = [
    "audit artifacts", "soc2 evidence", "operational", "external intel",
    "time savings", "process automation", "questionnaire alternative",
    "vendor comparison", "cost savings", "real-time intelligence"
]
HEATMAP_STAGES = STAGES  # reuse same ordering

# ------------------------------
# Sidebar — controls
# ------------------------------
with st.sidebar:
    st.header("🔧 Controls")
    st.subheader("✅ Working Controls")
    show_colorbar = st.checkbox("Show sentiment legend", value=False)
    cluster_mode = st.checkbox("Aggregate touchpoints", value=True)

    st.divider()
    st.subheader("🚧 Demo Filters")
    st.caption("Non-functional — illustrates intended interface for engineers")
    st.file_uploader("Upload journey JSON", type=["json"], disabled=True)
    st.multiselect("Personas", options=PERSONAS, default=PERSONAS, disabled=True)
    st.selectbox("Focus Stage", ["All"] + STAGES, index=0, disabled=True)
    st.slider("Min confidence", 0.0, 1.0, 0.6, 0.05, disabled=True)
    st.select_slider("Sentiment range", options=["😡", "😕", "😐", "🙂", "😄"], value=("😡", "😄"), disabled=True)
    st.slider("Bubble size range", 12, 80, (18, 58), disabled=True)
    st.radio("Order personas by", ["Original", "Total frequency", "Avg sentiment"], horizontal=True, disabled=True)
    st.selectbox("Rendering mode", ["Interactive (clicks)", "Safe (no clicks)"], index=0, disabled=True)
    st.date_input("Date range", disabled=True)
    st.multiselect("Industries", ["Telecom", "Banking", "Healthcare", "Insurance", "Financial Services"], disabled=True)

    st.divider()
    st.caption(f"📊 Showing {len(DEMO_DATA)} of {len(DEMO_DATA)} touchpoints")

# ------------------------------
# Tabs
# ------------------------------
tab_journey, tab_evidence, tab_themes, tab_summary, tab_compare, tab_export = st.tabs(
    ["Journey", "Evidence", "Themes", "Summary", "Compare", "Export"]
)

# ------------------------------
# Journey — swim-lanes scatter
# ------------------------------
with tab_journey:
    st.subheader("Journey Swim-lanes")

    df = pd.DataFrame(DEMO_DATA).copy()
    coords = pd.DataFrame(COORDINATES)
    df["x"] = coords["x"]
    df["y"] = coords["y"]

    size_max = 45 if cluster_mode else 55

    fig = px.scatter(
        df,
        x="x", y="y",
        size="frequency",
        color="sentiment",
        hover_data={"x": False, "y": False},
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=0,
        range_color=[-1, 1],
        size_max=size_max,
        opacity=0.88 if cluster_mode else 0.95,
    )
    fig.update_traces(
        mode="markers+text",
        text=df["emoji"], textposition="middle center",
        marker=dict(line=dict(width=1, color="rgba(0,0,0,0.35)"))
    )
    custom = pd.DataFrame({
        "label": df["label"],
        "stage": df["stage"],
        "persona": df["persona"],
        "sentiment_fmt": df["sentiment"].map(lambda v: f"{v:.2f}"),
        "frequency": df["frequency"],
        "emoji": df["emoji"],
    })
    fig.update_traces(
        customdata=custom[["label","stage","persona","sentiment_fmt","frequency","emoji"]],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Stage: %{customdata[1]}<br>"
            "Persona: %{customdata[2]}<br>"
            "Sentiment: %{customdata[3]} %{customdata[5]}<br>"
            "Frequency: %{customdata[4]} mentions"
            "<extra></extra>"
        )
    )

    shapes = []
    for i in range(len(PERSONAS)):
        shapes.append(dict(
            type="rect", xref="x", yref="y",
            x0=-0.5, x1=len(STAGES)-0.5, y0=i-0.45, y1=i+0.45,
            fillcolor="rgba(0,0,0,0.03)" if i % 2 == 0 else "rgba(0,0,0,0.06)",
            line=dict(width=0), layer="below"
        ))
    for i in range(len(STAGES)):
        shapes.append(dict(
            type="line", x0=i, x1=i, y0=-0.5, y1=len(PERSONAS)-0.5,
            xref="x", yref="y",
            line=dict(color="rgba(0,0,0,0.18)", width=1, dash="dot"),
            layer="below"
        ))

    fig.update_layout(
        shapes=shapes,
        xaxis=dict(
            tickmode="array", tickvals=list(range(len(STAGES))), ticktext=STAGES,
            range=[-0.5, len(STAGES)-0.5], title=None, tickangle=-45,
            zeroline=False, showgrid=False
        ),
        yaxis=dict(
            tickmode="array", tickvals=list(range(len(PERSONAS))), ticktext=PERSONAS,
            range=[-0.5, len(PERSONAS)-0.5], title=None,
            zeroline=False, showgrid=False
        ),
        height=520, showlegend=False,
        margin=dict(l=160, r=30, t=20, b=120),
        plot_bgcolor="white", paper_bgcolor="white",
        hoverlabel=dict(bgcolor="white")
    )
    if not show_colorbar:
        fig.update_coloraxes(showscale=False)

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ------------------------------
# Evidence — touchpoint details
# ------------------------------
with tab_evidence:
    st.subheader("Evidence")
    evidence_options = [f"{d['label']} — {d['persona']}" for d in DEMO_DATA]
    selected = st.selectbox("Select a touchpoint", evidence_options)

    # Hardcoded details keyed by label — replace with real data as needed
    evidence_details = {
        d["label"]: {
            "sentiment": f"{d['sentiment']:.2f} {d['emoji']}",
            "frequency": f"{d['frequency']} mentions",
            "quote": "<Insert representative quote here>",
            "themes": ", ".join(THEME_MAP_BLUE.get(d["label"], [])),
            "actions": "<Insert suggested action here>"
        }
        for d in DEMO_DATA
    }

    details = evidence_details[selected.split(" — ")[0]]
    st.markdown(f"### {selected.split(' — ')[0]}")
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**Sentiment:** {details['sentiment']}")
        st.write(f"**Frequency:** {details['frequency']}")
    with c2:
        st.write(f"**Themes:** {details['themes']}")
    st.write("**Quote:**")
    st.write(f"_{details['quote']}_")
    st.write("**Suggested Actions:**")
    st.write(f"• {details['actions']}")

# ------------------------------
# Themes — blue heatmap
# ------------------------------
with tab_themes:
    st.subheader("Themes × Stages")
    st.caption("Heatmap of theme mentions by journey stage (demo)")

    df_themes = pd.DataFrame(DEMO_DATA).copy()
    df_themes["themes"] = df_themes["label"].map(lambda s: THEME_MAP_BLUE.get(s, []))
    df_exp = df_themes.explode("themes").dropna(subset=["themes"])

    if df_exp.empty:
        st.info("No themes found in the current demo selection.")
    else:
        mat = df_exp.groupby(["themes", "stage"])["frequency"].sum().unstack(fill_value=0)
        mat = mat.reindex(index=HEATMAP_THEMES, columns=HEATMAP_STAGES, fill_value=0)

        z = mat.values
        vmax = float(z.max()) if z.size else 1.0

        heat = go.Figure(data=go.Heatmap(
            z=z, x=mat.columns, y=mat.index,
            zmin=0, zmax=vmax, colorscale="Blues",
            colorbar=dict(title="Mentions"),
            hovertemplate="<b>%{y}</b><br>Stage: %{x}<br>Mentions: %{z}<extra></extra>",
        ))
        heat.update_layout(
            xaxis=dict(title=None, tickangle=-35, tickfont=dict(color="#6B7280"),
                       showgrid=False, zeroline=False),
            yaxis=dict(title=None, tickfont=dict(color="#6B7280"),
                       showgrid=False, zeroline=False, autorange="reversed"),
            margin=dict(l=170, r=40, t=10, b=110),
            height=460, paper_bgcolor="white",
            plot_bgcolor="rgba(218, 238, 255, 0.35)",
        )
        st.plotly_chart(heat, use_container_width=True, config={"displayModeBar": False})

# ------------------------------
# Summary — KPI cards, bars, quadrant, brief
# ------------------------------
with tab_summary:
    st.subheader("Summary")
    df_sum = pd.DataFrame(DEMO_DATA)

    colc1, colc2, _ = st.columns([1,1,2])
    with colc1:
        weight_mode = st.selectbox("Weighting", ["Confidence", "Frequency", "Equal"], index=0)
    with colc2:
        low_conf_thresh = st.slider("Low-confidence threshold", 0.5, 0.95, 0.75, 0.01)

    if weight_mode == "Confidence":
        weights = df_sum["confidence"].clip(lower=0.001)
    elif weight_mode == "Frequency":
        weights = df_sum["frequency"].clip(lower=0.001)
    else:
        weights = pd.Series(1.0, index=df_sum.index)

    avg_sentiment = float((df_sum["sentiment"] * weights).sum() / weights.sum())
    total_mentions = int(df_sum["frequency"].sum())
    coverage = len(df_sum) / (len(STAGES) * len(PERSONAS))
    low_conf_share = float((df_sum["confidence"] < low_conf_thresh).mean())

    k1, k2, k4 = st.columns(3)
    with k1: st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
    with k2: st.metric("Total Mentions", f"{total_mentions}")
    with k4: st.metric("Low-confidence Share", f"{low_conf_share:.0%}")

    st.divider()

    # Stage health
    left, right = st.columns(2)
    with left:
        st.markdown("**Stage Health**")
        stage_stats = (
            df_sum.assign(w=weights)
                  .groupby("stage")
                  .apply(lambda g: (g["sentiment"] * g["w"]).sum() / g["w"].sum())
                  .reset_index(name="avg_sentiment")
                  .sort_values("avg_sentiment", ascending=True)
        )
        fig_stage = px.bar(stage_stats, x="avg_sentiment", y="stage",
                           orientation="h", range_x=[-0.2, 1.0],
                           color="avg_sentiment", color_continuous_scale="RdYlGn",
                           labels={"avg_sentiment": "Avg Sentiment", "stage": ""})
        fig_stage.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10),
                                coloraxis_showscale=False)
        fig_stage.add_vline(x=0.40, line_dash="dash", line_color="gray", opacity=0.7)
        st.plotly_chart(fig_stage, use_container_width=True, config={"displayModeBar": False})

    with right:
        st.markdown("**Persona Engagement**")
        persona_agg = (
            df_sum.assign(w=weights)
                  .groupby("persona")
                  .apply(lambda g: pd.Series({
                      "total_mentions": g["frequency"].sum(),
                      "avg_sentiment": (g["sentiment"] * g["w"]).sum() / g["w"].sum()
                  })).reset_index()
                  .sort_values("total_mentions", ascending=True)
        )
        fig_pers = px.bar(persona_agg, x="total_mentions", y="persona",
                          color="avg_sentiment", color_continuous_scale="RdYlGn",
                          orientation="h", labels={"total_mentions": "Mentions", "persona": ""})
        fig_pers.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10),
                               coloraxis_showscale=False)
        st.plotly_chart(fig_pers, use_container_width=True, config={"displayModeBar": False})

    st.divider()

    # Opportunity quadrant
    ql, qr = st.columns([2,1])
    with ql:
        st.markdown("**Opportunities Quadrant**  \n_mentions vs sentiment (each point = touchpoint)_")
        med_freq = df_sum["frequency"].median()
        sent_threshold = 0.30
        fig_sc = px.scatter(
            df_sum, x="frequency", y="sentiment",
            size="frequency", color="sentiment",
            color_continuous_scale="RdYlGn",
            hover_name="label", text=df_sum["persona"],
            size_max=38, range_y=[-0.2, 1.0]
        )
        fig_sc.update_traces(textposition="top center",
                             hovertemplate="<b>%{hovertext}</b><br>Mentions: %{x}<br>Sentiment: %{y:.2f}<extra></extra>")
        fig_sc.add_hline(y=sent_threshold, line_dash="dash", line_color="gray", opacity=0.6)
        fig_sc.add_vline(x=med_freq, line_dash="dash", line_color="gray", opacity=0.6)
        fig_sc.add_annotation(x=med_freq*0.5, y=sent_threshold+0.5, text="Leverage", showarrow=False, opacity=0.7)
        fig_sc.add_annotation(x=med_freq*0.5, y=sent_threshold-0.15, text="Fix first", showarrow=False, opacity=0.7)
        fig_sc.add_annotation(x=med_freq*1.5, y=sent_threshold+0.5, text="Activate", showarrow=False, opacity=0.7)
        fig_sc.add_annotation(x=med_freq*1.5, y=sent_threshold-0.15, text="Low impact", showarrow=False, opacity=0.7)
        fig_sc.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

    with qr:
        st.markdown("**Executive Brief**")
        df_sum["impact_pos"] = df_sum["sentiment"] * df_sum["frequency"]
        wins = df_sum.sort_values("impact_pos", ascending=False).head(2)
        risks = df_sum.sort_values(["sentiment", "frequency"], ascending=[True, False]).head(3)
        brief = (
            f"Overall sentiment is **{avg_sentiment:.2f}** across **{total_mentions}** mentions "
            f"with **{coverage:.0%}** coverage. "
            f"**Wins:** {wins.iloc[0]['label']} ({wins.iloc[0]['sentiment']:.2f}), "
            f"{wins.iloc[1]['label']} ({wins.iloc[1]['sentiment']:.2f}). "
            f"**Risks:** {risks.iloc[0]['label']} ({risks.iloc[0]['sentiment']:.2f}), "
            f"{risks.iloc[1]['label']} ({risks.iloc[1]['sentiment']:.2f}), "
            f"{risks.iloc[2]['label']} ({risks.iloc[2]['sentiment']:.2f}). "
            f"**Next moves:** Investigate '{risks.iloc[0]['label']}' in {risks.iloc[0]['stage']}; "
            f"accelerate adoption with {wins.iloc[0]['persona']}; "
            f"standardize reporting in {wins.iloc[1]['stage']}."
        )
        st.write(brief)
        st.text_area("Copy-ready text", brief, height=180)

# ------------------------------
# Compare & Export (placeholders)
# ------------------------------
with tab_compare:
    st.subheader("Compare Studies")
    st.info("🚧 Demo: Comparison UI")
    st.file_uploader("Upload comparison JSON", type=["json"], disabled=True)
    st.write("• Current vs. previous sentiment…")

with tab_export:
    st.subheader("Export")
    st.info("🚧 Demo: Export UI")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("⬇️ Download CSV", disabled=True)
    with c2: st.button("⬇️ Download JSON", disabled=True)
    with c3: st.button("⬇️ Download PNG", disabled=True)
    st.write("**Options:** CSV, JSON, PNG")

# ------------------------------
# Debug Footer / Notes
# ------------------------------
st.divider()
with st.expander("🔍 Demo Technical Details"):
    st.markdown("""
**Working Features**
- ✅ Journey swim-lane visualization (Plotly)
- ✅ Evidence touchpoint details
- ✅ Sentiment legend toggle
- ✅ Aggregation (cluster) style toggle
- ✅ Interactive hover tooltips

**Demo (non-functional)**
- 🚧 File upload
- 🚧 Persona/stage filtering
- 🚧 Confidence thresholds
- 🚧 Visual customization
- 🚧 Data export
- 🚧 Comparison tools

**Performance Optimizations**
- Pre-laid coordinates for instant layout
- Hardcoded evidence database
- Minimal per-frame computation
- Static tables with fixed heights
    """)
