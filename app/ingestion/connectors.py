from pathlib import Path
from typing import Iterator, Dict

def load_raw_docs(data_dir: str = "data") -> Iterator[Dict]:
    root = Path(data_dir)
    for tenant_dir in root.iterdir():
        if not tenant_dir.is_dir():
            continue
        tenant_id = tenant_dir.name
        for f in tenant_dir.glob("**/*"):
            if f.is_file():
                try:
                    yield {
                        "tenant_id": tenant_id,
                        "filename": f.name,
                        "path": str(f),
                        "content": f.read_text(encoding="utf-8", errors="ignore")
                    }
                except Exception:
                    # Binary or unreadable file; skip in this demo
                    continue
