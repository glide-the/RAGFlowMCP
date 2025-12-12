"""Response models for Ragflow retrieval endpoint."""

from typing import List, Optional

from pydantic import BaseModel


class RagflowChunk(BaseModel):
    content: str
    content_ltks: Optional[str] = None
    document_id: Optional[str] = None
    document_keyword: Optional[str] = None
    highlight: Optional[str] = None
    id: Optional[str] = None
    image_id: Optional[str] = None
    important_keywords: Optional[List[str]] = None
    kb_id: Optional[str] = None
    positions: Optional[List[str]] = None
    similarity: Optional[float] = None
    term_similarity: Optional[float] = None
    vector_similarity: Optional[float] = None


class RagflowDocAgg(BaseModel):
    count: int
    doc_id: str
    doc_name: str


class RagflowRetrievalData(BaseModel):
    chunks: List[RagflowChunk]
    doc_aggs: List[RagflowDocAgg]
    total: int


class RagflowRetrievalResponse(BaseModel):
    code: int
    data: Optional[RagflowRetrievalData] = None
    message: Optional[str] = None

    def is_success(self) -> bool:
        return self.code == 0
