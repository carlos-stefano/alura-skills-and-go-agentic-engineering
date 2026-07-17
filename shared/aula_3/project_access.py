from pathlib import Path
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".log"
}


def resolve_safe_path(project_root, relative_path):
    root = Path(project_root).resolve()
    requested = (root / relative_path).resolve()

    if requested != root and root not in requested.parents:
        raise ValueError("Acesso negado: caminho fora do target_project.")

    return requested


def list_project_files(project_root, extensions=None):
    allowed_extensions = set(extensions or DEFAULT_EXTENSIONS)
    root = Path(project_root).resolve()

    return [
        str(path.relative_to(root))
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in allowed_extensions
    ]


def read_project_file(project_root, relative_path, max_chars=12000):
    path = resolve_safe_path(project_root, relative_path)

    if not path.is_file():
        return {
            "ok": False,
            "error": "Arquivo inexistente ou não legível.",
            "relative_path": relative_path,
        }

    text = path.read_text(encoding="utf-8", errors="replace")
    root = Path(project_root).resolve()

    return {
        "ok": True,
        "evidence_id": f"project:{path.relative_to(root)}",
        "relative_path": str(path.relative_to(root)),
        "content": text[:max_chars],
        "truncated": len(text) > max_chars,
        "character_count": len(text),
    }


def build_project_catalog(project_root, extensions=None, max_chars_per_file=20000):
    files = list_project_files(project_root, extensions)
    documents = [
        read_project_file(project_root, item, max_chars=max_chars_per_file)
        for item in files
    ]
    documents = [document for document in documents if document["ok"]]

    corpus = [
        f"{document['relative_path']}\n{document['content']}"
        for document in documents
    ]

    if not corpus:
        return {"documents": [], "vectorizer": None, "matrix": None}

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b[\w./:-]+\b",
    )
    matrix = vectorizer.fit_transform(corpus)

    return {
        "documents": documents,
        "vectorizer": vectorizer,
        "matrix": matrix,
    }


def search_project(query, catalog, top_k=5, min_score=0.01):
    if not catalog["documents"] or catalog["vectorizer"] is None:
        return []

    query_vector = catalog["vectorizer"].transform([query])
    scores = cosine_similarity(query_vector, catalog["matrix"]).ravel()

    ranked = sorted(
        [
            {
                "evidence_id": document["evidence_id"],
                "relative_path": document["relative_path"],
                "score": float(score),
                "preview": document["content"][:1200],
            }
            for document, score in zip(catalog["documents"], scores)
            if score >= min_score
        ],
        key=lambda item: item["score"],
        reverse=True,
    )

    return ranked[:top_k]


def to_json(data):
    return json.dumps(data, ensure_ascii=False, indent=2)
