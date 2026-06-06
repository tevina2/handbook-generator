import streamlit as st
st.title("Handbook Generator")
st.write("Welcome!Upload a PDF to get started .")
uploaded_file = st.file_uploader("Upload a PDF ", type="PDF")
if uploaded_file is not None:
  st.success("PDF uploaded successfully!")
  st.write ("File Name:", uploaded_file.name)

