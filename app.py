import streamlit as st
import pdfplumber
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("Handbook Generator")
st.write("Upload a PDF and ask questions about it.")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    st.subheader("Extracted Text Preview")
    st.text_area("Content", full_text[:2000], height=200)
    st.write(f"Total characters extracted: {len(full_text)}")

    st.subheader("Chat with your PDF")
    user_question = st.text_input("Ask a question about the document:")

    if user_question:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant. Answer questions based on this document:\n\n{full_text[:8000]}"},
                    {"role": "user", "content": user_question}
                ]
            )
        answer = response.choices[0].message.content
        st.write("**Answer:**", answer)
