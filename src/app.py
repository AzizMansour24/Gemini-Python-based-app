from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Streamlit UI config
st.set_page_config(page_title="Gemini Text Tool", layout="centered")
st.title("🌐 Gemini Text Summarizer & Translator")
st.write("Enter a paragraph or upload a .txt file. Then choose to summarize or translate it.")

# Input options
paragraph = st.text_area("Enter paragraph:")
uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])

# Common helper to read input
def get_input_text():
    if uploaded_file is not None:
        try:
            return uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading the file: {e}")
            return ""
    elif paragraph.strip():
        return paragraph.strip()
    else:
        st.warning("Please enter text or upload a file.")
        return ""

# Summarize function
def summarize_paragraph(text: str) -> str:
    prompt = f"Summarize the following paragraph in a few sentences:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# Translate function
def translate_paragraph(text: str) -> str:
    prompt = f"Translate the following English text to Arabic:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Summarize"):
        input_text = get_input_text()
        if input_text:
            with st.spinner("Generating summary..."):
                try:
                    summary = summarize_paragraph(input_text)
                    st.success("Summary generated!")
                    st.subheader("📄 Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error generating summary: {e}")

with col2:
    if st.button("🌍 Translate to Arabic"):
        input_text = get_input_text()
        if input_text:
            with st.spinner("Translating to Arabic..."):
                try:
                    translation = translate_paragraph(input_text)
                    st.success("Translation complete!")
                    st.subheader("🗣️ Arabic Translation:")
                    st.write(translation)
                except Exception as e:
                    st.error(f"Error translating: {e}")
