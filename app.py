
import streamlit as st
import os
import PyPDF2
import numpy as np
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Rockwell Chatbot", layout="wide")
st.title("📐 Rockwell Standards Chatbot")

# Load secrets
openai_key = os.getenv("OPENAI_API_KEY") or (open("secrets.txt").read().strip() if os.path.exists("secrets.txt") else "")
client = OpenAI(api_key=openai_key)

# Load PDF and extract text
def extract_text(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    return "\n\n".join(page.extract_text() for page in reader.pages if page.extract_text())

manual_text = extract_text("FILE_9114.pdf")

chunks = [chunk.strip() for chunk in manual_text.split("\n\n") if len(chunk.strip()) > 40]
vectorizer = TfidfVectorizer().fit(chunks)
chunk_vectors = vectorizer.transform(chunks)

query = st.text_input("Ask a question about the Rockwell standards manual:")
if st.button("Submit") and query:
    query_vec = vectorizer.transform([query])
    sims = cosine_similarity(query_vec, chunk_vectors)[0]
    top_indices = np.argsort(sims)[::-1][:3]
    retrieved = "\n\n".join(chunks[i] for i in top_indices)

    prompt = f"You are a Rockwell CAD standards expert. Use the manual context below to answer clearly.\n\nContext:\n{retrieved}\n\nQuestion: {query}\nAnswer:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    st.markdown("**Answer:**")
    st.write(response.choices[0].message.content.strip())
