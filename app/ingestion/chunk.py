from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)

def chunk(doc: dict) -> list[Document]:
    chunks = splitter.split_text(doc["cleaned"])
    return [
        Document(
            page_content=c,
            metadata={
                "tenant_id": doc["tenant_id"],
                "source": doc["filename"],
                "path": doc["path"],
                "lang": doc["lang"],
            },
        )
        for c in chunks
    ]
