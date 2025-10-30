import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
_API_KEY = os.getenv("GEMINI_API_KEY")
if _API_KEY:
    genai.configure(api_key=_API_KEY)

def _build_prompt(feedback_list, analysis_focus):
    header = (
        "You are a concise CX analyst. Return well-structured Markdown.\n"
        "Use clear headings, lists, and, when applicable, short tables.\n\n"
    )
    if analysis_focus == 'Sentiment Analysis':
        task = (
            "## Sentiment\n"
            "Classify overall sentiment (Positive, Neutral, Negative)."
        )
    elif analysis_focus == 'Theme Identification':
        task = (
            "## Key Themes\n"
            "List 3-7 dominant themes with 1-line evidence each."
        )
    elif analysis_focus == 'Improvement Suggestions':
        task = (
            "## Improvement Suggestions\n"
            "Provide prioritized actions (bulleted) and expected impact."
        )
    elif analysis_focus == 'All of the Above':
        task = (
            "## Sentiment\nBriefly classify overall sentiment.\n\n"
            "## Key Themes\nList dominant themes with brief evidence.\n\n"
            "## Suggestions\nProvide prioritized, actionable improvements."
        )
    else:
        return None
    corpus = "\n".join(feedback_list)
    return f"{header}{task}\n\n### Feedback Corpus\n{corpus}"

def analyze_feedback(feedback_list, analysis_focus):
    feedback_list = [str(feedback).strip() for feedback in feedback_list if str(feedback).strip()]
    if not feedback_list:
        return "No valid feedback provided for analysis."

    prompt = _build_prompt(feedback_list, analysis_focus)
    if not prompt:
        return "Invalid analysis focus selected."

    if not _API_KEY:
        return (
            "Gemini API key not found. Please set GEMINI_API_KEY in environment to enable AI analysis."
        )

    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
        return (response.text or "").strip() or "No response from the model."
    except Exception as exc:
        return f"AI analysis error: {exc}"
