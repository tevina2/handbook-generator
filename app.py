import streamlit as st
import pdfplumber
import os
from groq import Groq
from supabase import create_client
from dotenv import load_dotenv
import tempfile

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.title("Handbook Generator")
st.write("Upload a PDF and ask questions about it.")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    
    st.write(f"Total characters extracted: {len(full_text)}")
    
    chunks = []
    chunk_size = 500
    words = full_text.split()
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    st.write(f"Document split into {len(chunks)} chunks")

    st.subheader("Chat with your PDF")
    user_question = st.text_input("Ask a question about the document:")

    if user_question:
        with st.spinner("Thinking..."):
            relevant_chunks = chunks[:3]
            context = "\n\n".join(relevant_chunks)
            
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant. Answer questions based on this document content:\n\n{context}"},
                    {"role": "user", "content": user_question}
                ]
            )
        answer = response.choices[0].message.content
        st.write("**Answer:**", answer)
        
        try:
            supabase.table("documents").insert({
                "content": user_question,
                "metadata": {"answer": answer[:500]}
            }).execute()
            st.caption("Conversation saved to database")
        except:
            pass
