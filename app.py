import streamlit as st
import pdfplumber

st.title("Handbook Generator")
st.write("Upload a PDF to get started.")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    st.write("File name:", uploaded_file.name)
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    st.subheader("Extracted Text Preview")
    st.text_area("Content", full_text[:2000], height=300)
    st.write(f"Total characters extracted: {len(full_text)}")
