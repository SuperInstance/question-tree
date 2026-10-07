#!/usr/bin/env python3
"""Question Folder Matcher — zeropoc's first instrument.

Input:  a question text string.
Output: ranked closest-matching question-folder path in
        SuperInstance/question-tree, by embedding cosine similarity.

Embedding backend: local Ollama. Designed for TEV1; TEV1 (qwen35-family
generative GGUF) has NO embedding head — see result notes for 001/002.
Fallback backend: nomic-embed-text (137M, runs on the same box).

Usage:
    ./qmatch.py "who changed this file last?"
    ./qmatch.py --json "what is the state of the repo?"
    ./qmatch.py --top 3 "how do i make the repo say hi"
"""
import argparse
import json
import math
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

OLLAMA = "http://127.0.0.1:11434/api/embed"
DEFAULT_MODEL = "nomic-embed-text"   # TEV1 blocker: see --tev1 note below
TREE_DEFAULT = Path.home() / "question-tree"


def embed(texts, model):
    body = json.dumps({"model": model, "input": texts}).encode()
    req = urllib.request.Request(OLLAMA, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["embeddings"]


def folder_docs(tree):
    """Each question-folder becomes one doc: folder name + question.md body."""
    docs = []
    for qdir in sorted(p for p in tree.rglob("q-*") if p.is_dir()):
        parts = []
        name = qdir.name
        # q-how-do-i-greet-a-repo -> "how do i greet a repo"
        readable = re.sub(r"^q-", "", name).replace("-", " ")
        parts.append(readable)
        qfile = qdir / "question.md"
        if qfile.exists():
            parts.append(qfile.read_text(errors="replace")[:500])
        docs.append((qdir.relative_to(tree).as_posix(), " ".join(parts)))
    return docs


def cos(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


def match(question, tree, model, top):
    docs = folder_docs(tree)
    if not docs:
        sys.exit(f"no question-folders (q-*) found under {tree}")
    paths = [p for p, _ in docs]
    mat = embed([question] + [d for _, d in docs], model)
    q, folder_embs = mat[0], mat[1:]
    ranked = sorted(zip(paths, folder_embs), key=lambda t: -cos(q, t[1]))
    return [(p, round(cos(q, e), 4)) for p, e in ranked[:top]]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("question")
    ap.add_argument("--tree", default=str(TREE_DEFAULT))
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help="embedding model (TEV1 cannot embed; generative only)")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    results = match(args.question, Path(args.tree).expanduser(), args.model, args.top)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for p, s in results:
            print(f"{s:.4f}  {p}")


if __name__ == "__main__":
    main()
