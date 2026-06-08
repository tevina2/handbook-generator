# Handbook Generator

An AI-powered chat application that generates 20,000-word handbooks from uploaded PDF documents

## What It Does
- Upload any PDF document
- Ask questions about the content through a chat interface
- Type "generate handbook" to receive a  structured 20,000+ word document based on your PDF

## Tech Stack
**Frontend:** Streamlit
**AI Model** Groq API ( Llama 3.3 70B)
**PDF Processing** pdfplumber
**Database** Supabase ( pgvector)
**Language** Python 3.12

##Setup Instructions
1. Clone the repository
git clone https://github.com/tevina2/handbook-generator.git
cd handbook-generator

2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install streamlit pdfplumber python-dotenv groq supabase lightrag-hku

4. Set up environment variables
Create an .env file with these values:
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

5. Set up Supabase
Run this in your Supabase SQL editor:
create extension if not exists vector;
create table if not exists documents(
id bigserial primary key,
content text,
embedding vector(384),
metadata jsonb
);

6.Run the app
streamlit run app.py

## How to use
1. Open the app at htttp://localhost:8502
2. Upload a PDF file
3. Ask any question about the document
4. Type "generate handbook" to generate a 20,0000-word handbook
5. Download the handbook using the download button

##API Keys Required
-GROQ_API- Free at console.groq.com
- Supabase- Free at Supabase

##Built by
Tevina Osewe- Lunartech AI Engineering Apprenticeship Assignent-June 2026
READMEEOF
