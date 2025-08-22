def detect_pii(text: str) -> list[str]:
    # Plug in Presidio/regex here if needed
    return []

def annotate_chunk_metadata(chunk):
    pii = detect_pii(chunk.page_content)
    if pii:
        chunk.metadata["pii_flags"] = pii
    return chunk
