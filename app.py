import streamlit as st
import pdfplumber
import os
from groq import Groq
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.title("Handbook Generator")
st.write("Upload a PDF, ask questions, or generate a full handbook.")

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
    user_question = st.text_input("Ask a question or type 'generate handbook':")

    if user_question:
        if "generate handbook" in user_question.lower():
            st.info("Generating your 20,000 word handbook... this will take a few minutes.")
            
            handbook_sections = [
                "Introduction and Overview",
                "Core Concepts and Definitions",
                "Key Themes and Analysis",
                "Detailed Examination of Main Topics",
                "Critical Perspectives",
                "Practical Applications",
                "Case Studies and Examples",
                "Comparative Analysis",
                "Implications and Significance",
                "Conclusion and Future Directions"
            ]
            
            full_handbook = f"# Handbook: {uploaded_file.name}\n\n"
            full_handbook += "---\n\n"
            
            progress_bar = st.progress(0)
            
            for i, section in enumerate(handbook_sections):
                with st.spinner(f"Writing section {i+1}/10: {section}..."):
                    chunk_index = min(i * 2, len(chunks) - 1)
                    context = " ".join(chunks[max(0, chunk_index-1):chunk_index+2])
                    
                    response = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": f"You are an expert handbook writer. Write a comprehensive, detailed section of at least 2000 words for a professional handbook based on this document content:\n\n{context}\n\nFull document context:\n\n{full_text[:3000]}"},
                            {"role": "user", "content": f"Write the '{section}' section of the handbook. Be thorough, detailed and comprehensive. Write at least 2000 words for this section."}
                        ],
                        max_tokens=2000
                    )
                    
                    section_content = response.choices[0].message.content
                    full_handbook += f"## {section}\n\n{section_content}\n\n---\n\n"
                    
                progress_bar.progress((i + 1) / len(handbook_sections))
            
            st.success(f"Handbook generated! Total length: {len(full_handbook)} characters")
            st.markdown(full_handbook)
            
            st.download_button(
                label="Download Handbook as Markdown",
                data=full_handbook,
                file_name="handbook.md",
                mime="text/markdown"
            )
            
            try:
                supabase.table("documents").insert({
                    "content": "Generated handbook",
                    "metadata": {"length": len(full_handbook), "sections": len(handbook_sections)}
                }).execute()
            except:
                pass
                
        else:
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
