import argparse
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from pypdf import PdfReader

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
COLLECTION_NAME = "docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load PDF documents from a docs folder and build a persistent Chroma vector store."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "docs",
        help="Path to the folder containing PDF documents.",
    )
    parser.add_argument(
        "--vector-db-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "vector_db",
        help="Path to the output Chroma vector store directory.",
    )
    parser.add_argument(
        "--model-name",
        default=EMBEDDING_MODEL,
        help="SentenceTransformers model name used for embeddings.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=CHUNK_SIZE,
        help="Maximum number of characters per chunk.",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=CHUNK_OVERLAP,
        help="Number of characters that overlap between chunks.",
    )
    return parser.parse_args()


def load_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            pages.append(text)
    return "\n\n".join(pages)


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text.strip()]

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        if end == text_length:
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            break

        split_at = text.rfind(" ", start, end)
        if split_at <= start:
            split_at = end

        chunk = text[start:split_at].strip()
        if chunk:
            chunks.append(chunk)

        start = split_at - chunk_overlap
        if start < 0:
            start = 0

    return chunks


def build_vector_store(
    docs_dir: Path,
    vector_db_dir: Path,
    model_name: str,
    chunk_size: int,
    chunk_overlap: int,
) -> None:
    docs_dir = docs_dir.resolve()
    vector_db_dir = vector_db_dir.resolve()

    if not docs_dir.is_dir():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    pdf_files = sorted([path for path in docs_dir.iterdir() if path.suffix.lower() == ".pdf"])
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in docs directory: {docs_dir}")

    vector_db_dir.mkdir(parents=True, exist_ok=True)

    all_documents: list[str] = []
    all_metadatas: list[dict[str, str]] = []

    for pdf_path in pdf_files:
        text = load_pdf_text(pdf_path)
        if not text:
            continue

        chunks = split_text(text, chunk_size, chunk_overlap)
        for idx, chunk in enumerate(chunks, start=1):
            all_documents.append(chunk)
            all_metadatas.append({
                "source": pdf_path.name,
                "chunk": str(idx),
            })

    if not all_documents:
        raise ValueError(f"No text extracted from PDFs in {docs_dir}")

    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name=model_name,
        device="cpu",
    )

    client = chromadb.PersistentClient(path=str(vector_db_dir))
    if COLLECTION_NAME in [collection.name for collection in client.list_collections()]:
        client.delete_collection(name=COLLECTION_NAME)

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    collection.add(
        ids=[f"doc-{idx+1}" for idx in range(len(all_documents))],
        documents=all_documents,
        metadatas=all_metadatas,
    )

    print(
        f"Knowledge base created successfully with {len(all_documents)} document chunks."
    )


if __name__ == "__main__":
    args = parse_args()
    build_vector_store(
        docs_dir=args.docs_dir,
        vector_db_dir=args.vector_db_dir,
        model_name=args.model_name,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
