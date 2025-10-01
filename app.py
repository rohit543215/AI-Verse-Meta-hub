import streamlit as st
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load knowledge base from markdown files
def load_knowledge():
    knowledge = []
    data_folder = "data"
    if os.path.exists(data_folder):
        for file in os.listdir(data_folder):
            if file.endswith(".md"):
                with open(os.path.join(data_folder, file), encoding="utf-8") as f:
                    text = f.read()
                    # Split into paragraphs or sentences for better granularity
                    parts = text.split("\n\n")
                    knowledge.extend([p.strip() for p in parts if p.strip()])
    return knowledge

KNOWLEDGE = load_knowledge()

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings of knowledge base
knowledge_embeddings = model.encode(KNOWLEDGE, convert_to_tensor=True)

st.title("Toro Chatbot with Transformers")

query = st.text_input("Ask a question")
if st.button("Ask") and query.strip():
    query_emb = model.encode([query], convert_to_tensor=True)

    # Compute cosine similarity between query and knowledge base
    similarities = cosine_similarity(query_emb.cpu(), knowledge_embeddings.cpu())[0]

    # Find best matching paragraph
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]

    if best_score > 0.5:  # threshold for matching confidence
        response = KNOWLEDGE[best_idx]
    else:
        response = "I don't know that yet. Try asking about TORO or AI tools."

    st.markdown(f"**Answer:** {response}")
else:
    st.write("Enter a question and press Ask")
