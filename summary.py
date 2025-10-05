# summarize.py
from unittest import result
import streamlit as st
import pandas as pd
import requests
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="C:\\Users\\rajki\\OneDrive\\Desktop\\Summerizer UI\\key.env")  # or give your full path of dotenv
api_key = os.getenv("MY_API_KEY")


HF_API_TOKEN = api_key  # Or replace with your KEY directly
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}



# Extract text from PDF
def load_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


# Extract text from Excel or CSV
def load_excel(file):
    try:
        df = pd.read_excel(file)
    except Exception:
        df = pd.read_csv(file)
    return df.to_string()


# Summarize text using Hugging Face API (3–5 bullet points)
@st.cache_data(show_spinner=False)
def summarize_text(text):
    # Clean and normalize text
    cleaned_text = (
        text.replace("\n", " ")
            .replace("\r", " ")
            .replace("•", "")
            .replace("-", " ")
            .replace("  ", " ")
            .strip()
    )

    # Split into smaller safe chunks (avoid model crash)
    max_chunk_size = 2500  # characters per chunk
    chunks = [cleaned_text[i:i + max_chunk_size] for i in range(0, len(cleaned_text), max_chunk_size)]

    all_points = []

    for chunk in chunks[:2]:  # only first 2 chunks to keep summary short
        prompt = (
            "Summarize the following content into 3 to 5 concise bullet points. "
            "Each bullet should be a full sentence:\n\n"
            f"{chunk}"
        )

        payload = {
            "inputs": prompt,
            "parameters": {"max_length": 150, "min_length": 40, "do_sample": False},
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=90)
            result = response.json()
        except Exception as e:
            return f"API request failed: {str(e)}"

        # 3️⃣ Process safely
        if isinstance(result, list) and len(result) > 0 and "summary_text" in result[0]:
            summary_text = result[0]["summary_text"].strip()
            sentences = [
                s.strip(" -•\t")
                for s in summary_text.replace("\n", " ").split(". ")
                if len(s.strip()) > 3
            ]
            for s in sentences[:5]:
                all_points.append(f"• {s.strip()}.")
        elif isinstance(result, dict) and "error" in result:
            all_points.append(f"API Error: {result['error']}")
        else:
            all_points.append("Unexpected API response for one chunk.")

    # Combine and limit output
    if not all_points:
        return "No summary generated. Try shorter or clearer text."

    return "\n\n".join(all_points[:5])




st.set_page_config(page_title="Text Summarizer", layout="wide")
st.title("Text & File Summarizer (3–5 Bullet Points)")

st.markdown("**Summarize text or upload a document (PDF, Excel, CSV) — using the Hugging Face API.**")

# Upload file or enter text
uploaded_file = st.file_uploader("Upload File", type=["pdf", "xlsx", "xls", "csv"])
text_input = st.text_area("Or paste your text below:", height=200)

# Summarize button
if st.button("Summarize"):
    if uploaded_file:
        ext = uploaded_file.name.split(".")[-1].lower()
        if ext == "pdf":
            text = load_pdf(uploaded_file)
        else:
            text = load_excel(uploaded_file)
        st.success("File loaded successfully!")
    elif text_input.strip():
        text = text_input.strip()
    else:
        st.warning("Please upload a file or enter text to summarize.")
        st.stop()

    with st.spinner("Summarizing using Hugging Face API..."):
        summary = summarize_text(text)

    st.subheader("Summary (3–5 Bullet Points):")
    st.markdown(summary)
