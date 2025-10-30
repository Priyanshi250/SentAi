import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from analysis import analyze_feedback

st.set_page_config(
    page_title="Customer Feedback Analyzer",
    page_icon="💬",
    layout="wide"
)

# Sidebar controls
with st.sidebar:
    st.markdown("## 💬 Customer Feedback Analyzer")
    st.caption("Upload data, explore insights, and generate AI-driven analysis.")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    analysis_focus = st.radio(
        "Analysis focus",
        (
            "Sentiment Analysis",
            "Theme Identification",
            "Improvement Suggestions",
            "All of the Above",
        ),
        index=3,
    )

st.title("Customer Feedback Analyzer")
st.write(
    "Transform raw feedback into actionable insights with a modern, responsive interface."
)

def compute_vader_sentiment(text_series: pd.Series) -> pd.Series:
    analyzer = SentimentIntensityAnalyzer()
    def label(text: str) -> str:
        scores = analyzer.polarity_scores(str(text))
        compound = scores.get("compound", 0.0)
        if compound >= 0.05:
            return "Positive"
        if compound <= -0.05:
            return "Negative"
        return "Neutral"
    return text_series.fillna("").astype(str).apply(label)

def get_basic_stats(text_series: pd.Series) -> dict:
    lengths = text_series.fillna("").astype(str).apply(lambda x: len(x.split()))
    return {
        "num_rows": int(text_series.shape[0]),
        "num_non_null": int(text_series.dropna().shape[0]),
        "avg_words": float(np.round(lengths.mean() if len(lengths) else 0.0, 2)),
    }

def render_overview_tab(df: pd.DataFrame, text_col: str):
    stats = get_basic_stats(df[text_col])
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", f"{stats['num_rows']}")
    col2.metric("Non-empty", f"{stats['num_non_null']}")
    col3.metric("Avg words/review", f"{stats['avg_words']}")

    st.subheader("Sentiment distribution (VADER)")
    sentiments = compute_vader_sentiment(df[text_col])
    sent_df = sentiments.value_counts().rename_axis("sentiment").reset_index(name="count")
    if not sent_df.empty:
        fig = px.bar(
            sent_df,
            x="sentiment",
            y="count",
            color="sentiment",
            text="count",
            title="Sentiment counts",
            color_discrete_map={
                "Positive": "#2ecc71",
                "Neutral": "#95a5a6",
                "Negative": "#e74c3c",
            },
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis_title="Count", xaxis_title="Sentiment", bargap=0.2)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No sentiment data to visualize.")

def simple_top_words(texts: pd.Series, top_k: int = 15) -> pd.DataFrame:
    stop = {
        "the","a","an","and","or","is","are","to","for","of","in","on","it","this",
        "that","with","as","was","were","be","by","at","from","we","you","our","your",
    }
    counts = {}
    for t in texts.fillna("").astype(str):
        for w in str(t).lower().split():
            w = "".join([ch for ch in w if ch.isalnum()])
            if not w or w in stop:
                continue
            counts[w] = counts.get(w, 0) + 1
    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[: top_k]
    return pd.DataFrame(items, columns=["word", "count"]) if items else pd.DataFrame(columns=["word","count"])

def render_pdf(summary_text: str, stats: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x, y = 40, height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "Customer Feedback Insights Report")
    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(x, y, f"Rows: {stats.get('num_rows', 0)}  |  Non-empty: {stats.get('num_non_null', 0)}  |  Avg words: {stats.get('avg_words', 0)}")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "AI Summary")
    y -= 18
    c.setFont("Helvetica", 10)
    # Wrap summary across lines
    for line in summary_text.splitlines():
        for chunk_start in range(0, len(line), 95):
            c.drawString(x, y, line[chunk_start:chunk_start+95])
            y -= 14
            if y < 60:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

if uploaded_file is None:
    st.info("Upload a CSV from the sidebar to get started.")
else:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        st.stop()

    st.subheader("Preview")
    with st.expander("Show first rows", expanded=True):
        st.dataframe(df.head(), use_container_width=True)

    column_name = st.selectbox("Select the column containing reviews", df.columns)
    if not column_name:
        st.warning("Select a text column to continue.")
        st.stop()

    overview_tab, analyze_tab, insights_tab, report_tab = st.tabs([
        "Overview", "AI Analysis", "Insights", "Report"
    ])

    with overview_tab:
        render_overview_tab(df, column_name)

    with analyze_tab:
        st.write("Configure your focus in the sidebar, then run analysis.")
        feedback_list = df[column_name].dropna().astype(str).tolist()
        if st.button("Run AI Analysis", type="primary"):
            with st.spinner("Analyzing with AI..."):
                try:
                    result = analyze_feedback(feedback_list, analysis_focus)
                except Exception as e:
                    result = f"Analysis failed: {e}"
            st.markdown("### Analysis Results")
            st.markdown(result)

    with insights_tab:
        st.subheader("Top words (quick view)")
        words_df = simple_top_words(df[column_name])
        if words_df.empty:
            st.info("No words to display.")
        else:
            fig2 = px.bar(words_df, x="word", y="count", title="Most frequent words")
            st.plotly_chart(fig2, use_container_width=True)

    with report_tab:
        st.subheader("Export PDF")
        stats = get_basic_stats(df[column_name])
        feedback_list = df[column_name].dropna().astype(str).tolist()
        ai_summary = ""
        with st.spinner("Generating AI summary for report..."):
            try:
                ai_summary = analyze_feedback(feedback_list[:200], "All of the Above")  # limit to avoid very long prompts
            except Exception as e:
                ai_summary = f"Summary unavailable: {e}"
        pdf_bytes = render_pdf(ai_summary, stats)
        st.download_button(
            label="Download Insights PDF",
            data=pdf_bytes,
            file_name="customer_feedback_report.pdf",
            mime="application/pdf",
        )


# Hint to run locally (kept for convenience)
# streamlit run main.py
