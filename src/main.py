from helpers.handlers import HumanizerHandlers
from utils.config import GEMINI_API_KEY
from api.gemini import GoogleGemini
from utils.logger import SyncLogger
import streamlit as st


logger = SyncLogger("AIHumanizer")


# --- Page Setup ---
st.set_page_config(page_title="AI Humanizer", layout="wide", initial_sidebar_state="collapsed")


# --- Custom CSS ---
st.markdown("""
<style>
    body {
        font-family: 'Roboto', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #D1D3E2;
        padding: 12px;
    }

    .humanize-btn {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }

    .humanize-btn button {
        min-width: 180px;
        font-size: 1.2rem;
        padding: 14px 35px;
        border-radius: 12px;
    }

    .faq-section {
        margin-top: 2rem;
    }

    .faq-title {
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }

    .stExpander .stExpanderHeader {
        font-size: 1.1rem;
        font-weight: 500;
    }

    .stExpander .stExpanderContent {
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Session State ---
for key in ["input", "output", "processing", "humanize_clicked"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key in ["input", "output"] else False


# --- API Key Setup ---
if GEMINI_API_KEY:
    gemini_api_key = GEMINI_API_KEY
else:
    gemini_api_key = st.text_input(
        "🔐 Enter your Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/apikey)) ",
        type="password",
        key="manual_api_key"
    )
    if gemini_api_key:
        st.success("API key set successfully.")

    st.divider()

gemini = GoogleGemini(gemini_api_key) if gemini_api_key else None
handlers = HumanizerHandlers(gemini_api_key)


# --- Header ---
st.markdown("<h1 class='main-title'>🧠 AI Humanizer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Transform AI-generated content into natural, polished, and human-sounding language.</p>", unsafe_allow_html=True)


# --- Input/Output Columns ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### ✍️ AI-Generated Text")
    paste_col, clear_col = st.columns(2)
    if paste_col.button("📋 Paste from Clipboard", use_container_width=True):
        handlers.handle_clipboard_paste()
    if clear_col.button("🗑️ Clear", use_container_width=True):
        handlers.clear_text()
    st.text_area("Enter AI-Generated Text", height=300, key="input", label_visibility="collapsed", disabled=not gemini_api_key, placeholder="Paste or type AI-generated text here...")

with col2:
    st.markdown("#### 🙋 Humanized Output")
    if st.button("📄 Copy to Clipboard", use_container_width=True):
        handlers.copy_to_clipboard()
    st.text_area("Humanized Output", height=300, value=st.session_state.output, label_visibility="collapsed", disabled=not st.session_state.output or not gemini_api_key, key="output_display")


# --- Humanize Button ---
st.markdown("<div class='humanize-btn'>", unsafe_allow_html=True)
if st.columns([3, 1, 3])[1].button("✨ Humanize Text", use_container_width=True, on_click=handlers.on_humanize_click):
    pass
st.markdown("</div>", unsafe_allow_html=True)


# --- Humanization Process ---
if st.session_state.humanize_clicked and not st.session_state.processing:
    st.session_state.humanize_clicked = False
    st.session_state.processing = True
    with st.columns([3, 1, 3])[1]:
        with st.spinner("Humanizing your text..."):
            try:
                logger.write_log("info", f"Humanizing text: {len(st.session_state.input)} characters")
                result = gemini.generate_content(content=st.session_state.input)
                st.session_state.output = result
                logger.write_log("info", f"Humanized text: {len(st.session_state.output)} characters")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                st.session_state.processing = False
        st.rerun()


# --- FAQ Section ---
st.divider()
st.markdown("<div class='faq-section'>", unsafe_allow_html=True)
st.markdown("<h4 class='faq-title'>❓ Frequently Asked Questions</h4>", unsafe_allow_html=True)

with st.expander("How do I use AI Humanizer?"):
    st.write("""
**Step 1:** Paste or type your AI-generated text into the input field.  
**Step 2:** Click the **✨ Humanize Text** button to refine the content.  
**Step 3:** Review the result, then click **📄 Copy to Clipboard** to use the humanized version anywhere you like.
""")

with st.expander("How does AI Humanizer work?"):
    st.write("""
AI Humanizer is powered by **Google's Gemini**, a cutting-edge large language model.  
It uses prompt engineering techniques to rephrase AI-generated text, improving its tone, flow, and readability.  
The system enhances sentence variety, reduces robotic phrasing, and produces writing that sounds more natural and human-like—perfect for essays, emails, social media, and more.
""")

with st.expander("Is AI Humanizer free to use?"):
    st.write("""
Yes! AI Humanizer is completely free and open to everyone.  
It's also an open-source project, so you're welcome to explore the code, report issues, or contribute enhancements.  
Visit our GitHub repository here: [AI Humanzier](https://github.com/dixon2004/ai-humanizer)
""")

st.markdown("</div>", unsafe_allow_html=True)
