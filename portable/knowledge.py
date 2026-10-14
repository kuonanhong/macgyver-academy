"""Small local keyword retriever. No network, embeddings, or execution of documents."""
import json
import math
import re
import threading
from pathlib import Path

STOP = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'what', 'how', 'why', 'into', 'please'}


def terms(text):
    latin = {x for x in re.findall(r'[a-z][a-z0-9_-]{2,}', text.casefold()) if x not in STOP}
    chinese = set()
    for run in re.findall(r'[\u3400-\u9fff]+', text):
        chinese.update(run[i:i + 2] for i in range(len(run) - 1))
    return latin | chinese


class KnowledgeIndex:
    def __init__(self, path):
        self.path = Path(path)
        self.stamp = None
        self.rows = []
        self.lock = threading.Lock()

    def search(self, query, limit=4):
        with self.lock:
            try:
                stamp = self.path.stat().st_mtime_ns
                if stamp != self.stamp:
                    if self.path.stat().st_size > 64 * 1024 * 1024:
                        return []
                    doc = json.loads(self.path.read_text(encoding='utf-8'))
                    if not isinstance(doc, dict) or doc.get('version') != 1 or not isinstance(doc.get('chunks'), list):
                        return []
                    rows = doc['chunks']
                    if len(rows) > 50000:
                        return []
                    self.rows = [(r, terms(r['text'])) for r in rows
                                 if isinstance(r, dict) and isinstance(r.get('text'), str)
                                 and isinstance(r.get('source'), str) and 0 < len(r['source']) <= 500
                                 and len(r['text']) <= 1600
                                 and isinstance(r.get('page', 1), int) and not isinstance(r.get('page', 1), bool)
                                 and 0 < r.get('page', 1) <= 1_000_000]
                    self.stamp = stamp
            except (OSError, ValueError, TypeError, KeyError):
                return []
            q = terms(query)
            if not q:
                return []
            scored = []
            for row, words in self.rows:
                overlap = len(q & words)
                if overlap >= (1 if len(q) <= 2 else 2):
                    scored.append((overlap / math.sqrt(max(len(words), 1)), row))
            scored.sort(key=lambda pair: pair[0], reverse=True)
            return [{k: r[k] for k in ('source', 'page', 'text') if k in r}
                    for _, r in scored[:limit]]
