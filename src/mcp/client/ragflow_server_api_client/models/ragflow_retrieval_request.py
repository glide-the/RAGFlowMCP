"""Request models for Ragflow retrieval endpoint."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RagflowMetadataConditionClause(BaseModel):
    """Single metadata condition clause for Ragflow retrieval filtering."""

    name: str
    comparison_operator: str
    value: Optional[str] = None


class RagflowMetadataCondition(BaseModel):
    """Grouping of metadata condition clauses."""

    conditions: List[RagflowMetadataConditionClause] = Field(default_factory=list)


class RagflowRetrievalRequest(BaseModel):
    """Payload for `/api/v1/retrieval` requests."""

    question: str

    dataset_ids: Optional[List[str]] = None
    document_ids: Optional[List[str]] = None

    page: int = 1
    page_size: int = 30

    similarity_threshold: float = 0.2
    vector_similarity_weight: float = 0.3
    top_k: int = 1024

    rerank_id: Optional[str] = None
    keyword: bool = False
    highlight: bool = False
    cross_languages: Optional[List[str]] = None
    metadata_condition: Optional[RagflowMetadataCondition] = None
    use_kg: bool = False

    model_config = {"extra": "ignore"}

    def to_payload(self) -> Dict[str, Any]:
        """Return a dict suitable for JSON serialization, excluding ``None`` values."""

        return self.model_dump(exclude_none=True, by_alias=True)
