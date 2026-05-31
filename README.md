# cloudsec-ai-assistant

AI-powered Cloud Security Engineer Assistant with searchable document ingestion, a Chroma vector knowledge base, and a Streamlit conversational interface.

## Project Overview

This repository demonstrates a practical cloud security assistant architecture with two main components:

- `scripts/load_docs.py`: discovers PDF documents in `docs/`, extracts text, splits it into semantic chunks, generates embeddings, and stores them in a Chroma vector database under `vector_db/`.
- `app.py`: provides a Streamlit UI that queries the Chroma knowledge base and generates answers through OpenAI chat completions.

The project also holds security-related content and artifact folders such as `docs/`, `compliance/`, `incident_response/`, `terraform/`, and `wazuh/`.

## Installation

Create and activate a virtual environment, then install the required Python packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file and set your OpenAI API key:

```bash
cp .env.example .env
```

Then add the key to `.env`:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Build the vector database from your PDF documents:

```bash
source .venv/bin/activate
python scripts/load_docs.py
```

2. Start the Streamlit application:

```bash
source .venv/bin/activate
streamlit run app.py
```

3. Ask cloud security questions through the browser interface.

## Requirements

This repository depends on the following Python packages:

- `streamlit`
- `openai`
- `python-dotenv`
- `chromadb`
- `sentence-transformers`
- `pypdf`

## Notes

- `scripts/load_docs.py` creates the searchable knowledge base from PDF documents.
- `app.py` reads the Chroma collection and uses an OpenAI chat completion model to answer queries.
- If the vector store is missing, the app will show a warning and prompt you to run the ingestion script.
