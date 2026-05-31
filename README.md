# cloudsec-ai-assistant

AI-powered Cloud Security Engineer Assistant built to demonstrate practical cloud security automation, documentation ingestion, and retrieval-augmented generation (RAG) with modern Python tooling.

## Dependency Manifest

The `requirements.txt` file currently contains no pinned Python packages; it is empty at this time.

## What This Project Implements

This repository captures the end-to-end work required to build a searchable, AI-enabled security assistant for cloud and compliance teams:

- Built a document ingestion pipeline in `scripts/load_docs.py` that discovers PDFs in `docs/`, splits content into semantic chunks, creates embeddings, and stores them in a Chroma vector database under `vector_db/`.
- Designed the project to support security and incident response knowledge by organizing content in folders such as `docs/`, `compliance/`, and `incident_response/`.
- Included a core application entry point in `app.py` to serve as the foundation for the assistant interface and integration logic.
- Added infrastructure and deployment artifacts such as `Dockerfile` and `requirements.txt` to support containerized execution and reproducible Python environments.
- Preserved example security telemetry and tooling artifacts, including the `wazuh/` folder and `terraform/` support files, to demonstrate experience with cloud security operations and infrastructure-as-code.

## Document Ingestion

The script `scripts/load_docs.py` is the main automation used so far. It:

1. loads PDF documents from the `docs/` directory,
2. splits the text into smaller, searchable chunks,
3. generates vector embeddings for semantic search,
4. stores the vectors in `vector_db/` using Chroma.

### Usage

```bash
source .venv/bin/activate
python scripts/load_docs.py
```

### Optional Arguments

```bash
python scripts/load_docs.py --docs-dir docs --vector-db-dir vector_db
```

## Next Steps

This repository is positioned to grow into a full security engineering assistant by adding an interactive UI, additional cloud connector integrations, and further automation for incident investigation and compliance reporting.
