from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.title("Cloud Security AI Co-Worker")

VECTOR_DB_DIR = Path("vector_db")
COLLECTION_NAME = "docs"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

@st.cache_resource
def get_chroma_collection() -> chromadb.api.models.Collection | None:
    if not VECTOR_DB_DIR.exists():
        return None

    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    collections = [collection.name for collection in client.list_collections()]
    if COLLECTION_NAME not in collections:
        return None

    return client.get_collection(name=COLLECTION_NAME)

collection = get_chroma_collection()

if collection is None:
    st.warning("No Chroma collection found. Run `scripts/load_docs.py` first and verify `vector_db/docs` exists.")
else:
    query = st.text_input("Ask a cloud security question")

    if query:
        if not OPENAI_API_KEY:
            st.error("OpenAI API key is not set. Add OPENAI_API_KEY to your environment.")
        else:
            results = collection.query(
                query_texts=[query],
                n_results=3,
                include=["documents", "metadatas"],
            )

            documents = results.get("documents", [[]])[0]
            if not documents:
                st.info("No relevant documents were found for that query.")
            else:
                context = "\n\n".join(doc for doc in documents if doc)
                prompt = (
                    "Use the following context to answer the question:\n\n"
                    f"{context}\n\nQuestion: {query}\nAnswer:" 
                )

                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                )
                answer = response["choices"][0]["message"]["content"]
                st.markdown(answer)
