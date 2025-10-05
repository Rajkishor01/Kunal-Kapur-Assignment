# Kunal-Kapur-Assignment
---
# Text & File Summarizer (3–5 Bullet Points)

This Streamlit app allows you to summarize text or documents (PDF, Excel, CSV) into 3–5 concise bullet points using the Hugging Face API. It is designed for quick and clean summarization while keeping your API key secure.

---

## Features

- Summarize text pasted in the textbox.
- Summarize uploaded files (PDF, Excel, CSV).
- Outputs 3–5 bullet points with clear sentences.
- Handles long documents by chunking content safely.
- Securely loads API key from a `.env` file using `python-dotenv`.
- Streamlit interface for easy usage.

---

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a .env file in the project root folder and add your Hugging Face API key:**
   ```bash
   MY_API_KEY=hf_your_huggingface_key_here
   ```
4. **Run the streamlit app**
   ```bash
   python -m streamlit run summarize.py
   ```

Open the app in your browser (usually http://localhost:8501).

Either:

-Paste text in the textbox, or
-Upload a file (PDF, Excel, CSV).

Click Summarize to generate a 3–5 bullet point summary.
